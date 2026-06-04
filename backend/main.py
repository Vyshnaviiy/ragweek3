
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import mock_data
from datetime import datetime
from mangum import Mangum

# AI + RAG imports
from services.bedrock_service import (
    generate_response
)

from services.rag_service import (
    index_pdf,
    retrieve_chunks
)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="VoltStream API",
    version="1.0.0"
)

# Index PDF into ChromaDB
index_pdf()

# =========================
# ROOT ROUTE
# =========================
@app.get("/")
async def root():

    return {
        "message": "VoltStream Backend Running"
    }


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3003",
        "http://voltstream-frontend-v.s3-website-ap-south-2.amazonaws.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# MODELS
# =========================
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


# =========================
# DASHBOARD APIs
# =========================
@app.get("/api/v1/dashboard/live")
async def get_live_dashboard():

    return mock_data.live_data


@app.get("/api/v1/analytics/history")
async def get_analytics_history(
    period: Optional[str] = None
):

    if period:

        selected = period.lower()

        if selected not in mock_data.analytics_data:

            raise HTTPException(
                status_code=400,
                detail="Invalid analytics period"
            )

        return mock_data.analytics_data[selected]

    return mock_data.analytics_data


@app.get("/api/v1/devices")
async def get_devices():

    return mock_data.devices


@app.patch("/api/v1/devices/{device_id}")
async def update_device(
    device_id: int,
    update: DeviceUpdate
):

    for device in mock_data.devices:

        if device["id"] == device_id:

            device["status"] = update.status

            return {
                "message": "Device updated",
                "device": device
            }

    raise HTTPException(
        status_code=404,
        detail="Device not found"
    )


@app.get("/api/v1/billing/summary")
async def get_billing_summary():

    return mock_data.billing_summary


# =========================
# AI CHAT ENDPOINT
# =========================
@app.post("/api/v1/chat")
async def chat_with_ai(
    request: ChatRequest
):

    try:

        response_text = generate_response(
            request.message
        )

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now()
        )

    except Exception as e:

        return ChatResponse(
            response=f"Error: {str(e)}",
            timestamp=datetime.now()
        )


# =========================
# RAG QA ENDPOINT
# =========================
@app.post("/api/v1/qa")
async def qa_with_rag(
    request: ChatRequest
):

    try:

        # Retrieve relevant chunks
        retrieved_chunks = retrieve_chunks(
            request.message
        )

        # Join chunks into context
        context = "\n".join(
            retrieved_chunks
        )

        # Create grounded prompt
        prompt = f"""
        Answer the question using ONLY
        the provided context.

        Context:
        {context}

        Question:
        {request.message}
        """

        # Generate AI response
        response_text = generate_response(
            prompt
        )

        return ChatResponse(
            response=response_text,
            timestamp=datetime.now()
        )

    except Exception as e:

        return ChatResponse(
            response=f"RAG Error: {str(e)}",
            timestamp=datetime.now()
        )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=True
    )


# =========================
# AWS LAMBDA HANDLER
# =========================
handler = Mangum(app)

