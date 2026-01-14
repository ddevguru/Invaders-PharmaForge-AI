"""
Custom Voice Agent - Rule-based system (NO LLM)
Uses custom trained voice for TTS responses
"""
import re
from typing import Dict, Optional

# Rule-based command patterns (NO LLM)
COMMAND_PATTERNS = {
    "navigate_login": [
        r"(open|go to|navigate to|show|खोल|जाओ|उघड|दाखव)\s*(login|लॉगिन|लॉग इन|लॉगइन)",
        r"login|लॉगिन"
    ],
    "navigate_signup": [
        r"(open|go to|navigate to|show|register|sign up|खोल|जाओ|उघड|नोंदणी|साइनअप)",
        r"register|signup|साइनअप|नोंदणी"
    ],
    "navigate_dashboard": [
        r"(open|go to|navigate to|show|dashboard|खोल|जाओ|उघड|डॅशबोर्ड|डैशबोर्ड)"
    ],
    "navigate_voice_training": [
        r"(voice training|train voice|voice|आवाज प्रशिक्षण|आवाज|व्हॉइस)"
    ],
    "help": [
        r"(help|what can you do|how|मदद|क्या कर सकते हो|कसे|मदत)"
    ],
    "greeting": [
        r"(hello|hi|hey|namaste|नमस्ते|नमस्कार|हाय)"
    ]
}

RESPONSES = {
    "en": {
        "navigate_login": "I'll take you to the login page. Opening login page now.",
        "navigate_signup": "I'll take you to the registration page. Opening signup page now.",
        "navigate_dashboard": "I'll take you to the dashboard. Opening dashboard now.",
        "navigate_voice_training": "I'll take you to voice training. Opening voice training page now.",
        "help": """I'm Rxcompute, your voice assistant. I can help you with:
- Navigation: Say "open login", "go to signup", or "show dashboard"
- Voice Training: Say "voice training" to train your custom voice
- I understand commands in English, Hindi, and Marathi

Just speak naturally and I'll help you!""",
        "greeting": "Hello! I'm Rxcompute. How can I help you today?",
        "default": "I understand. How can I help you?"
    },
    "hi": {
        "navigate_login": "मैं आपको लॉगिन पेज पर ले जा रहा हूँ। लॉगिन पेज खोल रहा हूँ।",
        "navigate_signup": "मैं आपको रजिस्ट्रेशन पेज पर ले जा रहा हूँ। साइनअप पेज खोल रहा हूँ।",
        "navigate_dashboard": "मैं आपको डैशबोर्ड पर ले जा रहा हूँ। डैशबोर्ड खोल रहा हूँ।",
        "navigate_voice_training": "मैं आपको वॉइस ट्रेनिंग पेज पर ले जा रहा हूँ।",
        "help": """मैं Rxcompute हूँ, आपकी आवाज़ सहायक। मैं आपकी मदद कर सकता हूँ:
- नेविगेशन: "लॉगिन खोलो", "साइनअप पर जाओ", या "डैशबोर्ड दिखाओ" कहें
- वॉइस ट्रेनिंग: "वॉइस ट्रेनिंग" कहें
- मैं अंग्रेजी, हिंदी और मराठी में कमांड समझता हूँ""",
        "greeting": "नमस्ते! मैं Rxcompute हूँ। मैं आपकी कैसे मदद कर सकता हूँ?",
        "default": "मैं समझ गया। मैं आपकी कैसे मदद कर सकता हूँ?"
    },
    "mr": {
        "navigate_login": "मी तुम्हाला लॉगिन पेजवर नेत आहे. लॉगिन पेज उघडत आहे.",
        "navigate_signup": "मी तुम्हाला नोंदणी पेजवर नेत आहे. साइनअप पेज उघडत आहे.",
        "navigate_dashboard": "मी तुम्हाला डॅशबोर्डवर नेत आहे. डॅशबोर्ड उघडत आहे.",
        "navigate_voice_training": "मी तुम्हाला व्हॉइस ट्रेनिंग पेजवर नेत आहे.",
        "help": """मी Rxcompute आहे, तुमचा व्हॉइस असिस्टंट. मी तुम्हाला मदत करू शकतो:
- नेव्हिगेशन: "लॉगिन उघड", "साइनअप वर जा", किंवा "डॅशबोर्ड दाखव" म्हणा
- व्हॉइस ट्रेनिंग: "व्हॉइस ट्रेनिंग" म्हणा
- मी इंग्रजी, हिंदी आणि मराठीमध्ये कमांड समजतो""",
        "greeting": "नमस्कार! मी Rxcompute आहे. मी तुम्हाला कशी मदत करू शकतो?",
        "default": "मी समजलो. मी तुम्हाला कशी मदत करू शकतो?"
    }
}

