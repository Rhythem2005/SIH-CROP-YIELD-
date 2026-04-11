// api config
// Clean trailing slash if it exists
export const API_BASE_URL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace(/\/$/, "") : "";

export const API_ENDPOINTS = {
  CHAT: `${API_BASE_URL}/api/chat`,
  PREDICT_YIELD: `${API_BASE_URL}/predict_yield`,
  ANALYZE_IMAGE: `${API_BASE_URL}/analyze_crop_image`,
};
