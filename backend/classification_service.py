from dotenv import load_dotenv
import os
from models import ClassificationResponse, IssueCategory
#from emergentintegrations.llm.chat import LlmChat, UserMessage
import json
import logging

load_dotenv()

logger = logging.getLogger(__name__)

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

CLASSIFICATION_SYSTEM_PROMPT = """You are an expert hearing aid issue classifier. 
Your task is to classify user complaints into specific categories.

Categories:
- NO_SOUND: No audio output at all
- LOW_SOUND: Weak or reduced audio
- WHISTLING: High-pitched feedback sound
- DISTORTED: Unclear or garbled sound
- INTERMITTENT: Sound cuts in and out
- NOT_CHARGING: Charging issues
- BATTERY_DRAIN: Battery depletes quickly
- BLUETOOTH: Connectivity problems
- DISCOMFORT: Physical discomfort or pain
- BACKGROUND_NOISE: Too much ambient noise
- HEAR_NOT_UNDERSTAND: Can hear but cannot understand speech
- OTHER: None of the above

Respond ONLY with valid JSON in this exact format:
{
  "issue_category": "<CATEGORY>",
  "confidence_score": 0.95,
  "needs_clarification": false,
  "clarification_question": null
}

If confidence is below 0.7, set needs_clarification to true and provide a clarification_question.
"""

async def classify_complaint(complaint_text: str, triage_data: dict, language: str) -> ClassificationResponse:
    return fallback_classification(triage_data)
    """
    Classify the user's complaint using LLM
    """
    try:
        # Create context from triage data
        context = f"""User complaint: {complaint_text}
        
Triage information:
- Main issue: {triage_data.get('main_issue', 'Not specified')}
- Affected side: {triage_data.get('side', 'Not specified')}
- Device type: {triage_data.get('device_type', 'Not specified')}
- Power type: {triage_data.get('power_type', 'Not specified')}
- Exposed to water/dropped: {triage_data.get('exposed_to_water', False)}
- Additional details: {triage_data.get('additional_details', 'None')}

Classify this complaint into one of the predefined categories."""

        # Initialize LLM chat
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"classification_{triage_data.get('main_issue', 'unknown')}",
            system_message=CLASSIFICATION_SYSTEM_PROMPT
        ).with_model("openai", "gpt-5.2")
        
        # Send message
        user_message = UserMessage(text=context)
        response = await chat.send_message(user_message)
        
        # Parse response
        logger.info(f"LLM Response: {response}")
        
        # Extract JSON from response
        response_text = response.strip()
        
        # Try to find JSON in the response
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        result = json.loads(response_text)
        
        # Validate and create response
        return ClassificationResponse(
            issue_category=IssueCategory(result['issue_category']),
            confidence_score=result['confidence_score'],
            needs_clarification=result.get('needs_clarification', False),
            clarification_question=result.get('clarification_question')
        )
        
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        # Fallback to triage-based classification
        return fallback_classification(triage_data)

def fallback_classification(triage_data: dict) -> ClassificationResponse:
    """
    Rule-based fallback classification when LLM fails
    """
    main_issue = triage_data.get('main_issue', '').lower()
    
    mapping = {
        'no sound': IssueCategory.NO_SOUND,
        'weak sound': IssueCategory.LOW_SOUND,
        'whistling': IssueCategory.WHISTLING,
        'distorted sound': IssueCategory.DISTORTED,
        'sound cuts in/out': IssueCategory.INTERMITTENT,
        'not charging': IssueCategory.NOT_CHARGING,
        'battery drains fast': IssueCategory.BATTERY_DRAIN,
        'bluetooth issue': IssueCategory.BLUETOOTH,
        'discomfort': IssueCategory.DISCOMFORT,
        'too much background noise': IssueCategory.BACKGROUND_NOISE,
        'hear but don\'t understand': IssueCategory.HEAR_NOT_UNDERSTAND
    }
    
    category = IssueCategory.OTHER
    for key, value in mapping.items():
        if key in main_issue:
            category = value
            break
    
    return ClassificationResponse(
        issue_category=category,
        confidence_score=0.8,
        needs_clarification=False
    )
