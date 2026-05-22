from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import mock_data
from datetime import datetime
from mangum import Mangum

app = FastAPI(title="VoltStream API", version="1.0.0")
@app.get("/")
async def root():
    return {"message": "VoltStream Backend Running"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://localhost:3003",
    "http://voltstream-frontend-v.s3-website-ap-south-2.amazonaws.com"
], # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Device(BaseModel):
    id: int
    name: str
    status: str
    power_consumption: Optional[float] = None

class DeviceUpdate(BaseModel):
    status: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

@app.get("/api/v1/dashboard/live")
async def get_live_dashboard():
    return mock_data.live_data

@app.get("/api/v1/analytics/history")
async def get_analytics_history(period: Optional[str] = None):
    if period:
        selected = period.lower()
        if selected not in mock_data.analytics_data:
            raise HTTPException(status_code=400, detail="Invalid analytics period")
        return mock_data.analytics_data[selected]
    return mock_data.analytics_data

@app.get("/api/v1/devices")
async def get_devices():
    return mock_data.devices

@app.patch("/api/v1/devices/{device_id}")
async def update_device(device_id: int, update: DeviceUpdate):
    for device in mock_data.devices:
        if device["id"] == device_id:
            device["status"] = update.status
            return {"message": "Device updated", "device": device}
    raise HTTPException(status_code=404, detail="Device not found")

@app.get("/api/v1/billing/summary")
async def get_billing_summary():
    return mock_data.billing_summary

@app.post("/api/v1/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        # For now, use a simple rule-based response system
        # In production, replace with actual OpenAI integration
        message = request.message.lower()

        responses = {
            "hello": "Hello! Welcome to VoltStream. How can I help you with your energy management today?",
            "hi": "Hi there! I'm here to assist you with your energy usage and device management.",
            "help": "I can help you with:\n• Energy usage analysis and insights\n• Device control and optimization\n• Billing questions and cost savings\n• Usage patterns and recommendations\n• Troubleshooting device issues\n\nWhat would you like to know?",
            "cost": "To reduce your energy costs:\n1. Turn off unused devices (currently saving you energy)\n2. Use solar generation during peak hours\n3. Optimize device usage patterns\n4. Monitor your usage analytics for trends\n\nYour current net usage shows a surplus of 180W from solar generation!",
            "device": "You have 6 smart devices:\n• Air Conditioner (2800W) - OFF\n• Washing Machine (850W) - ON\n• Refrigerator (120W) - ON\n• Smart TV (200W) - OFF\n• EV Charger (3200W) - ON\n• Water Heater (4500W) - OFF\n\nTotal power consumption: 4,170W from active devices.",
            "analytics": "Your usage analytics show:\n• Daily: 260 kWh total usage\n• Weekly: 1,015 kWh total usage\n• Monthly: 7,580 kWh total usage\n\nSolar generation is helping offset your grid consumption!",
            "billing": "Your billing summary:\n• Current balance: $2,400.50\n• Projected bill: $3,100.75\n• Budget limit: $2,500\n• Usage at 85% of budget\n\nYou have 4 pending invoices totaling $2,890."
        }

        # Find matching response
        response_text = "I'm here to help with your energy management questions. Try asking about costs, devices, analytics, or billing!"

        for key, response in responses.items():
            if key in message:
                response_text = response
                break

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now()
        )

    except Exception as e:
        # Fallback response if anything fails
        return ChatResponse(
            response="I'm sorry, I'm currently unable to process your request. Please try again later or contact support if the issue persists.",
            timestamp=datetime.now()
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
handler = Mangum(app)
