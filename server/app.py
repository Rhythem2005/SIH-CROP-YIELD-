from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
# [AUTH DISABLED] from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
import pandas as pd
import numpy as np
import xgboost as xgb
import cv2
import tempfile
import warnings
import httpx
import os
import random   # ✅ NEW
import google.generativeai as genai  # ✅ Gemini API
from dotenv import load_dotenv  # ✅ Load env vars

load_dotenv()  # ✅ Load .env file

# Local imports (keep these files as they are in your project)
# [AUTH DISABLED] from database import users_collection
# [AUTH DISABLED] from auth import get_password_hash, verify_password, create_access_token, verify_token
# [AUTH DISABLED] import schemas

warnings.filterwarnings("ignore")

app = FastAPI(title="Crop Prediction & Image Analysis API")

# ==============================
# CORS Middleware
# ==============================
# Allow localhost for development, and production frontend URL
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5174,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Gemini AI Setup
# ==============================
GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    print("Warning: GEMINI_KEY not found in .env file. Chatbot will be disabled.")
    gemini_model = None

# ==============================
# Load ML Model
# ==============================
try:
    model = xgb.Booster()
    model.load_model("crop_yield_model.json")
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: 'crop_yield_model.json' not found. Place it in the project folder.")
    raise

# [AUTH DISABLED] OAuth2 scheme
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ==============================
# [AUTH DISABLED] Auth Routes — commented out, not deleted
# ==============================
# @app.post("/signup")
# async def signup(user: schemas.SignupModel):
#     existing_user = await users_collection.find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
# 
#     hashed_password = get_password_hash(user.password)
#     user_dict = user.dict()
#     user_dict["password"] = hashed_password
# 
#     await users_collection.insert_one(user_dict)
#     return {"message": "User created successfully"}
# 
# 
# @app.post("/login")
# async def login(user: schemas.LoginModel):
#     db_user = await users_collection.find_one({"email": user.email})
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials"}
#     
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(
#         data={"sub": db_user["email"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
# 
# 
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
# 
#     email: str = payload.get("sub")
#     user = await users_collection.find_one({"email": email})
#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user

# ==============================
# Weather Integration
# ==============================
STATE_TO_CITY = {
    "Uttar Pradesh": "Lucknow",
    "Maharashtra": "Mumbai",
    "Punjab": "Chandigarh",
    "Karnataka": "Bengaluru",
    "Tamil Nadu": "Chennai",
    "Delhi": "Delhi",
    # Add more states if needed
}

OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")

async def fetch_weather(state: str):
    city = STATE_TO_CITY.get(state, state)
    if not OPENWEATHER_KEY:
        return {"Temp": 25, "Humidity": 60, "Rainfall": 500}  # fallback

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            data = resp.json()

        if data.get("cod") != 200:
            return {"Temp": 25, "Humidity": 60, "Rainfall": 500}

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rainfall = data.get("rain", {}).get("1h") or data.get("rain", {}).get("3h") or 0

        return {"Temp": temp, "Humidity": humidity, "Rainfall": rainfall}

    except Exception as e:
        print("Weather fetch failed:", e)
        return {"Temp": 25, "Humidity": 60, "Rainfall": 500}

# ==============================
# Yield Prediction
# ==============================
class YieldInput(BaseModel):
    Crop: str
    State: str
    Year: int
    N: float
    P: float
    K: float
    pH: float
    soil_type: str
    Fertilizer_Type: str
    Fertilizer_Amount: float
    Pesticide_Amount: float
    sowing_date: str
    area: float

# ==============================
# Chatbot Models & Routes
# ==============================
class ChatMessage(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(chat_input: ChatMessage):
    """Handle chatbot requests - forward to Gemini API"""
    if not gemini_model:
        return JSONResponse(
            content={"error": "Chatbot service is not available. API key not configured."},
            status_code=503
        )
    
    try:
        prompt = f"""
You are a friendly Indian farmer assistant named "Kisan Mitra 🌾".
Answer ONLY agriculture or farming related questions.
Answer in English if user types in English, answer in Hindi if user types in Hindi or Hinglish.
Be very friendly and helpful, like a senior farmer advising a junior.
Keep answers concise and easy to understand.

User Question:
{chat_input.message}
"""
        # ✅ ADDED: Minimal error handling for Gemini API calls
        try:
            response = gemini_model.generate_content(prompt)
        except Exception as gemini_error:
            # ✅ ADDED: Log the error for debugging
            print(f"Error calling Gemini API: {gemini_error}")
            # ✅ ADDED: Return safe fallback response instead of error details
            return JSONResponse(
                content={"response": "AI service temporarily unavailable. Please try again later."},
                status_code=503
            )
        
        bot_response = response.text.strip() if response.text else "Maaf kijiye, iska jawab mujhe abhi nahi pata. 😅"
        
        return {
            "success": True,
            "response": bot_response
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return JSONResponse(
            content={
                "success": False,
                "error": "Could not generate response",
                "details": str(e)
            },
            status_code=500
        )

@app.post("/predict_yield")
async def predict_yield_api(data: YieldInput):
    input_data = data.dict()

    try:
        # Fetch live weather
        weather_data = await fetch_weather(input_data["State"])
        Temp = weather_data["Temp"]
        Humidity = weather_data["Humidity"]
        Rainfall = weather_data["Rainfall"]

        df_input = pd.DataFrame([input_data])

        categorical_cols = ['Crop', 'State', 'soil_type', 'Fertilizer_Type']
        for col in categorical_cols:
            df_input[col] = df_input[col].astype('category').cat.codes

        if 'sowing_date' in df_input.columns:
            df_input = df_input.drop(columns=['sowing_date'])

        dmatrix = xgb.DMatrix(df_input)
        predicted_yield = float(model.predict(dmatrix)[0])

        total_production_kg = predicted_yield * input_data["area"]
        total_production_tonnes = total_production_kg / 1000

        recommendations = []

        # ==============================
        # Nutrient Recommendations
        # ==============================
        if input_data["N"] < 30:
            msgs = [
                "🌱 Nitrogen very low: Apply 25–30 kg/ha urea immediately.",
                "🌱 Severe nitrogen deficiency detected — add 25–30 kg/ha urea soon.",
                "🌱 Nitrogen levels are critically low, urgent urea application recommended."
            ]
            recommendations.append(random.choice(msgs))
        elif input_data["N"] < 50:
            msgs = [
                "🌱 Nitrogen low: Apply nitrogen-rich fertilizer like urea.",
                "🌱 Mild nitrogen shortage. Consider using urea or ammonium sulfate.",
                "🌱 Nitrogen is slightly low — boost with nitrogen fertilizer."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "🌱 Nitrogen levels are sufficient.",
                "🌱 Adequate nitrogen detected, no immediate action needed.",
                "🌱 Nitrogen supply is optimal — maintain current fertilization."
            ]
            recommendations.append(random.choice(msgs))

        if input_data["P"] < 15:
            msgs = [
                "🌿 Phosphorus very low: Apply 30–40 kg/ha DAP.",
                "🌿 Severe phosphorus deficiency — provide DAP urgently.",
                "🌿 Very low phosphorus detected. Apply 30–40 kg/ha phosphate fertilizer."
            ]
            recommendations.append(random.choice(msgs))
        elif input_data["P"] < 25:
            msgs = [
                "🌿 Phosphorus low: Consider additional phosphorus fertilizer.",
                "🌿 Mild phosphorus shortage observed. Top-up with phosphate fertilizer.",
                "🌿 Phosphorus slightly low — apply more DAP for balance."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "🌿 Phosphorus levels are sufficient.",
                "🌿 Adequate phosphorus detected, no action needed.",
                "🌿 Phosphorus levels are balanced — maintain current fertilization."
            ]
            recommendations.append(random.choice(msgs))

        if input_data["K"] < 20:
            msgs = [
                "🪴 Potassium very low: Apply 30–40 kg/ha MOP.",
                "🪴 Severe potassium deficiency detected, add muriate of potash.",
                "🪴 Very low potassium levels, apply MOP urgently."
            ]
            recommendations.append(random.choice(msgs))
        elif input_data["K"] < 35:
            msgs = [
                "🪴 Potassium low: Consider additional potassium fertilizer.",
                "🪴 Mild potassium shortage — add muriate of potash (MOP).",
                "🪴 Potassium is slightly low, top-up recommended."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "🪴 Potassium levels are sufficient.",
                "🪴 Adequate potassium detected.",
                "🪴 Potassium status is optimal — no adjustments required."
            ]
            recommendations.append(random.choice(msgs))

        # pH
        if input_data["pH"] < 6.0:
            msgs = [
                "🧪 Soil is acidic. Apply lime to raise pH and improve nutrient uptake.",
                "🧪 The soil shows acidity — consider liming to balance pH.",
                "🧪 Acidic soil detected. Add lime to improve nutrient absorption."
            ]
            recommendations.append(random.choice(msgs))
        elif input_data["pH"] > 7.5:
            msgs = [
                "🧪 Soil is alkaline. Add organic matter or gypsum to improve pH.",
                "🧪 High alkalinity detected — gypsum application recommended.",
                "🧪 Alkaline soil present. Use organic matter to rebalance pH."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "🧪 Soil pH is optimal.",
                "🧪 Balanced soil pH detected.",
                "🧪 Soil pH is within the healthy range."
            ]
            recommendations.append(random.choice(msgs))

        # Weather-based recommendations
        if Rainfall < 200:
            msgs = [
                "💧 Low rainfall detected. Irrigation is necessary.",
                "💧 Very little rainfall — ensure supplementary irrigation.",
                "💧 Insufficient rainfall, arrange irrigation support."
            ]
            recommendations.append(random.choice(msgs))
        elif Rainfall > 800:
            msgs = [
                "💧 High rainfall. Ensure proper drainage to avoid waterlogging.",
                "💧 Excess rainfall observed — maintain good field drainage.",
                "💧 Heavy rainfall detected, check for waterlogging issues."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "💧 Rainfall is adequate.",
                "💧 Rainfall levels are optimal for crop growth.",
                "💧 Adequate rainfall — irrigation adjustments not needed."
            ]
            recommendations.append(random.choice(msgs))

        if Temp > 35:
            msgs = [
                "☀️ High temperature: Use mulching/shading or plant heat-tolerant varieties.",
                "☀️ Extreme heat detected — provide shade or mulch for crops.",
                "☀️ High temperatures can stress crops, consider heat-tolerant seeds."
            ]
            recommendations.append(random.choice(msgs))
        elif Temp < 15:
            msgs = [
                "❄️ Low temperature: Protect crops from frost if applicable.",
                "❄️ Very cold conditions detected — cover young plants if possible.",
                "❄️ Low temperatures may harm crops — take protective measures."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "🌡️ Temperature is within optimal range.",
                "🌡️ Temperature levels are suitable for growth.",
                "🌡️ Current temperature is favorable for crops."
            ]
            recommendations.append(random.choice(msgs))

        if Humidity > 80:
            msgs = [
                "💦 High humidity: Monitor for fungal diseases and apply fungicides proactively.",
                "💦 Excess humidity may trigger fungal infections — take preventive steps.",
                "💦 Very humid conditions detected, keep watch for fungal outbreaks."
            ]
            recommendations.append(random.choice(msgs))
        elif Humidity < 50:
            msgs = [
                "💦 Low humidity: Use drip irrigation or maintain soil moisture.",
                "💦 Dry air detected — ensure consistent soil watering.",
                "💦 Low humidity may dry crops, maintain irrigation."
            ]
            recommendations.append(random.choice(msgs))
        else:
            msgs = [
                "💦 Humidity is within ideal range.",
                "💦 Balanced humidity observed.",
                "💦 Humidity levels are favorable for crops."
            ]
            recommendations.append(random.choice(msgs))

        # Fertilizer & Pesticide
        if input_data["Fertilizer_Amount"] < 50:
            msgs = [
                f"🌾 Fertilizer amount is low. Consider increasing {input_data['Fertilizer_Type']} fertilizer for optimal growth.",
                f"🌾 Low fertilizer detected — add more {input_data['Fertilizer_Type']} for better yield.",
                f"🌾 Insufficient fertilizer applied. Increase {input_data['Fertilizer_Type']} usage."
            ]
            recommendations.append(random.choice(msgs))
        if input_data["Pesticide_Amount"] < 5:
            msgs = [
                "🐛 Pesticide amount is low. Regular pest monitoring is recommended.",
                "🐛 Low pesticide use detected — ensure proper pest surveillance.",
                "🐛 Insufficient pesticide applied. Monitor crops closely."
            ]
            recommendations.append(random.choice(msgs))

        # Crop health status
        if predicted_yield > 80:
            crop_status = "Excellent"
            msgs = [
                "📊 Overall crop health is excellent. Maintain current practices.",
                "📊 Crops look excellent — continue with existing care.",
                "📊 Excellent yield potential — sustain present management."
            ]
            recommendations.append(random.choice(msgs))
        elif predicted_yield > 50:
            crop_status = "Moderate"
            msgs = [
                "📊 Overall crop health is moderate. Follow above recommendations for better yield.",
                "📊 Crop condition is moderate — improvements possible with adjustments.",
                "📊 Yield outlook is moderate. Apply suggested measures for improvement."
            ]
            recommendations.append(random.choice(msgs))
        else:
            crop_status = "Poor"
            msgs = [
                "📊 Overall crop health is poor. Immediate action required: optimize nutrients, irrigation, and pest control.",
                "📊 Crop condition is poor — urgent corrective action needed.",
                "📊 Very low crop health detected. Adjust fertilization, water, and pest management immediately."
            ]
            recommendations.append(random.choice(msgs))

        result = {
            "crop_name": input_data["Crop"],
            "location": input_data["State"],
            "area": input_data["area"],
            "weather": {
                "temperature": Temp,
                "humidity": Humidity,
                "description": "Data from API"},
            "predicted_yield_kgha": predicted_yield,
            "total_production_tonnes": total_production_tonnes,
            "recommendations": recommendations,
            "sowing_date": input_data["sowing_date"]
        }

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)



# ==============================
# Image Analysis
# ==============================
import random

# ==============================
# Image Analysis (Multiple Statements)
# ==============================
def analyze_crop_health_detailed(image_path, crop_type="Wheat"):
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Image not found!"}

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (256, 256))
    hsv = cv2.cvtColor(img_resized, cv2.COLOR_RGB2HSV)

    total_pixels = img_resized.shape[0] * img_resized.shape[1]

    green_mask = cv2.inRange(hsv, (25, 40, 40), (95, 255, 255))
    green_count = np.sum(green_mask > 0)

    yellow_mask = cv2.inRange(hsv, (20, 100, 100), (40, 255, 255))
    yellow_count = np.sum(yellow_mask > 0)

    brown_mask = cv2.inRange(hsv, (10, 50, 20), (20, 255, 100))
    brown_count = np.sum(brown_mask > 0)

    gray_mask = cv2.inRange(hsv, (0, 0, 40), (180, 50, 180))
    gray_count = np.sum(gray_mask > 0)

    # Ratios
    green_ratio = green_count / total_pixels
    yellow_ratio = yellow_count / total_pixels
    brown_ratio = brown_count / total_pixels
    gray_ratio = gray_count / total_pixels

    health_score = green_ratio * 100  

    analysis = {
        "crop_type": crop_type,
        "health_score_percent": round(health_score, 2),
        "leaf_conditions": {
            "healthy_green_percent": round(green_ratio * 100, 2),
            "yellow_leaves_percent": round(yellow_ratio * 100, 2),
            "brown_spots_percent": round(brown_ratio * 100, 2),
            "dry_gray_percent": round(gray_ratio * 100, 2)
        },
        "diagnosis": [],
        "recommendations": []
    }

    # --- Nitrogen deficiency (yellow) ---
    if yellow_ratio > 0.05:
        nitrogen_diag = [
            "Nitrogen deficiency detected (yellow leaves).",
            "Leaves show yellowing, likely from low nitrogen.",
            "Crop may be suffering from nitrogen stress.",
            "Yellowing leaves suggest nitrogen shortage.",
            "Signs of poor nitrogen nutrition are visible."
        ]
        nitrogen_reco = [
            "Apply nitrogen-rich fertilizer immediately (e.g., urea).",
            "Use ammonium nitrate or urea to restore nitrogen levels.",
            "Boost nitrogen with compost or organic fertilizer.",
            "Add nitrogenous fertilizer to improve leaf greenness.",
            "Supply additional nitrogen to avoid stunted growth."
        ]
        analysis["diagnosis"] += random.sample(nitrogen_diag, k=3)
        analysis["recommendations"] += random.sample(nitrogen_reco, k=3)

    # --- Disease / pest (brown) ---
    if brown_ratio > 0.02:
        disease_diag = [
            "Possible disease or pest attack (brown spots).",
            "Brown lesions may indicate fungal infection.",
            "Pest or disease stress detected on leaves.",
            "Spotted leaves suggest pathogen activity.",
            "Crop may be affected by pests or early blight."
        ]
        disease_reco = [
            "Apply suitable fungicide/pesticide for this crop.",
            "Spray approved fungicides and monitor regularly.",
            "Seek agri-expert advice for targeted pest control.",
            "Follow integrated pest management practices.",
            "Rotate crops to reduce pest and disease pressure."
        ]
        analysis["diagnosis"] += random.sample(disease_diag, k=3)
        analysis["recommendations"] += random.sample(disease_reco, k=3)

    # --- Dry/gray patches ---
    if gray_ratio > 0.05:
        gray_diag = [
            "Signs of drought stress observed.",
            "Gray patches may indicate dry leaves.",
            "Possible water shortage symptoms on crop.",
            "Leaves appear dehydrated or moisture-stressed.",
            "Soil moisture stress signs detected in foliage."
        ]
        gray_reco = [
            "Increase irrigation and check soil moisture.",
            "Apply mulching to retain soil water.",
            "Follow a regular watering schedule.",
            "Ensure irrigation matches crop growth stage.",
            "Improve soil moisture retention with organic matter."
        ]
        analysis["diagnosis"] += random.sample(gray_diag, k=3)
        analysis["recommendations"] += random.sample(gray_reco, k=3)

    # --- Healthy crop ---
    if green_ratio > 0.8 and yellow_ratio < 0.05 and brown_ratio < 0.02 and gray_ratio < 0.05:
        healthy_diag = [
            "Crop looks healthy and vigorous.",
            "Foliage is lush and green.",
            "Plant canopy appears stress-free.",
            "Crop is in excellent health condition.",
            "Overall crop health is good with no major stress."
        ]
        healthy_reco = [
            "Maintain regular irrigation schedule.",
            "Continue current crop management practices.",
            "No major action needed, keep monitoring.",
            "Sustain present practices for stable growth.",
            "Keep observing for early signs of stress."
        ]
        analysis["diagnosis"] += random.sample(healthy_diag, k=3)
        analysis["recommendations"] += random.sample(healthy_reco, k=3)

    return analysis


@app.post("/analyze_crop_image")
async def analyze_crop_image_api(file: UploadFile = File(...), crop_type: str = "Wheat"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = analyze_crop_health_detailed(tmp_path, crop_type)
        return JSONResponse(content={"result": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
