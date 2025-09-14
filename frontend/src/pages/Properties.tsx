import React, { useState, useEffect } from 'react'
import { 
  Search, 
  Filter, 
  Eye, 
  ToggleLeft, 
  ToggleRight,
  Trash2,
  Building2,
  Star,
  Users,
  MapPin
} from 'lucide-react'
import { propertiesApi } from '../services/api'
import { Property } from '../types'

const Properties: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({
    city: '',
    status: 'all',
    search: ''
  })
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 20,
    total: 0,
    pages: 0
  })
  const [cities, setCities] = useState<string[]>([])

  useEffect(() => {
    fetchProperties()
    fetchCities()
  }, [filters, pagination.page])

  const fetchProperties = async () => {
    try {
      setLoading(true)
      const response = await propertiesApi.getProperties({
        page: pagination.page,
        limit: pagination.limit,
        ...filters
      })
      setProperties(response.properties)
      setPagination(response.pagination)
    } catch (error) {
      console.error('숙소 목록 로딩 실패:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCities = async () => {
    try {
      const citiesList = await propertiesApi.getCitiesList()
      setCities(citiesList)
    } catch (error) {
      console.error('도시 목록 로딩 실패:', error)
    }
  }

  const handleToggleProperty = async (propertyId: string) => {
    try {
      await propertiesApi.toggleProperty(propertyId)
      fetchProperties() // 목록 새로고침
    } catch (error) {
      console.error('숙소 상태 변경 실패:', error)
    }
  }

  const handleDeleteProperty = async (propertyId: string) => {
    if (window.confirm('정말로 이 숙소를 삭제하시겠습니까?')) {
      try {
        await propertiesApi.deleteProperty(propertyId)
        fetchProperties() // 목록 새로고침
      } catch (error) {
        console.error('숙소 삭제 실패:', error)
      }
    }
  }

  const PropertyCard: React.FC<{ property: Property }> = ({ property }) => (
    <div className="card">
      <div className="card-content p-6">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{property.title}</h3>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                property.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {property.is_active ? '활성' : '비활성'}
              </div>
            </div>
            
            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
              <div className="flex items-center">
                <MapPin className="h-4 w-4 mr-1" />
                {property.city}
              </div>
              <div className="flex items-center">
                <Star className="h-4 w-4 mr-1" />
                {property.rating}/5
              </div>
              <div className="flex items-center">
                <Users className="h-4 w-4 mr-1" />
                {property.max_guests}명
              </div>
            </div>
            
            <div className="text-lg font-bold text-primary mb-2">
              {property.price_per_night.toLocaleString()}원/박
            </div>
            
            <div className="flex flex-wrap gap-1 mb-3">
              {property.amenities.slice(0, 3).map((amenity, index) => (
                <span 
                  key={index}
                  className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                >
                  {amenity}
                </span>
              ))}
              {property.amenities.length > 3 && (
                <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                  +{property.amenities.length - 3}개
                </span>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleToggleProperty(property.id)}
              className="p-2 text-gray-400 hover:text-gray-600"
              title={property.is_active ? '비활성화' : '활성화'}
            >
              {property.is_active ? (
                <ToggleRight className="h-5 w-5 text-green-500" />
              ) : (
                <ToggleLeft className="h-5 w-5 text-gray-400" />
              )}
            </button>
            
            <button className="p-2 text-gray-400 hover:text-gray-600" title="상세보기">
              <Eye className="h-5 w-5" />
            </button>
            
            <button
              onClick={() => handleDeleteProperty(property.id)}
              className="p-2 text-gray-400 hover:text-red-600"
              title="삭제"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">숙소 관리</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          등록된 숙소를 관리하고 상태를 제어하세요
        </p>
      </div>

      {/* 필터 */}
      <div className="card">
        <div className="card-content p-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                검색
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="숙소명, 도시 검색..."
                  value={filters.search}
                  onChange={(e) => setFilters({...filters, search: e.target.value})}
                  className="w-full pl-10 pr-3 py-2 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:border-transparent dark:bg-gray-700 dark:text-gray-100 dark:placeholder-gray-400"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                도시
              </label>
              <select
                value={filters.city}
                onChange={(e) => setFilters({...filters, city: e.target.value})}
                className="w-full px-3 py-2 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:border-transparent dark:bg-gray-700 dark:text-gray-100"
              >
                <option value="">모든 도시</option>
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                상태
              </label>
              <select
                value={filters.status}
                onChange={(e) => setFilters({...filters, status: e.target.value})}
                className="w-full px-3 py-2 border border-transparent rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent dark:border-transparent dark:bg-gray-700 dark:text-gray-100"
              >
                <option value="all">모든 상태</option>
                <option value="active">활성</option>
                <option value="inactive">비활성</option>
              </select>
            </div>
            
            <div className="flex items-end">
              <button
                onClick={fetchProperties}
                className="w-full btn btn-primary"
              >
                <Filter className="h-10 w-4 mr-2" />
                필터 적용
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 숙소 목록 */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : properties.length > 0 ? (
          properties.map(property => (
            <PropertyCard key={property.id} property={property} />
          ))
        ) : (
          <div className="text-center py-12">
            <Building2 className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">숙소가 없습니다</h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              검색 조건에 맞는 숙소를 찾을 수 없습니다.
            </p>
          </div>
        )}
      </div>

      {/* 페이지네이션 */}
      {pagination.pages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-700 dark:text-gray-300">
            총 {pagination.total}개 중 {((pagination.page - 1) * pagination.limit) + 1}-{Math.min(pagination.page * pagination.limit, pagination.total)}개 표시
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setPagination({...pagination, page: pagination.page - 1})}
              disabled={pagination.page === 1}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-transparent rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-transparent dark:text-gray-300 dark:hover:bg-gray-700"
            >
              이전
            </button>
            <span className="px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-transparent rounded-md dark:bg-gray-700 dark:border-transparent dark:text-gray-300">
              {pagination.page} / {pagination.pages}
            </span>
            <button
              onClick={() => setPagination({...pagination, page: pagination.page + 1})}
              disabled={pagination.page === pagination.pages}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-transparent rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-transparent dark:text-gray-300 dark:hover:bg-gray-700"
            >
              다음
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default Properties
