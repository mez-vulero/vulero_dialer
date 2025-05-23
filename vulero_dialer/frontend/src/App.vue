<template>
  <button @click="simulateIncomingCall">Simulate Incoming Call</button>
  <audio ref="xaid" id="remoteAudio"> </audio>

  <div v-show="showCallPopup">
    <div
      ref="callPopup"
      class="fixed z-20 flex w-60 cursor-move select-none flex-col rounded-lg bg-gray-900 p-4 text-gray-300 shadow-2xl"
      :style="style"
    >
      <div class="flex flex-row-reverse items-center gap-1">
        <MinimizeIcon
          class="h-4 w-4 cursor-pointer"
          @click="toggleCallWindow"
        />
      </div>
      <div class="flex flex-col items-center justify-center gap-3">
        <Avatar
          :image="contact.image"
          :label="contact.full_name"
          class="relative flex !h-24 !w-24 items-center justify-center [&>div]:text-[30px]"
          :class="onCall || calling ? '' : 'pulse'"
        />
        <div class="flex flex-col items-center justify-center gap-1">
          <div class="text-xl font-medium">
            {{ contact.full_name }}
          </div>
          <div class="text-sm text-gray-600">{{ contact.mobile_no }}</div>
        </div>
        <CountUpTimer ref="counterUp">
          <div v-if="onCall" class="my-1 text-base">
            {{ counterUp?.updatedTime }}
          </div>
        </CountUpTimer>
        <div v-if="!onCall" class="my-1 text-base">
          {{
            callStatus == 'initiating'
              ? 'Initiating call...'
              : callStatus == 'ringing'
              ? 'Ringing...'
              : calling
              ? 'Calling...'
              : 'Incoming call...'
          }}
        </div>
        <div v-if="onCall" class="flex gap-2">
          <Button
            :icon="muted ? 'mic-off' : 'mic'"
            class="rounded-full"
            @click="toggleMute"
          />
          <!-- <Button class="rounded-full">
          <template #icon>
            <DialpadIcon class="cursor-pointer rounded-full" />
          </template>
        </Button> -->
          <Button class="rounded-full">
            <template #icon>
              <NoteIcon
                class="h-4 w-4 cursor-pointer rounded-full text-gray-900"
                @click="showNoteModal = true"
              />
            </template>
          </Button>
          <Button class="rounded-full bg-red-600 hover:bg-red-700">
            <template #icon>
              <PhoneIcon
                class="h-4 w-4 rotate-[135deg] fill-white text-white"
                @click="hangUpCall"
              />
            </template>
          </Button>
        </div>
        <div v-else-if="calling || callStatus == 'initiating'">
          <Button
            size="md"
            variant="solid"
            theme="red"
            label="Cancel"
            @click="cancelCall"
            class="rounded-lg"
            :disabled="callStatus == 'initiating'"
          >
            <template #prefix>
              <PhoneIcon class="h-4 w-4 rotate-[135deg] fill-white" />
            </template>
          </Button>
        </div>
        <div v-else class="flex gap-2">
          <Button
            size="md"
            variant="solid"
            theme="green"
            label="Accept"
            class="rounded-lg"
            @click="acceptIncomingCall"
          >
            <template #prefix>
              <PhoneIcon class="h-4 w-4 fill-white" />
            </template>
          </Button>
          <Button
            size="md"
            variant="solid"
            theme="red"
            label="Reject"
            class="rounded-lg"
            @click="rejectIncomingCall"
          >
            <template #prefix>
              <PhoneIcon class="h-4 w-4 rotate-[135deg] fill-white" />
            </template>
          </Button>
        </div>
      </div>
    </div>
  </div>
  <div
    v-show="showSmallCallWindow"
    class="ml-2 flex cursor-pointer select-none items-center justify-between gap-3 rounded-lg bg-gray-900 px-2 py-[7px] text-base text-gray-300"
    @click="toggleCallWindow"
  >
    <div class="flex items-center gap-2">
      <Avatar
        :image="contact.image"
        :label="contact.full_name"
        class="relative flex !h-5 !w-5 items-center justify-center"
      />
      <div class="max-w-[120px] truncate">
        {{ contact.full_name }}
      </div>
    </div>
    <div v-if="onCall" class="flex items-center gap-2">
      <div class="my-1 min-w-[40px] text-center">
        {{ counterUp?.updatedTime }}
      </div>
      <Button variant="solid" theme="red" class="!h-6 !w-6 rounded-full">
        <template #icon>
          <PhoneIcon
            class="h-4 w-4 rotate-[135deg] fill-white"
            @click.stop="hangUpCall"
          />
        </template>
      </Button>
    </div>
    <div v-else-if="calling" class="flex items-center gap-3">
      <div class="my-1">
        {{ callStatus == 'ringing' ? 'Ringing...' : 'Calling...' }}
      </div>
      <Button
        variant="solid"
        theme="red"
        class="!h-6 !w-6 rounded-full"
        @click.stop="cancelCall"
      >
        <template #icon>
          <PhoneIcon class="h-4 w-4 rotate-[135deg] fill-white" />
        </template>
      </Button>
    </div>
    <div v-else class="flex items-center gap-2">
      <Button
        variant="solid"
        theme="green"
        class="pulse relative !h-6 !w-6 rounded-full"
        @click.stop="acceptIncomingCall"
      >
        <template #icon>
          <PhoneIcon class="h-4 w-4 animate-pulse fill-white" />
        </template>
      </Button>
      <Button
        variant="solid"
        theme="red"
        class="!h-6 !w-6 rounded-full"
        @click.stop="rejectIncomingCall"
      >
        <template #icon>
          <PhoneIcon class="h-4 w-4 rotate-[135deg] fill-white" />
        </template>
      </Button>
    </div>
  </div>
  <NoteModal
    v-model="showNoteModal"
    :note="note"
    doctype="CRM Call Log"
    @after="updateNote"
  />
