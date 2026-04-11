// api config
export const API_BASE_URL = 
  import.meta.env.MODE === 'production'
    ? import.meta.env.VITE_API_BASE_URL || window.location.origin
    : 'http://localhost:8000';

export const API_ENDPOINTS = {
  CHAT: `${API_BASE_URL}/api/chat`,
  PREDICT_YIELD: `${API_BASE_URL}/predict_yield`,
  ANALYZE_IMAGE: `${API_BASE_URL}/analyze_crop_image`,
};
