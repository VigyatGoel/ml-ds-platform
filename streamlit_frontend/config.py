"""
Configuration file for the Streamlit ML Platform Frontend
"""

import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Streamlit Configuration
PAGE_TITLE = "ML Data Science Platform"
PAGE_ICON = "📊"
LAYOUT = "wide"

# File Upload Configuration
ALLOWED_FILE_TYPES = ["csv"]
MAX_FILE_SIZE_MB = 200

# UI Configuration
SIDEBAR_STATE = "expanded"

# Feature Configuration
DEFAULT_PLOT_HEIGHT = 500
DEFAULT_PLOT_WIDTH = 800