</template>

<script setup>
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import MinimizeIcon from '@/components/Icons/MinimizeIcon.vue'
import DialpadIcon from '@/components/Icons/DialpadIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import CountUpTimer from '@/components/CountUpTimer.vue'
import NoteModal from '@/components/Modals/NoteModal.vue'
import { Device } from '@twilio/voice-sdk'
import {
    Inviter,
    Registerer,
    RegistererState,
    SessionState,
    UserAgent,
} from "sip.js";
import { useDraggable, useWindowSize } from '@vueuse/core'
import { globalStore } from '@/stores/global'
import { contactsStore } from '@/stores/contacts'
import { Avatar, call } from 'frappe-ui'
import { onMounted, ref, watch } from 'vue'

const { getContact, getLeadContact } = contactsStore()
const { setMakeCall, setTwilioEnabled, $dialog } = globalStore()

let device = ''
let log = ref('Connecting...')
let _call = null
const contact = ref({
  full_name: '',
  mobile_no: '',
})

let showCallPopup = ref(false)
let showSmallCallWindow = ref(false)
let onCall = ref(false)
let calling = ref(false)
let muted = ref(false)
let callPopup = ref(null)
let counterUp = ref(null)
let callStatus = ref('')
const showNoteModal = ref(false)
const note = ref({
  title: '',
  content: '',
})

