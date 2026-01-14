"""
Voice Training API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from .security import get_current_claims
from .voice_training import (
    VoiceTrainingStatus,
    VoiceTrainingConfig,
    save_training_config,
    get_training_status,
    update_training_status,
    get_model_path,
    validate_audio_samples,
    VOICE_TRAINING_DIR
)

router = APIRouter(prefix="/voice-training", tags=["voice-training"])

class TrainingStatusResponse(BaseModel):
    status: str
    progress: float
    message: str
    model_path: Optional[str] = None
    languages: List[str] = []

class StartTrainingRequest(BaseModel):
    voice_name: str
    languages: List[str]  # ["en", "hi", "mr"]

@router.get("/status", response_model=TrainingStatusResponse)
async def get_status(claims: dict = Depends(get_current_claims)):
    """Get voice training status for current user"""
    user_id = claims.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    status = get_training_status(user_id)
    return TrainingStatusResponse(
        status=status.status,
        progress=status.progress,
        message=status.message,
        model_path=status.model_path,
        languages=status.languages
    )

@router.post("/upload")
async def upload_audio_samples(
    files: List[UploadFile] = File(...),
    claims: dict = Depends(get_current_claims)
):
    """Upload audio samples for voice training"""
    user_id = claims.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    if len(files) < 3:
        raise HTTPException(status_code=400, detail="At least 3 audio samples are required")
    
    user_dir = VOICE_TRAINING_DIR / user_id / "samples"
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear existing samples
    if user_dir.exists():
        shutil.rmtree(user_dir)
    user_dir.mkdir(parents=True, exist_ok=True)
    
    uploaded_files = []
    for i, file in enumerate(files):
        # Validate file type
        if not file.filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a')):
            raise HTTPException(status_code=400, detail=f"Invalid audio format: {file.filename}")
        
        file_path = user_dir / f"sample_{i+1}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded_files.append(str(file_path))
    
    return {
        "message": f"Uploaded {len(uploaded_files)} audio samples",
        "files": uploaded_files
    }

@router.post("/start-training")
async def start_training(
    request: StartTrainingRequest,
    claims: dict = Depends(get_current_claims)
):
    """Start voice training process"""
    user_id = claims.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    # Validate languages
    valid_languages = ["en", "hi", "mr"]
    for lang in request.languages:
        if lang not in valid_languages:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid language: {lang}. Valid languages: {valid_languages}"
            )
    
    # Check if audio samples exist
    samples_dir = VOICE_TRAINING_DIR / user_id / "samples"
    if not samples_dir.exists() or not list(samples_dir.glob("*")):
        raise HTTPException(
            status_code=400,
            detail="No audio samples found. Please upload audio samples first."
        )
    
    # Get uploaded files
    audio_files = [str(f) for f in samples_dir.glob("*") if f.is_file()]
    
    # Validate samples
    is_valid, error_msg = validate_audio_samples(audio_files)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Save training configuration
    config = VoiceTrainingConfig(
        user_id=user_id,
        voice_name=request.voice_name,
        languages=request.languages,
        audio_samples=audio_files
    )
    save_training_config(user_id, config)
    
    # Update status to training
    status = VoiceTrainingStatus(
        status="training",
        progress=0.1,
        message="Training started. This may take several minutes...",
        languages=request.languages
    )
    update_training_status(user_id, status)
    
    # TODO: In production, start actual training process in background
    # For now, simulate training completion
    # In real implementation, you would:
    # 1. Use Coqui TTS, Piper TTS, or similar library
    # 2. Train model on uploaded samples
    # 3. Save trained model
    # 4. Update status
    
    return {
        "message": "Voice training started",
        "status": "training",
        "languages": request.languages
    }

@router.get("/model-path")
async def get_voice_model_path(claims: dict = Depends(get_current_claims)):
    """Get path to trained voice model"""
    user_id = claims.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    model_path = get_model_path(user_id)
    if not model_path:
        raise HTTPException(status_code=404, detail="No trained model found")
    
    return {"model_path": model_path}

@router.delete("/reset")
async def reset_training(claims: dict = Depends(get_current_claims)):
    """Reset/delete voice training data"""
    user_id = claims.get("uid")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found")
    
    user_dir = VOICE_TRAINING_DIR / user_id
    if user_dir.exists():
        shutil.rmtree(user_dir)
    
    return {"message": "Voice training data reset"}

