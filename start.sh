#!/bin/bash
# Start API BackEnd using Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000 

