<template>
  <audio id="remoteAudio"></audio>
 <div ref="callPopup" v-show="showCallPopup" :style="style" class="fixed z-20 bg-gray-900 text-gray-300 p-4 rounded-lg">
    <MinimizeIcon class="cursor-pointer" @click="toggleCallWindow" />
    <div>{{ callStatus }}</div>
    <div v-if="onCall">In Call</div>
    <div>
      <Button :icon="muted ? 'mic-off' : 'mic'" @click="toggleMute" />
      <Button @click="togglePopover"><ReplyIcon /></Button>
      <Button class="bg-red-600" @click="hangUpCall"><PhoneIcon /></Button>
    </div>
    <div v-if="showPopover" class="absolute bg-white shadow-lg p-4 rounded">
      <h3>Transfer Call To:</h3>
      <ul>
        <li v-for="user in organizationUsers" :key="user.id" class="mb-2">
          <div class="flex justify-between items-center">
            <span>{{ user.cid_name }}-{{ user.extension }}</span>
            <Button @click="transferCall(user.extension)" class="text-blue-500">Transfer</Button>
          </div>
        </li>
      </ul>
    </div>
  </div>
  <div v-show="showSmallCallWindow" @click="toggleCallWindow">
    <span>{{ callStatus }}</span>
  </div>
</template>

<script setup>
import MinimizeIcon from '@/components/Icons/MinimizeIcon.vue'
import ReplyIcon from '@/components/Icons/ReplyIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import { Inviter, Registerer, SessionState, TransportState, UserAgent } from 'sip.js'
import { useDraggable, useWindowSize } from '@vueuse/core'
import { ref, onMounted } from 'vue'
import { call } from 'frappe-ui'

const showCallPopup = ref(false)
const showSmallCallWindow = ref(false)
const onCall = ref(false)
const calling = ref(false)
const muted = ref(false)
const showPopover = ref(false)
const callPopup = ref(null)
const callStatus = ref('')
const organizationUsers = ref([])
let activeSession = null
let wsDetails = null
let sipServer = null
let userAgent = null
let uaConfig = null
let connectAttempt = 0
let uri = null
let joinDTMF = null
let leaveDTMF = null
let onlineStatus = 0

async function getOrganizationUsers() {
  try {
    const users = await call('vulero_dialer.config.user_list.fetch_users_to_transfer', {},
      { headers: { 'X-Frappe-CSRF-Token': window.frappe.csrf_token } })
    organizationUsers.value = users.status === 'OK' ? users.result : []
  } catch (e) {
    organizationUsers.value = []
  }
}

async function onInvite(session) {
  showCallPopup.value = true
  activeSession = session
  session.stateChange.addListener((newState) => {
    switch (newState) {
      case SessionState.Established:
        audioConfig(session)
        onCall.value = true
        break
      case SessionState.Terminated:
        cleanup()
        break
    }
  })
}

const { width, height } = useWindowSize()
const { style } = useDraggable(callPopup, {
  initialValue: { x: width.value - 280, y: height.value - 310 },
  containerElement: document.body,
  preventDefault: true
})

async function startupClient() {
  ++connectAttempt
  wsDetails = await call('vulero_dialer.config.call_setting.get_user_settings', {},
    { headers: { 'X-Frappe-CSRF-Token': window.frappe.csrf_token } })
  const { username, cid_name, ep_pass: password, pri_sip_address, sec_sip_address } = wsDetails.result
  sipServer = connectAttempt > 3 ? sec_sip_address : pri_sip_address
  const wsServer = `wss://${sipServer}:8089/ws`
  uri = UserAgent.makeURI(`sip:${username}@${sipServer}`)
  uaConfig = {
    uri,
    media: { remote: { audio: document.getElementById('remoteAudio') } },
    delegate: { onInvite },
    transportOptions: { server: wsServer, keepAliveInterval: 5 },
    register: true,
    authorizationUsername: username,
    authorizationPassword: password,
    displayName: cid_name
  }
  userAgent = new UserAgent(uaConfig)
  userAgent.transport.stateChange.addListener((state) => {
    if (state === TransportState.Connected) onlineStatus = 1
    if (state === TransportState.Disconnected) {
      onlineStatus = 0
      if (connectAttempt < 10) setTimeout(startupClient, 5000)
    }
  })
  await registerSipUser()
}

