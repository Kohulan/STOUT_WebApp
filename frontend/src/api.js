import axios from 'axios'

const apiUrl =
  process.env.NODE_ENV === 'production'
    ? window.APP_CONFIG.API_URL || 'http://backend:3000' // Modify here
    : process.env.VUE_APP_API_URL

const apiClient = axios.create({
  baseURL: apiUrl,
})

export default apiClient
