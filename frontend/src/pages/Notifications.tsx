import React, { useState, useEffect } from 'react'
import { 
  Bell, 
  CheckCircle, 
  AlertCircle, 
  Info, 
  Filter,
  Check,
  Settings
} from 'lucide-react'
import { notificationsApi } from '../services/api'
import { Notification } from '../types'

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'unread' | 'success' | 'error'>('all')

  useEffect(() => {
    fetchNotifications()
  }, [filter])

  const fetchNotifications = async () => {
    try {
      setLoading(true)
      const response = await notificationsApi.getNotifications(100)
      let filteredNotifications = response.notifications || []
      
      if (filter === 'unread') {
        filteredNotifications = filteredNotifications.filter((n: any) => !n.read)
      } else if (filter !== 'all') {
        filteredNotifications = filteredNotifications.filter((n: any) => n.type === filter)
      }
      
      setNotifications(filteredNotifications)
    } catch (error) {
      console.error('알림 목록 로딩 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleMarkAsRead = async (notificationId: string) => {
    try {
      await notificationsApi.markAsRead(notificationId)
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? {...n, read: true} : n)
      )
    } catch (error) {
      console.error('알림 읽음 처리 실패:', error)
    }
  }

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsApi.markAllAsRead()
      setNotifications(prev => prev.map(n => ({...n, read: true})))
    } catch (error) {
      console.error('모든 알림 읽음 처리 실패:', error)
    }
  }

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />
      default:
        return <Info className="h-5 w-5 text-blue-500" />
    }
  }

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'success':
        return 'border-l-green-500 bg-green-50'
      case 'error':
        return 'border-l-red-500 bg-red-50'
      case 'warning':
        return 'border-l-yellow-500 bg-yellow-50'
      default:
        return 'border-l-blue-500 bg-blue-50'
    }
  }

  const NotificationItem: React.FC<{ notification: Notification }> = ({ notification }) => (
    <div className={`border-l-4 ${getNotificationColor(notification.type)} ${
      notification.read ? 'opacity-60' : ''
    }`}>
      <div className="bg-white p-4 shadow-sm">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {getNotificationIcon(notification.type)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <h4 className="text-sm font-medium text-gray-900">
                  {notification.title}
                </h4>
                {!notification.read && (
                  <div className="h-2 w-2 bg-primary rounded-full"></div>
                )}
              </div>
              <p className="mt-1 text-sm text-gray-600">
                {notification.message}
              </p>
              <p className="mt-1 text-xs text-gray-500">
                {new Date(notification.timestamp).toLocaleString()}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {!notification.read && (
              <button
                onClick={() => handleMarkAsRead(notification.id)}
                className="p-1 text-gray-400 hover:text-gray-600"
                title="읽음 처리"
              >
                <Check className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )

  const unreadCount = notifications.filter(n => !n.read).length

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">알림</h1>
          <p className="mt-2 text-gray-600">
            시스템 알림과 활동 내역을 확인하세요
          </p>
        </div>
        <div className="flex items-center space-x-2">
          {unreadCount > 0 && (
            <button
              onClick={handleMarkAllAsRead}
              className="btn btn-outline btn-sm"
            >
              <Check className="h-4 w-4 mr-2" />
              모두 읽음 처리
            </button>
          )}
          <button className="btn btn-outline btn-sm">
            <Settings className="h-4 w-4 mr-2" />
            설정
          </button>
        </div>
      </div>

      {/* 필터 */}
      <div className="card">
        <div className="card-content p-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">필터:</span>
            </div>
            <div className="flex space-x-2">
              {[
                { key: 'all', label: '전체', count: notifications.length },
                { key: 'unread', label: '읽지 않음', count: unreadCount },
                { key: 'success', label: '성공', count: notifications.filter(n => n.type === 'success').length },
                { key: 'error', label: '오류', count: notifications.filter(n => n.type === 'error').length }
              ].map(({ key, label, count }) => (
                <button
                  key={key}
                  onClick={() => setFilter(key as any)}
                  className={`px-3 py-1 text-sm font-medium rounded-full ${
                    filter === key
                      ? 'bg-primary text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {label} ({count})
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 알림 목록 */}
      <div className="space-y-2">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : notifications.length > 0 ? (
          notifications.map(notification => (
            <NotificationItem key={notification.id} notification={notification} />
          ))
        ) : (
          <div className="text-center py-12">
            <Bell className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">알림이 없습니다</h3>
            <p className="mt-1 text-sm text-gray-500">
              {filter === 'unread' 
                ? '읽지 않은 알림이 없습니다.'
                : '알림이 없습니다.'
              }
            </p>
          </div>
        )}
      </div>

      {/* 통계 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="card-content p-4">
            <div className="flex items-center">
              <Bell className="h-8 w-8 text-blue-500" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">총 알림</p>
                <p className="text-2xl font-semibold text-gray-900">{notifications.length}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-content p-4">
            <div className="flex items-center">
              <div className="h-8 w-8 bg-red-100 rounded-full flex items-center justify-center">
                <div className="h-2 w-2 bg-red-500 rounded-full"></div>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">읽지 않음</p>
                <p className="text-2xl font-semibold text-gray-900">{unreadCount}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-content p-4">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-500" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">성공</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {notifications.filter(n => n.type === 'success').length}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="card-content p-4">
            <div className="flex items-center">
              <AlertCircle className="h-8 w-8 text-red-500" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">오류</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {notifications.filter(n => n.type === 'error').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Notifications
