# AgroAI: Crop Prediction & Image Analysis

AgroAI is a smart agricultural platform designed to help farmers make data-driven decisions. By combining machine learning for crop yield prediction, computer vision for plant health analysis, and an AI chatbot for farming advice, AgroAI provides actionable, localized insights to maximize productivity and minimize crop loss.

## Features

- **Crop Yield Prediction**: Estimates crop yield using a trained XGBoost model, taking into account soil nutrients (N, P, K, pH), rainfall, and live weather data.
- **Disease & Health Analysis**: Upload leaf images to instantly detect signs of nitrogen deficiency, fungal diseases, or drought stress via OpenCV color ratio analysis.
- **Kisan Mitra Chatbot 🌾**: An intelligent, friendly farming assistant powered by Google's Gemini AI, answering agricultural questions in English, Hindi, and Hinglish.
- **Smart Recommendations**: Get actionable advice on fertilizer usage, pest control, and watering schedules based on real-time weather and soil inputs.
- **Multilingual Support**: Switch seamlessly between English and Hindi for a more inclusive user experience.

## Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, React Router, i18next
- **Backend**: FastAPI, Python, Pandas, NumPy
- **Machine Learning**: XGBoost (Yield Prediction), OpenCV (Image Processing)
- **AI Integration**: Google Generative AI (Gemini 2.0 Flash)
- **APIs**: OpenWeather API

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Rhythem2005/SIH-CROP-YIELD-.git
cd SIH-CROP-YIELD-
```

### 2. Set up the Backend
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
Create a `.env` file in the `server` folder using `.env.example` as a template, and fill in your API keys (OpenWeather, Gemini).

Start the FastAPI server:
```bash
uvicorn app:app --reload
```

### 3. Set up the Frontend
```bash
cd ../client
npm install
```
Create a `.env` file in the `client` folder and add:
```env
VITE_OPENWEATHER_KEY=your_openweather_key
VITE_API_URL=http://127.0.0.1:8000
```

Start the React development server:
```bash
npm run dev
```

## Environment Variables

### Backend (`server/.env`)
- `GEMINI_KEY`: Google Gemini API key for the Chatbot.
- `OPENWEATHER_KEY`: OpenWeather API key for fetching live weather data during predictions.
- `ALLOWED_ORIGINS`: CORS domains (e.g., `http://localhost:5174,https://your-frontend.vercel.app`).

### Frontend (`client/.env`)
- `VITE_OPENWEATHER_KEY`: Weather API key used by frontend components.
- `VITE_API_URL`: Target URL for backend API calls.

## Deployment

- **Backend (Render)**: Deployed automatically using the `Procfile` and `requirements.txt`. Live URL: `https://sih-crop-yield-1.onrender.com`
- **Frontend (Vercel)**: Connect the repository to Vercel and ensure the build command is `npm run build` and output directory is `dist`. Set `VITE_API_URL` to the Render backend URL in Vercel's environment variables.

## API Endpoints

- `POST /predict_yield`: Accepts soil and crop data to return yield estimates and fertilizer recommendations.
- `POST /analyze_crop_image`: Accepts an uploaded image of a leaf and returns a health score and disease diagnosis.
- `POST /api/chat`: Communicates with the Gemini AI chatbot to answer farming queries.

## Notes & Limitations

- The authentication system is currently bypassed for faster access and testing.
- The `crop_yield_model.json` must be present in the `server` root directory for predictions to work.
- Image analysis relies on color mapping (HSV ratios) rather than a deep learning convolution network. It's an approximation meant for quick, accessible checks.
