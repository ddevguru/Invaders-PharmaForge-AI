# Custom Voice Training Implementation Guide

## Overview

This implementation provides a custom voice training system for PharmaForge-AI that allows users to train their own voice for Text-to-Speech (TTS) in multiple languages (Hindi, English, Marathi) without using external LLM models.

## Key Features

✅ **Authentication Protection**: All dashboards require login/registration - no access without authentication
✅ **Custom Voice Training**: Train your own voice using audio samples
✅ **Multi-language Support**: Hindi (हिंदी), English, and Marathi (मराठी)
✅ **Rule-based Voice Agent**: NO LLM dependencies - uses rule-based command recognition
✅ **Voice Training Interface**: User-friendly UI for uploading audio samples and training

## Architecture

### Backend (Python/FastAPI)

1. **`server-py/app/voice_training.py`**
   - Voice training configuration and status management
   - Model storage and retrieval
   - Audio sample validation

2. **`server-py/app/voice_training_api.py`**
   - REST API endpoints for voice training
   - Upload audio samples
   - Start/stop training
   - Get training status

3. **`server-py/app/custom_voice_agent.py`**
   - Rule-based voice command processing (NO LLM)
   - Multi-language support (en, hi, mr)
   - Intent classification using regex patterns
   - Response generation in multiple languages

4. **`server-py/app/ai.py`**
   - Updated to use custom voice agent instead of LLM
   - Voice command processing API

### Frontend (React)

1. **`src/components/ProtectedRoute.jsx`**
   - Authentication check wrapper
   - Redirects to login if not authenticated
   - Role-based access control

2. **`src/pages/VoiceTraining.jsx`**
   - Voice training interface
   - Audio file upload
   - Language selection
   - Training status display

3. **`src/App.jsx`**
   - Updated routes with authentication protection
   - All dashboard routes require login
   - Voice training route added

## API Endpoints

### Voice Training

- `GET /voice-training/status` - Get training status
- `POST /voice-training/upload` - Upload audio samples
- `POST /voice-training/start-training` - Start training process
- `GET /voice-training/model-path` - Get trained model path
- `DELETE /voice-training/reset` - Reset training data

### Voice Agent (Custom - NO LLM)

- `POST /ai/chat` - Process voice commands (rule-based)
- `POST /ai/welcome` - Get welcome message
- `GET /ai/language-prompt` - Get language selection prompts

## Authentication Protection

All dashboard routes are now protected:

- `/dashboard/user` - Requires authentication (user/admin role)
- `/dashboard/admin` - Requires authentication (admin role)
- `/dashboard/warehouse` - Requires authentication (warehouse/admin role)
- `/dashboard/pharmacist` - Requires authentication (pharmacist/admin role)
- `/voice-training` - Requires authentication

If user is not logged in, they are redirected to `/login`.

## Voice Training Workflow

1. **Upload Audio Samples**
   - User uploads at least 3 audio samples (WAV, MP3, FLAC, M4A)
   - Minimum 3 samples required for training
   - Each sample should be 10-30 seconds long

2. **Select Languages**
   - Choose languages for training: English, Hindi, Marathi
   - Can select one or more languages

3. **Start Training**
   - Training process starts (currently simulated)
   - Status updates in real-time
   - Training may take 10-30 minutes

4. **Use Custom Voice**
   - Once trained, custom voice is used for TTS responses
   - Voice agent uses trained voice for all responses

## Voice Agent Commands

The voice agent supports the following commands (rule-based, NO LLM):

### English
- "open login" / "go to login" - Navigate to login page
- "open signup" / "register" - Navigate to signup page
- "show dashboard" - Navigate to dashboard
- "voice training" - Navigate to voice training page
- "help" - Show help message

### Hindi (हिंदी)
- "लॉगिन खोलो" - Navigate to login
- "साइनअप पर जाओ" - Navigate to signup
- "डैशबोर्ड दिखाओ" - Navigate to dashboard
- "आवाज प्रशिक्षण" - Navigate to voice training
- "मदद" - Show help

### Marathi (मराठी)
- "लॉगिन उघड" - Navigate to login
- "साइनअप वर जा" - Navigate to signup
- "डॅशबोर्ड दाखव" - Navigate to dashboard
- "व्हॉइस ट्रेनिंग" - Navigate to voice training
- "मदत" - Show help

## Implementation Notes

### Current Implementation Status

✅ **Completed:**
- Authentication protection for all routes
- Voice training API structure
- Voice training frontend interface
- Rule-based voice agent (NO LLM)
- Multi-language support (en, hi, mr)

⚠️ **Production Requirements:**
- Actual TTS model training (currently placeholder)
- Integration with TTS library (Coqui TTS, Piper TTS, or similar)
- Model storage and retrieval
- Audio processing and preprocessing

### TTS Library Integration

For production, you'll need to integrate a TTS library:

**Option 1: Coqui TTS** (Recommended)
```python
from TTS.api import TTS

# Load trained model
tts = TTS(model_path="path/to/trained/model")

# Synthesize speech
audio = tts.tts("Hello, this is my custom voice", language="en")
```

**Option 2: Piper TTS**
```python
import piper

# Load model
voice = piper.Voice.load("path/to/model")

# Synthesize
audio = voice.synthesize("Hello, this is my custom voice")
```

**Option 3: Custom Model**
- Train using your own TTS model
- Integrate model inference in `voice_training.py`

## File Structure

```
PharmaForge-AI/
├── server-py/
│   └── app/
│       ├── voice_training.py          # Voice training logic
│       ├── voice_training_api.py      # Training API routes
│       ├── custom_voice_agent.py      # Rule-based voice agent (NO LLM)
│       ├── ai.py                      # Updated to use custom agent
│       └── main.py                    # Updated with new routes
├── src/
│   ├── components/
│   │   └── ProtectedRoute.jsx         # Authentication wrapper
│   ├── pages/
│   │   ├── VoiceTraining.jsx          # Voice training UI
│   │   └── dashboard/                 # Protected dashboards
│   └── App.jsx                        # Updated routes with auth
└── voice_models/                      # Trained voice models (created at runtime)
```

## Usage

1. **Login/Register**: Users must login to access any dashboard
2. **Train Voice**: Go to `/voice-training` page
3. **Upload Samples**: Upload at least 3 audio samples
4. **Select Languages**: Choose languages (en, hi, mr)
5. **Start Training**: Click "Start Voice Training"
6. **Use Voice**: Custom voice will be used in voice agent

## Future Enhancements

- Actual TTS model training integration
- Real-time training progress updates
- Voice quality testing interface
- Multiple voice profiles per user
- Voice cloning from fewer samples
- Emotion and tone control
- Pronunciation customization

## Security Notes

- All routes require authentication
- Voice training data is user-specific
- Audio samples are stored securely
- Models are stored per user ID
- No external LLM dependencies (privacy-focused)

## Testing

1. Test authentication protection
2. Test voice training upload
3. Test rule-based commands
4. Test multi-language support
5. Test navigation actions

---

**Note**: This implementation provides the foundation for custom voice training. The actual TTS model training needs to be integrated with a TTS library in production.