ACTIONS = {
    "navigate_login": "navigate:/login",
    "navigate_signup": "navigate:/signup",
    "navigate_dashboard": "navigate:/dashboard/user",
    "navigate_voice_training": "navigate:/voice-training",
    "help": "",
    "greeting": "",
    "default": ""
}

def detect_language(text: str) -> str:
    """Detect language from text (simple heuristic)"""
    text_lower = text.lower()
    
    # Hindi detection (Devanagari script)
    if any('\u0900' <= char <= '\u097F' for char in text):
        return "hi"
    
    # Marathi detection (also uses Devanagari, but check common words)
    marathi_words = ["म्हण", "आहे", "नाही", "कर", "आला"]
    if any(word in text for word in marathi_words):
        # Could be Marathi, but hard to distinguish from Hindi
        # Default to Hindi for now, can be improved
        pass
    
    # Default to English
    return "en"

def classify_intent(text: str) -> str:
    """Classify intent using rule-based patterns (NO LLM)"""
    text_lower = text.lower()
    
    for intent, patterns in COMMAND_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return intent
    
    return "default"

def process_voice_command(text: str, language: Optional[str] = None) -> Dict:
    """
    Process voice command using rule-based system (NO LLM)
    
    Args:
        text: User's voice input text
        language: Language code (en, hi, mr) - if None, auto-detect
    
    Returns:
        dict with 'response', 'action', 'intent', and 'language' keys
    """
    if not text or not text.strip():
        return {
            "response": "I didn't understand. Please try again.",
            "action": "",
            "intent": "default",
            "language": "en"
        }
    
    # Detect language if not provided
    if not language:
        lang_code = detect_language(text)
    else:
        # Convert language code format (en-IN -> en)
        lang_code = language.split('-')[0] if '-' in language else language
        if lang_code not in ["en", "hi", "mr"]:
            lang_code = "en"
    
    # Classify intent
    intent = classify_intent(text)
    
    # Get response and action
    response = RESPONSES.get(lang_code, RESPONSES["en"]).get(intent, RESPONSES["en"]["default"])
    action = ACTIONS.get(intent, "")
    
    return {
        "response": response,
        "action": action,
        "intent": intent,
        "language": lang_code
    }

def get_welcome_message(language: str = "en") -> str:
    """Get welcome message in specified language"""
    lang_code = language.split('-')[0] if '-' in language else language
    if lang_code not in ["en", "hi", "mr"]:
        lang_code = "en"
    
    return RESPONSES.get(lang_code, RESPONSES["en"]).get("greeting", "Hello! I'm Rxcompute.")

def get_language_selection_prompt() -> Dict:
    """Get language selection prompt in all languages"""
    return {
        "en-IN": "Hello! I am Rxcompute. Please select your preferred language. Say English, Hindi, or Marathi.",
        "hi-IN": "नमस्कार! मैं Rxcompute हूँ। कृपया अपनी पसंदीदा भाषा चुनें। अंग्रेजी, हिंदी, या मराठी कहें।",
        "mr-IN": "नमस्कार! मी Rxcompute आहे. कृपया तुमची आवडती भाषा निवडा. इंग्रजी, हिंदी, किंवा मराठी म्हणा."
    }
