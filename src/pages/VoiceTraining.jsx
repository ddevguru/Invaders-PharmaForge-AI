import React, { useState, useEffect } from 'react';
import { Upload, Play, Trash2, Mic, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export default function VoiceTraining() {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [training, setTraining] = useState(false);
  const [status, setStatus] = useState(null);
  const [voiceName, setVoiceName] = useState('My Voice');
  const [selectedLanguages, setSelectedLanguages] = useState(['en']);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthAndLoadStatus();
  }, []);

  const checkAuthAndLoadStatus = async () => {
    const token = localStorage.getItem('app_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/voice-training/status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStatus(data);
        if (data.languages && data.languages.length > 0) {
          setSelectedLanguages(data.languages);
        }
      }
    } catch (err) {
      console.error('Error loading status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const validFiles = selectedFiles.filter(file => {
      const ext = file.name.toLowerCase().split('.').pop();
      return ['wav', 'mp3', 'flac', 'm4a'].includes(ext);
    });

    if (validFiles.length !== selectedFiles.length) {
      setError('Some files were rejected. Only WAV, MP3, FLAC, and M4A files are supported.');
    }

    setFiles(prev => [...prev, ...validFiles]);
    setError('');
  };

  const removeFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length < 3) {
      setError('Please upload at least 3 audio samples for training');
      return;
    }

    const token = localStorage.getItem('app_token');
    if (!token) {
      navigate('/login');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`${API_BASE}/voice-training/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      const data = await response.json();
      alert(`Successfully uploaded ${data.files.length} audio samples`);
    } catch (err) {
      setError(err.message || 'Failed to upload files');
    } finally {
      setUploading(false);
    }
  };

  const handleStartTraining = async () => {
    if (selectedLanguages.length === 0) {
      setError('Please select at least one language');
      return;
    }

    const token = localStorage.getItem('app_token');
    if (!token) {
      navigate('/login');
      return;
    }

    setTraining(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/voice-training/start-training`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          voice_name: voiceName,
          languages: selectedLanguages
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Training failed to start');
      }

      alert('Voice training started! This may take several minutes.');
      checkAuthAndLoadStatus();
    } catch (err) {
      setError(err.message || 'Failed to start training');
    } finally {
      setTraining(false);
    }
  };

  const toggleLanguage = (lang) => {
    setSelectedLanguages(prev => {
      if (prev.includes(lang)) {
        return prev.filter(l => l !== lang);
      } else {
        return [...prev, lang];
      }
    });
  };

  const languages = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'hi', name: 'Hindi', native: 'हिंदी' },
    { code: 'mr', name: 'Marathi', native: 'मराठी' }
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 via-white to-teal-50">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
              <Mic className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Custom Voice Training</h1>
              <p className="text-gray-600">Train your own voice for multi-language TTS</p>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {status && status.status === 'completed' && (
            <div className="mb-6 p-4 bg-emerald-100 border border-emerald-300 text-emerald-700 rounded-lg">
              ✓ Voice model trained successfully! Your custom voice is ready to use.
            </div>
          )}

          {status && status.status === 'training' && (
            <div className="mb-6 p-4 bg-blue-100 border border-blue-300 text-blue-700 rounded-lg">
              ⏳ Training in progress... {status.message}
            </div>
          )}

          {/* Voice Name */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Voice Name
            </label>
            <input
              type="text"
              value={voiceName}
              onChange={(e) => setVoiceName(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none"
              placeholder="My Voice"
            />
          </div>

          {/* Language Selection */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select Languages for Training
            </label>
            <div className="flex flex-wrap gap-3">
              {languages.map(lang => (
                <button
                  key={lang.code}
                  onClick={() => toggleLanguage(lang.code)}
                  className={`px-4 py-2 rounded-lg border-2 transition-all ${
                    selectedLanguages.includes(lang.code)
                      ? 'bg-emerald-600 text-white border-emerald-600'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-emerald-500'
                  }`}
                >
                  {lang.name} ({lang.native})
                </button>
              ))}
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Selected: {selectedLanguages.length > 0 ? selectedLanguages.join(', ') : 'None'}
            </p>
          </div>

          {/* File Upload */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Upload Audio Samples (Minimum 3 files)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-emerald-500 transition-colors">
              <input
                type="file"
                multiple
                accept=".wav,.mp3,.flac,.m4a,audio/*"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer flex flex-col items-center"
              >
                <Upload className="w-12 h-12 text-gray-400 mb-3" />
                <span className="text-gray-700 font-medium">
                  Click to select audio files
                </span>
                <span className="text-sm text-gray-500 mt-1">
                  WAV, MP3, FLAC, or M4A format
                </span>
              </label>
            </div>

            {files.length > 0 && (
              <div className="mt-4 space-y-2">
                {files.map((file, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <span className="text-sm text-gray-700">{file.name}</span>
                    <button
                      onClick={() => removeFile(index)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={files.length < 3 || uploading}
              className="mt-4 w-full py-3 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Upload {files.length} File(s)
                </>
              )}
            </button>
          </div>

          {/* Training Status */}
          {status && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-2">Training Status</h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-medium">Status:</span>{' '}
                  <span className="capitalize">{status.status}</span>
                </div>
                {status.progress > 0 && (
                  <div>
                    <span className="font-medium">Progress:</span>{' '}
                    <span>{(status.progress * 100).toFixed(1)}%</span>
                  </div>
                )}
                {status.message && (
                  <div>
                    <span className="font-medium">Message:</span> {status.message}
                  </div>
                )}
                {status.languages && status.languages.length > 0 && (
                  <div>
                    <span className="font-medium">Languages:</span>{' '}
                    {status.languages.join(', ')}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Start Training Button */}
          <button
            onClick={handleStartTraining}
            disabled={training || files.length < 3}
            className="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            {training ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Starting Training...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Start Voice Training
              </>
            )}
          </button>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">Instructions</h3>
            <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
              <li>Record at least 3 high-quality audio samples in your voice</li>
              <li>Each sample should be 10-30 seconds long</li>
              <li>Speak clearly and naturally</li>
              <li>Choose the languages you want to train (English, Hindi, Marathi)</li>
              <li>Training may take 10-30 minutes depending on the number of samples</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

