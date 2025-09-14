import { io, Socket } from 'socket.io-client'

class WebSocketService {
  private socket: Socket | null = null
  private listeners: Map<string, Function[]> = new Map()

  connect() {
    if (this.socket?.connected) return

    this.socket = io('ws://localhost:8000', {
      transports: ['websocket'],
      autoConnect: true,
    })

    this.socket.on('connect', () => {
      console.log('WebSocket 연결됨')
      this.emit('connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket 연결 해제됨')
      this.emit('disconnected')
    })

    this.socket.on('notification', (data) => {
      console.log('알림 수신:', data)
      this.emit('notification', data)
    })

    this.socket.on('system_update', (data) => {
      console.log('시스템 업데이트:', data)
      this.emit('system_update', data)
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket 오류:', error)
      this.emit('error', error)
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)!.push(callback)
  }

  off(event: string, callback: Function) {
    const listeners = this.listeners.get(event)
    if (listeners) {
      const index = listeners.indexOf(callback)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    }
  }

  private emit(event: string, data?: any) {
    const listeners = this.listeners.get(event)
    if (listeners) {
      listeners.forEach(callback => callback(data))
    }
  }

  send(event: string, data?: any) {
    if (this.socket?.connected) {
      this.socket.emit(event, data)
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false
  }
}

export const wsService = new WebSocketService()
export default wsService
