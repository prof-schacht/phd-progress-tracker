// API Service Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api'

export const apiClient = {
  baseURL: API_BASE_URL,
  
  // Basic fetch wrapper with error handling
  async fetch(endpoint: string, options?: RequestInit) {
    const url = `${this.baseURL}${endpoint}`
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      })
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API Request failed:', error)
      throw error
    }
  },
  
  // Convenience methods
  get(endpoint: string) {
    return this.fetch(endpoint, { method: 'GET' })
  },
  
  post(endpoint: string, data: any) {
    return this.fetch(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },
  
  put(endpoint: string, data: any) {
    return this.fetch(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },
  
  delete(endpoint: string) {
    return this.fetch(endpoint, { method: 'DELETE' })
  },
}

// Health check function
export const checkApiHealth = async () => {
  try {
    const response = await apiClient.get('/health')
    return response
  } catch (error) {
    console.error('Health check failed:', error)
    return { status: 'error', error }
  }
}