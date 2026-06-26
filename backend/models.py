from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum

class IssueCategory(str, Enum):
    NO_SOUND = "NO_SOUND"
    LOW_SOUND = "LOW_SOUND"
    WHISTLING = "WHISTLING"
    DISTORTED = "DISTORTED"
    INTERMITTENT = "INTERMITTENT"
    NOT_CHARGING = "NOT_CHARGING"
    BATTERY_DRAIN = "BATTERY_DRAIN"
    BLUETOOTH = "BLUETOOTH"
    DISCOMFORT = "DISCOMFORT"
    BACKGROUND_NOISE = "BACKGROUND_NOISE"
    HEAR_NOT_UNDERSTAND = "HEAR_NOT_UNDERSTAND"
    OTHER = "OTHER"

class DeviceType(str, Enum):
    RIC = "RIC"
    BTE = "BTE"
    ITE = "ITE"
    NOT_SURE = "NOT_SURE"

class PowerType(str, Enum):
    BATTERY = "BATTERY"
    RECHARGEABLE = "RECHARGEABLE"
    NOT_SURE = "NOT_SURE"

class Side(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTH = "BOTH"

class Language(str, Enum):
    EN = "en"
    HI = "hi"
    KN = "kn"

# Auth Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    preferred_language: Language = Language.EN

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    email: EmailStr
    name: str
    preferred_language: Language
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserResponse(BaseModel):
    email: EmailStr
    name: str
    preferred_language: Language

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Triage Models
class TriageSubmission(BaseModel):
    main_issue: str
    side: Side
    device_type: DeviceType
    power_type: PowerType
    exposed_to_water: bool
    language: Language
    additional_details: Optional[str] = None

class TriageResponse(BaseModel):
    triage_id: str
    message: str

# Classification Models
class ClassificationRequest(BaseModel):
    complaint_text: str
    triage_data: Dict[str, Any]
    language: Language

class ClassificationResponse(BaseModel):
    issue_category: IssueCategory
    confidence_score: float
    needs_clarification: bool = False
    clarification_question: Optional[str] = None

# Step Models
class StepAction(str, Enum):
    FIXED = "FIXED"
    CONTINUE = "CONTINUE"

class StepUpdate(BaseModel):
    session_id: str
    step_id: str
    action: StepAction

class Step(BaseModel):
    id: str
    title: Dict[str, str]
    instructions: Dict[str, str]
    safety_notes: Dict[str, str]
    icon: str
    order: int

class StepResponse(BaseModel):
    current_step: Step
    progress: float
    total_steps: int
    current_step_number: int
    is_last_step: bool

# Session Models
class SessionCreate(BaseModel):
    triage_data: Dict[str, Any]
    classification_result: Dict[str, Any]
    language: Language

class SessionUpdate(BaseModel):
    step_id: str
    action: StepAction
    outcome: Optional[str] = None

class TroubleshootingSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    user_email: str
    triage_data: Dict[str, Any]
    classification_result: Dict[str, Any]
    language: Language
    steps_attempted: List[Dict[str, Any]] = []
    status: str = "in_progress"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SessionResponse(BaseModel):
    id: str
    triage_data: Dict[str, Any]
    classification_result: Dict[str, Any]
    language: str
    steps_attempted: List[Dict[str, Any]]
    status: str
    created_at: str
    updated_at: str

class SessionHistoryResponse(BaseModel):
    sessions: List[SessionResponse]
    total: int

# PDF Generation Models
class SupportSummaryRequest(BaseModel):
    session_id: str
    language: Language
