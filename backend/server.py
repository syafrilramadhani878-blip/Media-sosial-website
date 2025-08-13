from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

# Import new models and services
from models.contact import ContactMessage, ContactMessageCreate, ContactResponse
from services.email_service import email_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Original routes
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# New contact form endpoint
@api_router.post("/contact", response_model=ContactResponse)
async def send_contact_message(contact_data: ContactMessageCreate):
    try:
        # Create contact message object
        contact_message = ContactMessage(**contact_data.dict())
        
        # Try to send email
        email_sent = email_service.send_contact_message(
            contact_data.name,
            contact_data.email,
            contact_data.message
        )
        
        if email_sent:
            contact_message.is_sent = True
            # Save to database
            await db.contact_messages.insert_one(contact_message.dict())
            
            return ContactResponse(
                success=True,
                message="Pesan Anda berhasil dikirim! Terima kasih atas masukan Anda.",
                data={"sent_at": contact_message.timestamp.isoformat()}
            )
        else:
            # Save to database even if email failed
            await db.contact_messages.insert_one(contact_message.dict())
            
            return ContactResponse(
                success=False,
                message="Maaf, terjadi masalah saat mengirim email. Pesan Anda sudah tersimpan.",
                data=None
            )
            
    except Exception as e:
        logging.error(f"Contact form error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan server. Silakan coba lagi nanti."
        )

# Test email configuration endpoint
@api_router.get("/test-email")
async def test_email_config():
    """Test endpoint to check email configuration"""
    try:
        is_configured = email_service.gmail_password is not None
        connection_works = email_service.test_connection() if is_configured else False
        
        return {
            "email_configured": is_configured,
            "connection_test": connection_works,
            "gmail_email": email_service.gmail_email
        }
    except Exception as e:
        return {"error": str(e)}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()