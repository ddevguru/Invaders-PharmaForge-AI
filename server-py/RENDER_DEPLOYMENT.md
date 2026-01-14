# Render Deployment Guide for Voice Agent

## ✅ Important Notes for Voice Agent on Render

### 1. **HTTPS Requirement**
- ✅ **Voice Agent Render par kaam karega** - Web Speech API HTTPS pe kaam karti hai
- Render automatically HTTPS provide karta hai
- Frontend bhi HTTPS pe hona chahiye

### 2. **Ollama Model Issue**
- ❌ **Problem**: Ollama local model Render par directly host nahi kar sakte (memory issue)
- ✅ **Solution**: 
  - Option 1: External Ollama service use karein (Ollama Cloud, ya koi aur server)
  - Option 2: Smaller model use karein (llama3.2:1b instead of 3b)
  - Option 3: Alternative LLM service use karein (OpenAI, Anthropic, etc.)

### 3. **Voice Agent Features**
- ✅ Speech Recognition - Browser-based, Render se independent
- ✅ Text-to-Speech - Browser-based, Render se independent
- ✅ LangGraph Workflow - Backend pe chalega
- ✅ Langfuse Monitoring - Optional, cloud-based

## 🚀 Deployment Steps

### Step 1: Render Account Setup
1. Render.com pe account banayein
2. New Web Service create karein

### Step 2: Repository Connect
1. GitHub repository connect karein
2. Root directory: `server-py`
3. Build command: `pip install -r app/requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables
Render dashboard mein ye environment variables add karein:

```env
PYTHON_VERSION=3.12.0
ALLOWED_ORIGINS=https://your-frontend.onrender.com,https://your-frontend.vercel.app
OLLAMA_HOST=https://your-ollama-service.com
OLLAMA_MODEL=llama3.2:1b
LANGFUSE_PUBLIC_KEY=your_key_here
LANGFUSE_SECRET_KEY=your_secret_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Step 4: Frontend Configuration
Frontend `.env` file mein:

```env
VITE_API_BASE_URL=https://your-api.onrender.com
```

### Step 5: Ollama Alternative Setup

#### Option A: Use External Ollama Service
1. Ollama ko kisi aur server pe host karein (DigitalOcean, AWS, etc.)
2. Ya Ollama Cloud service use karein
3. `OLLAMA_HOST` environment variable mein URL daalein

#### Option B: Use Smaller Model
`voice_agent.py` mein model change karein:
```python
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:1b")  # Smaller model
```

#### Option C: Use Alternative LLM (Recommended for Production)
OpenAI ya Anthropic use karein:

```python
# voice_agent.py mein
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

## 📝 Required Files

### 1. `render.yaml` (Root directory)
Already created - Render configuration

### 2. `server-py/requirements.txt`
Dependencies already added

### 3. Update `server-py/app/voice_agent.py`
Ollama fallback add karein:

```python
# Better error handling for production
try:
    response = llm.invoke(messages)
    response_text = response.content if hasattr(response, 'content') else str(response)
except Exception as e:
    print(f"Error in LLM invocation: {e}")
    # Fallback response without LLM
    if language == "hi-IN":
        response_text = "मुझे क्षमा करें, मैं अभी उस प्रश्न का उत्तर नहीं दे सकता। कृपया बाद में कोशिश करें।"
    elif language == "mr-IN":
        response_text = "मला माफ करा, मी आत्ता त्या प्रश्नाचे उत्तर देऊ शकत नाही. कृपया नंतर प्रयत्न करा."
    else:
        response_text = "I apologize, I cannot answer that question right now. Please try again later."
```

## 🔧 Production Optimizations

### 1. Add Health Check
`server-py/app/main.py` mein already hai:
```python
@app.get('/health')
async def health():
    return {"ok": True, "service": "pharmaforge-auth-py"}
```

### 2. Add Error Handling
Better error responses for production

### 3. CORS Configuration
Frontend domain ko `ALLOWED_ORIGINS` mein add karein

## ⚠️ Important Limitations

1. **Ollama Local Model**: Render par directly Ollama host nahi kar sakte
   - Solution: External service use karein ya alternative LLM

2. **Memory**: Current model (llama3.2:3b) ko 13.6 GiB chahiye
   - Solution: Smaller model (1b) use karein

3. **Cold Starts**: Render free tier pe cold starts hote hain
   - Solution: Paid plan use karein ya keep-alive ping

## ✅ Voice Agent Will Work Because:

1. **Speech Recognition**: Browser-based, server se independent
2. **Text-to-Speech**: Browser-based, server se independent  
3. **HTTPS**: Render automatically provide karta hai
4. **API Calls**: Backend API properly configured hai

## 🧪 Testing After Deployment

1. Frontend deploy karein (Vercel/Render)
2. Backend API test karein: `https://your-api.onrender.com/health`
3. Voice agent test karein:
   - Language selection
   - Voice commands
   - Navigation

## 📞 Support

Agar koi issue ho:
1. Render logs check karein
2. Browser console check karein
3. Network tab mein API calls verify karein

---

**Note**: Voice agent kaam karega Render par, lekin Ollama model ke liye alternative solution chahiye hoga.