const jsonResponse =
      { "status": "OK", "result": { "id": "1149", "pkg_id": "2", "ep_pass": "pS19WMNVz6wj2a0i", "vm_pin": "746390", "cid_name": "Mezmure Dawit", "extension": "835266", "username": "117S835266", "pri_sip_public": "196.189.53.123", "pri_sip_private": "10.10.11.121", "pri_sip_address": "etw-pbx-sip1.websprix.com", "sec_sip_public": "196.189.53.124", "sec_sip_private": "10.10.11.122", "sec_sip_address": "etw-pbx-sip2.websprix.com" } }

    const {
      username,
      cid_name,
      ep_pass: password,
      pri_sip_address: sipServer
    } = jsonResponse.result;

    navigator.mediaDevices.getUserMedia({audio:true})

    const wsServer = `wss://${sipServer}:8089/ws`;

    var activeSession = null;

    const uri = UserAgent.makeURI(`sip:${username}@${sipServer}`);

    const uaConfig =
    {
      uri: uri,
      media: {
        remote: {
          audio: document.getElementById('remoteAudio'),
        },
      },
      delegate: {
  	    onInvite: onInvite,
  	      onMessage: function(message) {
    	      console.log("Received SIP message:", message);
  	      },
  	      onTransportError: function() {
    	      console.log("Transport Error");
  	      },
  	      onRegistered: function() {
    	      console.log("Successfully registered!");
  	      },
            onRegistrationFailed: function(cause) {
            console.log("Registration failed:", cause);
          }
      },
      transportOptions: {
        server: wsServer,
        traceSip: true,
        keepAliveInterval: 5,
      },
      hackIpInContact: true,
      authorizationUsername: username,
      authorizationPassword: password,
      displayName: cid_name,
      sessionDescriptionHandlerFactoryOptions: {
        peerConnectionOptions: {
          iceCheckingTimeout: 5000,
          rtcConfiguration: {
            /*  iceServers: [
                { urls: 'stun:stun.l.google.com:19302' }
              ],
            },*/
          },
        },
      }
    };

    const userAgent = new UserAgent(uaConfig);

    const registerer = new Registerer(userAgent, uri);

    userAgent.start().then(() => {
      registerer.register();
    });

    function onInvite(session) {
      showCallPopup.value=true;
      activeSession = session;  // Store the active session globally if needed elsewhere
      session.stateChange.addListener((newState) => {
          switch (newState) {
              case SessionState.Establishing:
                  // Handle establishing state if needed
                  break;
              case SessionState.Established:
                  // Call audio configuration when the session is established
                  audioConfig(session);
                  break;
              case SessionState.Terminated:
                  activeSession = null;
                  showCallPopup.value = false
                  if (showSmallCallWindow.value == undefined) {
                    showSmallCallWindow = false
                  } else {
                    showSmallCallWindow.value = false
                  }
                  muted.value = false
                  onCall.value = false
                  cleanupMedia()
                  counterUp.value.stop()
                  break;
              default:
                  break;
          }
      });
    };


async function updateNote(_note, insert_mode = false) {
  note.value = _note
  if (insert_mode && _note.name) {
    await call('crm.integrations.twilio.api.add_note_to_call_log', {
      call_sid: _call.parameters.CallSid,
      note: _note.name,
    })
  }
}

const { width, height } = useWindowSize()

let { style } = useDraggable(callPopup, {
  initialValue: { x: width.value - 280, y: height.value - 310 },
  preventDefault: true,
})

async function is_twilio_enabled() {
  return await call('crm.integrations.twilio.api.is_enabled')
}

async function startupClient() {
  log.value = 'Requesting Access Token...'

  try {
    //const data = await call('crm.integrations.twilio.api.generate_access_token')
    //log.value = 'Got a token.'
    //intitializeDevice(data.token)
    await registerSipUser();
  } catch (err) {
    log.value = 'An error occurred. ' + err.message
  }
}

function intitializeDevice(token) {
  device = new Device(token, {
    codecPreferences: ['opus', 'pcmu'],
    fakeLocalDTMF: true,
    enableRingingState: true,
  })

  addDeviceListeners()

  device.register()
}

function addDeviceListeners() {
  device.on('registered', () => {
    log.value = 'Ready to make and receive calls!'
  })

  device.on('unregistered', (device) => {
    log.value = 'Logged out'
  })

  device.on('error', (error) => {
    log.value = 'Twilio.Device Error: ' + error.message
  })

  device.on('incoming', handleIncomingCall)

  device.on('tokenWillExpire', async () => {
    const data = await call('crm.integrations.twilio.api.generate_access_token')
    device.updateToken(data.token)
  })
}

