import React from 'react'
import { Settings as SettingsIcon } from 'lucide-react'

const Settings: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">설정</h1>
        <p className="mt-2 text-gray-600">
          시스템 설정을 관리하세요
        </p>
      </div>
      
      <div className="text-center py-12">
        <SettingsIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">설정 페이지</h3>
        <p className="mt-1 text-sm text-gray-500">
          설정 기능이 곧 추가될 예정입니다.
        </p>
      </div>
    </div>
  )
}

export default Settings
