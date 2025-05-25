import os
import subprocess
import sys
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/verdictforge")

@app.get("/verdictforge")
def launch_streamlit():
    subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.headless", "true"])
    return {"message": "Streamlit app is launching on port 8501..."}
