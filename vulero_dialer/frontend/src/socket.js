//import { io } from 'socket.io-client'
//import { socketio_port } from '../../../../sites/common_site_config.json'

//function initSocket() {
//  let host = window.location.hostname
//  let port = window.location.port ? `:${socketio_port}` : ''
//  let protocol = port ? 'http' : 'https'
//  let url = `${protocol}://${host}${port}/${host}`
//  let socket = io(url, { withCredentials: true })
//  return socket
//}

//let socket = initSocket()
let socket = null;
export default socket
