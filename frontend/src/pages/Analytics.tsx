import React from 'react'
import { BarChart3 } from 'lucide-react'

const Analytics: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">분석</h1>
        <p className="mt-2 text-gray-600">
          성과 분석 및 트렌드를 확인하세요
        </p>
      </div>
      
      <div className="text-center py-12">
        <BarChart3 className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">분석 페이지</h3>
        <p className="mt-1 text-sm text-gray-500">
          분석 기능이 곧 추가될 예정입니다.
        </p>
      </div>
    </div>
  )
}

export default Analytics
