export interface DashboardStats {
  totalProperties: number
  activeProperties: number
  totalPosts: number
  successfulPosts: number
  failedPosts: number
  totalClicks: number
  totalConversions: number
  conversionRate: number
  errorCount: number
  successRate: number
}

export interface SystemStatus {
  isRunning: boolean
  lastExecution: string
  nextExecution: string
  activeWorkflows: string[]
  errorCount: number
  uptime: string
}

export interface Property {
  id: string
  title: string
  city: string
  price_per_night: number
  rating: number
  max_guests: number
  bedrooms: number
  bathrooms: number
  amenities: string[]
  images: string[]
  is_active: boolean
  created_at: string
  scraped_at: string
}

export interface PostingHistory {
  id: number
  property_id: string
  platform: string
  post_id: string
  post_url: string
  status: 'success' | 'failed' | 'pending'
  error_message?: string
  posted_at: string
  analytics_data: any
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  timestamp: string
  property_id?: string
  read: boolean
}

export interface Activity {
  type: 'post' | 'property_added' | 'error' | 'system'
  message: string
  status: 'success' | 'error' | 'warning' | 'info'
  timestamp: string
  property_id?: string
}

export interface AnalyticsData {
  period: string
  totalPosts: number
  successfulPosts: number
  failedPosts: number
  successRate: number
  totalClicks: number
  totalConversions: number
  conversionRate: number
  dailyStats: Record<string, {
    posts: number
    success: number
    error: number
  }>
  platformStats: Record<string, {
    posts: number
    success: number
    error: number
  }>
}

export interface Settings {
  postingSchedule: string[]
  targetCities: string[]
  contentSettings: {
    maxTitleLength: number
    maxDescriptionLength: number
    hashtagLimit: number
    imageQuality: number
    maxImageSize: [number, number]
  }
  socialMediaSettings: {
    instagram: {
      maxCaptionLength: number
      maxHashtags: number
      storyDuration: number
      reelsDuration: number
    }
    youtube: {
      maxTitleLength: number
      maxDescriptionLength: number
      maxTags: number
      shortsDuration: number
    }
    blog: {
      maxTitleLength: number
      minContentLength: number
      maxContentLength: number
      maxTags: number
    }
  }
  notificationSettings: {
    emailNotifications: boolean
    pushNotifications: boolean
    notificationTypes: {
      postSuccess: boolean
      postError: boolean
      systemAlert: boolean
      dailyReport: boolean
    }
  }
}
