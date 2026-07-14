from rag_service import search_documents
from fastapi import FastAPI, APIRouter, HTTPException, status, Header, Depends
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime, timezone
import uuid
from typing import Optional

from models import (
    UserCreate, UserLogin, UserResponse, TokenResponse, User,
    TriageSubmission, TriageResponse,
    ClassificationRequest, ClassificationResponse,
    SessionCreate, SessionUpdate, SessionResponse, SessionHistoryResponse,
    TroubleshootingSession, StepResponse, StepUpdate,
    SupportSummaryRequest, Step
)
from auth import get_password_hash, verify_password, create_access_token, decode_access_token
from step_library import get_steps_for_issue, STEP_LIBRARY
from classification_service import classify_complaint
from pdf_service import generate_support_summary_pdf

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dependency to get current user
async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return email
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

# Health check
@api_router.get("/")
async def root():
    return {"message": "AidAssist API is running", "version": "1.0.0"}

# Auth Routes
@api_router.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user document
    user_doc = {
        "email": user_data.email,
        "name": user_data.name,
        "preferred_language": user_data.preferred_language,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_data.email})
    
    user_response = UserResponse(
        email=user_data.email,
        name=user_data.name,
        preferred_language=user_data.preferred_language
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    # Find user
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": credentials.email})
    
    user_response = UserResponse(
        email=user['email'],
        name=user['name'],
        preferred_language=user['preferred_language']
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": current_user}, {"_id": 0})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        email=user['email'],
        name=user['name'],
        preferred_language=user['preferred_language']
    )

# Triage Routes
@api_router.post("/triage/submit", response_model=TriageResponse)
async def submit_triage(triage: TriageSubmission, current_user: str = Depends(get_current_user)):
    # Store triage data
    triage_doc = triage.model_dump()
    triage_doc['user_email'] = current_user
    triage_doc['created_at'] = datetime.now(timezone.utc).isoformat()
    triage_doc['id'] = str(uuid.uuid4())
    
    await db.triage_submissions.insert_one(triage_doc)
    
    return TriageResponse(
        triage_id=triage_doc['id'],
        message="Triage submitted successfully"
    )

# Classification Routes
@api_router.post("/classify", response_model=ClassificationResponse)
async def classify_issue(request: ClassificationRequest, current_user: str = Depends(get_current_user)):
    try:
        result = await classify_complaint(
            complaint_text=request.complaint_text,
            triage_data=request.triage_data,
            language=request.language
        )
        return result
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to classify complaint"
        )

# Session Routes
@api_router.post("/session/create")
async def create_session(session_data: SessionCreate, current_user: str = Depends(get_current_user)):
    session_doc = {
        "id": str(uuid.uuid4()),
        "user_email": current_user,
        "triage_data": session_data.triage_data,
        "classification_result": session_data.classification_result,
        "language": session_data.language,
        "steps_attempted": [],
        "current_step_index": 0,
        "status": "in_progress",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.sessions.insert_one(session_doc)
    
    return {"session_id": session_doc["id"], "message": "Session created successfully"}

@api_router.get("/session/{session_id}/current-step", response_model=StepResponse)
async def get_current_step(session_id: str, current_user: str = Depends(get_current_user)):
    session = await db.sessions.find_one(
        {"id": session_id, "user_email": current_user},
        {"_id": 0}
    )
    print(">>> get_current_step API called")
    print("Session ID:", session_id)

    if not session:
         raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
             detail="Session not found"
    )

    issue_category = session["classification_result"]["issue_category"]
    print("Issue:", issue_category)

    rag_results = search_documents(issue_category)
    print("RAG Results:", len(rag_results))

    if rag_results:
        print(rag_results[0].page_content)

    rag_results = search_documents(issue_category)
    print("Issue category:", issue_category)
    print("RAG Results Count:", len(rag_results))


    if rag_results:
        print(rag_results[0].page_content)


    # Existing troubleshooting steps
    steps = get_steps_for_issue(issue_category)

    #Add RAG information to the first step
    if rag_results:
        steps[0]["instructions"]["en"] += (
            "\n\n📖 User Guide Information:\n\n"
            + rag_results[0].page_content
        )

    current_step_index = session.get("current_step_index", 0)

    if current_step_index >= len(steps):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All steps completed"
        )

    current_step_data = steps[current_step_index]

    return StepResponse(
        current_step=Step(**current_step_data),
        progress=(current_step_index + 1) / len(steps) * 100,
        total_steps=len(steps),
        current_step_number=current_step_index + 1,
        is_last_step=(current_step_index == len(steps) - 1)
    )

@api_router.post("/session/{session_id}/update-step")
async def update_step(session_id: str, step_update: SessionUpdate, current_user: str = Depends(get_current_user)):
    session = await db.sessions.find_one({"id": session_id, "user_email": current_user}, {"_id": 0})
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    #Add step to attempted steps
    step_record = {
        "step_id": step_update.step_id,
        "action": step_update.action,
        "outcome": step_update.outcome,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    steps_attempted = session.get('steps_attempted', [])
    steps_attempted.append(step_record)
    
    # Update status based on action
    new_status = session['status']
    current_step_index = session.get('current_step_index', 0)
    
    if step_update.action == "FIXED":
        new_status = "resolved"
    elif step_update.action == "CONTINUE":
        current_step_index += 1
        # Check if this was the last step (ESCALATE)
        issue_category = session['classification_result']['issue_category']
        steps = get_steps_for_issue(issue_category)
        if current_step_index >= len(steps):
            new_status = "escalated"
    
    # Update session
    await db.sessions.update_one(
        {"id": session_id},
        {
            "$set": {
                "steps_attempted": steps_attempted,
                "current_step_index": current_step_index,
                "status": new_status,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {
        "message": "Step updated successfully",
        "status": new_status,
        "next_step_available": current_step_index < len(steps) and new_status == "in_progress"
    }

@api_router.get("/session/history", response_model=SessionHistoryResponse)
async def get_session_history(current_user: str = Depends(get_current_user)):
    sessions = await db.sessions.find(
        {"user_email": current_user},
        {"_id": 0}
    ).sort("created_at", -1).to_list(100)
    
    session_responses = [SessionResponse(**session) for session in sessions]
    
    return SessionHistoryResponse(
        sessions=session_responses,
        total=len(session_responses)
    )

@api_router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, current_user: str = Depends(get_current_user)):
    session = await db.sessions.find_one({"id": session_id, "user_email": current_user}, {"_id": 0})
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return SessionResponse(**session)

# PDF Generation Route
@api_router.post("/support-summary/generate")
async def generate_support_summary(request: SupportSummaryRequest, current_user: str = Depends(get_current_user)):
    # Get session data
    session = await db.sessions.find_one(
        {"id": request.session_id, "user_email": current_user},
        {"_id": 0}
    )
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    try:
        # Generate PDF
        pdf_bytes = generate_support_summary_pdf(session, request.language)
        
        # Return PDF as response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=aidassist_summary_{request.session_id}.pdf"
            }
        )
    except Exception as e:
        logger.error(f"PDF generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF"
        )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()