async function registerSipUser() {
    const uri = UserAgent.makeURI(`sip:${username}@${sipServer}`);
    const uaConfig =
    {
      uri: uri,
      media: {
        remote: {
          audio: document.getElementById('remoteAudio'),
        },
      },
      delegate: {
  	    onInvite: onInvite,
  	      onMessage: function(message) {
    	      console.log("Received SIP message:", message);
  	      },
  	      onTransportError: function() {
    	      console.log("Transport Error");
  	      },
  	      onRegistered: function() {
    	      console.log("Successfully registered!");
  	      },
            onRegistrationFailed: function(cause) {
            console.log("Registration failed:", cause);
          }
      },
      transportOptions: {
        server: wsServer,
        traceSip: true,
        keepAliveInterval: 5,
      },
      hackIpInContact: true,
      authorizationUsername: username,
      authorizationPassword: password,
      displayName: cid_name,
      sessionDescriptionHandlerFactoryOptions: {
        peerConnectionOptions: {
          iceCheckingTimeout: 5000,
          rtcConfiguration: {
            /*  iceServers: [
                { urls: 'stun:stun.l.google.com:19302' }
              ],
            },*/
          },
        },
      }
    };

    const userAgent = new UserAgent(uaConfig);

    const registerer = new Registerer(userAgent, uri);

    userAgent.start().then(() => {
      registerer.register();
    });
}

function toggleMute() {
    console.log(muted)
  if (!muted.value) {
    //_call.mute(false)
    muted.value = true
  } else {
    muted.value = false
  }
}

function handleIncomingCall(call) {
  log.value = `Incoming call from ${call.parameters.From}`

  // get name of the caller from the phone number
  contact.value = "Mezmure Dawit"//getContact(call.parameters.From)
  if (!contact.value) {
    contact.value = "Yoseph"//getLeadContact(call.parameters.From)
  }

  if (!contact.value) {
    contact.value = {
      full_name: 'Unknown',
      mobile_no: '994'//call.parameters.From,
    }
  }

  showCallPopup.value = true
  _call = call

  _call.on('accept', (conn) => {
    console.log('conn', conn)
  })

  // add event listener to call object
  call.on('cancel', handleDisconnectedIncomingCall)
  call.on('disconnect', handleDisconnectedIncomingCall)
  call.on('reject', handleDisconnectedIncomingCall)
}

async function acceptIncomingCall() {
  log.value = 'Accepted incoming call.'
  onCall.value = true
  activeSession.accept()
  counterUp.value.start()
}

function rejectIncomingCall() {
  activeSession.reject().catch((error) => console.log(error));
  log.value = 'Rejected incoming call'
  showCallPopup.value = false
  if (showSmallCallWindow.value == undefined) {
    showSmallCallWindow = false
  } else {
    showSmallCallWindow.value = false
  }
  callStatus.value = ''
  muted.value = false
}


function hangUpCall() {
  if (activeSession.state == "Established") {
    activeSession.bye().catch((error) => {});
  } else {
    activeSession.cancel().catch((error) => {});
  }
  log.value = 'Hanging up incoming call'
  onCall.value = false
  callStatus.value = ''
  muted.value = false
  note.value = {
    title: '',
    content: '',
  }
  counterUp.value.stop()
}

function handleDisconnectedIncomingCall() {
  log.value = `Call ended from handle disconnected Incoming call.`
  showCallPopup.value = false
  if (showSmallCallWindow.value == undefined) {
    showSmallCallWindow = false
  } else {
    showSmallCallWindow.value = false
  }
  _call = null
  muted.value = false
  onCall.value = false
  counterUp.value.stop()
}

