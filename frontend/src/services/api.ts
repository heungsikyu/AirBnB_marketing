import axios from 'axios'
import { DashboardStats, SystemStatus, Property, AnalyticsData, Settings } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 대시보드 API
export const dashboardApi = {
  getStats: (): Promise<DashboardStats> => 
    api.get('/dashboard/stats').then(res => res.data),
  
  getSystemStatus: (): Promise<SystemStatus> => 
    api.get('/dashboard/system-status').then(res => res.data),
  
  startSystem: () => 
    api.post('/dashboard/start').then(res => res.data),
  
  stopSystem: () => 
    api.post('/dashboard/stop').then(res => res.data),
  
  getRecentActivities: () => 
    api.get('/dashboard/recent-activities').then(res => res.data),
}

// 숙소 관리 API
export const propertiesApi = {
  getProperties: (params?: {
    page?: number
    limit?: number
    city?: string
    status?: string
    search?: string
  }) => 
    api.get('/properties', { params }).then(res => res.data),
  
  getProperty: (id: string): Promise<Property> => 
    api.get(`/properties/${id}`).then(res => res.data),
  
  toggleProperty: (id: string) => 
    api.post(`/properties/${id}/toggle`).then(res => res.data),
  
  deleteProperty: (id: string) => 
    api.delete(`/properties/${id}`).then(res => res.data),
  
  getCitiesList: (): Promise<string[]> => 
    api.get('/properties/cities/list').then(res => res.data),
  
  getPropertiesSummary: () => 
    api.get('/properties/stats/summary').then(res => res.data),
}

// 분석 API
export const analyticsApi = {
  getOverview: (days: number = 30): Promise<AnalyticsData> => 
    api.get('/analytics/overview', { params: { days } }).then(res => res.data),
  
  getPerformance: (days: number = 30) => 
    api.get('/analytics/performance', { params: { days } }).then(res => res.data),
  
  getTrends: (days: number = 30) => 
    api.get('/analytics/trends', { params: { days } }).then(res => res.data),
  
  exportData: (format: 'json' | 'csv', days: number = 30) => 
    api.get('/analytics/export', { params: { format, days } }).then(res => res.data),
}

// 알림 API
export const notificationsApi = {
  getNotifications: (limit: number = 50) => 
    api.get('/notifications', { params: { limit } }).then(res => res.data),
  
  markAsRead: (id: string) => 
    api.post(`/notifications/${id}/read`).then(res => res.data),
  
  markAllAsRead: () => 
    api.post('/notifications/mark-all-read').then(res => res.data),
  
  getStats: () => 
    api.get('/notifications/stats').then(res => res.data),
  
  getSettings: () => 
    api.get('/notifications/settings').then(res => res.data),
  
  updateSettings: (settings: any) => 
    api.post('/notifications/settings', settings).then(res => res.data),
}

// 설정 API
export const settingsApi = {
  getSettings: (): Promise<Settings> => 
    api.get('/settings').then(res => res.data),
  
  updateSettings: (settings: Partial<Settings>) => 
    api.post('/settings', settings).then(res => res.data),
  
  getApiKeys: () => 
    api.get('/settings/api-keys').then(res => res.data),
  
  updateApiKeys: (apiKeys: Record<string, string>) => 
    api.post('/settings/api-keys', apiKeys).then(res => res.data),
  
  testConnection: (service: string) => 
    api.post('/settings/test-connection', { service }).then(res => res.data),
  
  getSystemInfo: () => 
    api.get('/settings/system-info').then(res => res.data),
  
  createBackup: () => 
    api.post('/settings/backup').then(res => res.data),
  
  restoreBackup: (backupFile: string) => 
    api.post('/settings/restore', { backup_file: backupFile }).then(res => res.data),
}

export default api
