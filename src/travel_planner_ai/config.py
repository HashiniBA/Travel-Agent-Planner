"""
Configuration settings for Travel Planner AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")

# LLM Configuration
DEFAULT_LLM = "gemini/gemini-2.0-flash-exp"

# Output Configuration
OUTPUT_DIR = "outputs"
MEMORY_ENABLED = True

# Encoding Configuration
os.environ['PYTHONIOENCODING'] = 'utf-8'