async function registerSipUser() {
  const registerer = new Registerer(userAgent, uri)
  await userAgent.start()
  registerer.register().catch(console.log)
}

function togglePopover() {
  showPopover.value = !showPopover.value
}

function toggleMute() {
  handleMute(!muted.value)
  muted.value = !muted.value
}

function handleMute(enable) {
  const pc = activeSession.sessionDescriptionHandler.peerConnection
  if (!pc) return
  pc.getSenders().forEach((sender) => {
    if (sender.track) sender.track.enabled = enable
  })
}

function hangUpCall() {
  if (!activeSession) return
  if (activeSession.state === 'Established') {
    activeSession.bye()
  } else {
    activeSession.cancel()
  }
  cleanup()
}

async function makeOutgoingCall(number) {
  if (!onlineStatus) return
  let dtmfType = number
  if (number === 'join_queue' && joinDTMF) number = joinDTMF
  if (number === 'leave_queue' && leaveDTMF) number = leaveDTMF
  const target = UserAgent.makeURI(`sip:${number}@${sipServer}`)
  const inviter = new Inviter(userAgent, target, {
    earlyMedia: true,
    sessionDescriptionHandlerOptions: { constraints: { audio: true, video: false } }
  })
  activeSession = inviter
  await userAgent.start().then(() => inviter.invite())
  if (number[0] !== '*') {
    showCallPopup.value = true
    calling.value = true
    callStatus.value = 'initiating'
  }
  inviter.stateChange.addListener((state) => {
    switch (state) {
      case SessionState.Establishing:
        callStatus.value = 'ringing'
        earlyMediaConfig(inviter)
        break
      case SessionState.Established:
        callStatus.value = ''
        onCall.value = true
        calling.value = false
        audioConfig(inviter)
        window.dispatchEvent(new CustomEvent('queueEvent', { detail: dtmfType }))
        break
      case SessionState.Terminated:
        cleanup()
        break
    }
  })
}

function cancelCall() {
  if (!activeSession) return
  if (activeSession.state === 'Initial' || activeSession.state === 'Established') {
    activeSession.bye()
  } else if (activeSession.state === 'Establishing') {
    activeSession.cancel()
  }
  cleanup()
}

function transferCall(number) {
  if (!activeSession) return
  const target = UserAgent.makeURI(`sip:${number}@${sipServer}`)
  activeSession.refer(target).then(cleanup).catch(console.log)
}

function toggleCallWindow() {
  showCallPopup.value = !showCallPopup.value
  showSmallCallWindow.value = !showSmallCallWindow.value
}

function cleanup() {
  showCallPopup.value = false
  showSmallCallWindow.value = false
  onCall.value = false
  calling.value = false
  callStatus.value = ''
  muted.value = false
  showPopover.value = false
  const audio = document.getElementById('remoteAudio')
  audio.srcObject = null
  audio.pause()
  activeSession = null
}

function earlyMediaConfig(session) {
  const mediaElement = document.getElementById('remoteAudio')
  const remoteStream = new MediaStream()
  session.sessionDescriptionHandler.peerConnection.getReceivers().forEach((r) => {
    if (r.track) remoteStream.addTrack(r.track)
  })
  mediaElement.srcObject = remoteStream
  mediaElement.play()
}

function audioConfig(session) {
  const mediaElement = document.getElementById('remoteAudio')
  const remoteStream = new MediaStream()
  session.sessionDescriptionHandler.peerConnection.getReceivers().forEach((r) => {
    if (r.track) remoteStream.addTrack(r.track)
  })
  mediaElement.srcObject = remoteStream
  mediaElement.play()
}

onMounted(async () => {
  await startupClient()
  try {
    const queueSettings = await call('vulero_dialer.config.call_setting.get_queue_settings', {},
      { headers: { 'X-Frappe-CSRF-Token': window.frappe.csrf_token } })
    if (queueSettings) {
      joinDTMF = queueSettings.join_dtmf
      leaveDTMF = queueSettings.leave_dtmf
    }
  } catch (e) {
    console.log('Error fetching queue details', e)
  }
  window.addEventListener('callEvent', (e) => makeOutgoingCall(e.detail.number))
  await getOrganizationUsers()
})
</script>
