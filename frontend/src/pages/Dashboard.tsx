import React, { useState, useEffect } from 'react'
import { 
  Building2, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle, 
  Clock,
  DollarSign,
  Activity
} from 'lucide-react'
import { dashboardApi } from '../services/api'
import { DashboardStats, SystemStatus, Activity as ActivityType } from '../types'

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [activities, setActivities] = useState<ActivityType[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [statsData, systemData, activitiesData] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getSystemStatus(),
        dashboardApi.getRecentActivities()
      ])
      
      setStats(statsData)
      setSystemStatus(systemData)
      setActivities(activitiesData.activities || [])
    } catch (error) {
      console.error('대시보드 데이터 로딩 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const StatCard: React.FC<{
    title: string
    value: string | number
    subtitle?: string
    icon: React.ReactNode
    color: 'primary' | 'success' | 'warning' | 'error'
  }> = ({ title, value, subtitle, icon, color }) => {
    const colorClasses = {
      primary: 'bg-blue-500 text-white',
      success: 'bg-green-500 text-white',
      warning: 'bg-yellow-500 text-white',
      error: 'bg-red-500 text-white'
    }

    return (
      <div className="card">
        <div className="card-content p-6">
          <div className="flex items-center">
            <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
              {icon}
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{title}</p>
              <p className="text-2xl font-semibold text-gray-900">{value}</p>
              {subtitle && (
                <p className="text-sm text-gray-500">{subtitle}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">대시보드</h1>
        <p className="mt-2 text-gray-600">
          Airbnb 마케팅 자동화 시스템 현황을 확인하세요
        </p>
      </div>

      {/* 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="총 숙소"
          value={stats?.totalProperties || 0}
          subtitle={`활성: ${stats?.activeProperties || 0}`}
          icon={<Building2 className="h-6 w-6" />}
          color="primary"
        />
        
        <StatCard
          title="총 게시"
          value={stats?.totalPosts || 0}
          subtitle={`성공: ${stats?.successfulPosts || 0} | 실패: ${stats?.failedPosts || 0}`}
          icon={<TrendingUp className="h-6 w-6" />}
          color="success"
        />
        
        <StatCard
          title="전환율"
          value={`${(stats?.conversionRate || 0).toFixed(1)}%`}
          subtitle={`클릭: ${stats?.totalClicks || 0} | 전환: ${stats?.totalConversions || 0}`}
          icon={<DollarSign className="h-6 w-6" />}
          color="warning"
        />
        
        <StatCard
          title="성공률"
          value={`${(stats?.successRate || 0).toFixed(1)}%`}
          subtitle={`오류: ${stats?.errorCount || 0}건`}
          icon={<Activity className="h-6 w-6" />}
          color="error"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 시스템 상태 */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">시스템 상태</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">실행 상태</span>
                <div className="flex items-center gap-x-2">
                  <div className={`h-2 w-2 rounded-full ${systemStatus?.isRunning ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="text-sm text-gray-900">
                    {systemStatus?.isRunning ? '실행 중' : '중지됨'}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">마지막 실행</span>
                <span className="text-sm text-gray-900">
                  {systemStatus?.lastExecution ? 
                    new Date(systemStatus.lastExecution).toLocaleString() : 
                    '정보 없음'
                  }
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">다음 실행</span>
                <span className="text-sm text-gray-900">
                  {systemStatus?.nextExecution ? 
                    new Date(systemStatus.nextExecution).toLocaleString() : 
                    '정보 없음'
                  }
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-600">가동 시간</span>
                <span className="text-sm text-gray-900">{systemStatus?.uptime || '정보 없음'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* 최근 활동 */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">최근 활동</h3>
          </div>
          <div className="card-content">
            <div className="space-y-3">
              {activities.length > 0 ? (
                activities.slice(0, 5).map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className={`flex-shrink-0 w-2 h-2 rounded-full mt-2 ${
                      activity.status === 'success' ? 'bg-green-500' :
                      activity.status === 'error' ? 'bg-red-500' :
                      activity.status === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">{activity.message}</p>
                      <p className="text-xs text-gray-500">
                        {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-sm text-gray-500">최근 활동이 없습니다.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 빠른 액션 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">빠른 액션</h3>
        </div>
        <div className="card-content">
          <div className="flex space-x-4">
            <button className="btn btn-primary">
              <CheckCircle className="h-4 w-4 mr-2" />
              시스템 시작
            </button>
            <button className="btn btn-outline">
              <AlertCircle className="h-4 w-4 mr-2" />
              시스템 중지
            </button>
            <button className="btn btn-outline">
              <Clock className="h-4 w-4 mr-2" />
              수동 실행
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