async function makeOutgoingCall(number) {
  // check if number has a country code
  // if (number?.replace(/[^0-9+]/g, '').length == 10) {
  //   $dialog({
  //     title: 'Invalid Mobile Number',
  //     message: `${number} is not a valid mobile number. Either add a country code or check the number again.`,
  //   })
  //   return
  // }

  contact.value = getContact(number)
  if (!contact.value) {
    contact.value = getLeadContact(number)
  }

  if (device) {
    log.value = `Attempting to call ${number} ...`

    try {
      _call = await device.connect({
        params: { To: number },
      })

      showCallPopup.value = true
      callStatus.value = 'initiating'

      _call.on('messageReceived', (message) => {
        let info = message.content
        callStatus.value = info.CallStatus

        log.value = `Call status: ${info.CallStatus}`

        if (info.CallStatus == 'in-progress') {
          log.value = `Call in progress.`
          calling.value = false
          onCall.value = true
          counterUp.value.start()
        }
      })

      _call.on('accept', () => {
        log.value = `Initiated call!`
        showCallPopup.value = true
        calling.value = true
        onCall.value = false
      })
      _call.on('disconnect', (conn) => {
        log.value = `Call ended from makeOutgoing call disconnect.`
        calling.value = false
        onCall.value = false
        showCallPopup.value = false
        showSmallCallWindow = false
        _call = null
        callStatus.value = ''
        muted.value = false
        counterUp.value.stop()
        note.value = {
          title: '',
          content: '',
        }
      })
      _call.on('cancel', () => {
        log.value = `Call ended from makeOutgoing call cancel.`
        calling.value = false
        onCall.value = false
        showCallPopup.value = false
        showSmallCallWindow = false
        _call = null
        callStatus.value = ''
        muted.value = false
        note.value = {
          title: '',
          content: '',
        }
        counterUp.value.stop()
      })
    } catch (error) {
      log.value = `Could not connect call: ${error.message}`
    }
  } else {
    log.value = 'Unable to make call.'
  }
}

function cancelCall() {
  _call.disconnect()
  showCallPopup.value = false
  if (showSmallCallWindow.value == undefined) {
    showSmallCallWindow = false
  } else {
    showSmallCallWindow.value = false
  }
  calling.value = false
  onCall.value = false
  callStatus.value = ''
  muted.value = false
  note.value = {
    title: '',
    content: '',
  }
}

function toggleCallWindow() {
  showCallPopup.value = !showCallPopup.value
  if (showSmallCallWindow.value == undefined) {
    showSmallCallWindow = !showSmallCallWindow
  } else {
    showSmallCallWindow.value = !showSmallCallWindow.value
  }
}
function cleanupMedia() {
  let mediaElement = document.getElementById("remoteAudio");
  mediaElement.srcObject = null;
  mediaElement.pause();
}

function audioConfig(inviter) {
  const mediaElement = document.getElementById('remoteAudio')
  const remoteStream = new MediaStream()
    inviter.sessionDescriptionHandler.peerConnection
        .getReceivers().forEach((receiver) => {
          if (receiver.track) {
            remoteStream.addTrack(receiver.track)
          }
        })
    mediaElement.srcObject = remoteStream
    mediaElement.play()
    inviter.sessionDescriptionHandler.peerConnection
      .getReceivers()
      .forEach((receiver) => {
        if (receiver.track) {
          remoteStream.addTrack(receiver.track)
        }
      });
}


onMounted(async () => {
  enabled && startupClient()
  setMakeCall(makeOutgoingCall)
  window.addEventListener('callEvent', function(e) {
    console.log(e.detail.importantData);
  })
})

watch(
  () => log.value,
  (value) => {
    console.log(value)
  },
  { immediate: true }
)
</script>

<style scoped>
.pulse::before {
  content: '';
  position: absolute;
  border: 1px solid green;
  width: calc(100% + 20px);
  height: calc(100% + 20px);
  border-radius: 50%;
  animation: pulse 1s linear infinite;
}

.pulse::after {
  content: '';
  position: absolute;
  border: 1px solid green;
  width: calc(100% + 20px);
  height: calc(100% + 20px);
  border-radius: 50%;
  animation: pulse 1s linear infinite;
  animation-delay: 0.3s;
}

@keyframes pulse {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }

  50% {
    transform: scale(1);
    opacity: 1;
  }

  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}
</style>

