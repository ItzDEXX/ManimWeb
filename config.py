import os

# Configuration for the Flask server
FLASK_CONFIG = {
    # Server settings
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'DEBUG': False,
    
    # Generated files directory
    'OUTPUT_DIR': os.path.join(os.path.dirname(os.path.abspath(__file__)), "ManimOutput/generated"),
    
    # API endpoints
    'API_PREFIX': '/api',
    
    # Timeout settings (in seconds)
    'SOLUTION_TIMEOUT': 60,
    'MANIM_GENERATION_TIMEOUT': 120,
    'RENDERING_TIMEOUT': 300,
    
    # Job cleanup settings
    'JOB_RETENTION_HOURS': 24,  # How long to keep job data
    'CLEANUP_INTERVAL_MINUTES': 60,  # How often to run cleanup
}

# Configuration for the manim renderer
MANIM_CONFIG = {
    # Rendering quality: 'l' for low, 'm' for medium, 'h' for high
    'QUALITY': 'l',
    
    # Preview after rendering: True/False
    'PREVIEW': False,
    
    # Additional command line arguments for manim
    'EXTRA_ARGS': [],
}

# Create necessary directories
os.makedirs(FLASK_CONFIG['OUTPUT_DIR'], exist_ok=True)