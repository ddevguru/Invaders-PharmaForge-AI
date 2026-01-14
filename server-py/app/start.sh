#!/bin/bash
# Render start script
cd /opt/render/project/src/server-py || cd server-py
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}

