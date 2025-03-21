#!/usr/bin/env python3
"""
Run script for the Manim Visualization API server
"""
import os
import sys
import argparse
from flask_server import app
from config import FLASK_CONFIG

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run the Manim Visualization API server')
    parser.add_argument('--host', type=str, default=FLASK_CONFIG['HOST'],
                        help=f'Host to run the server on (default: {FLASK_CONFIG["HOST"]})')
    parser.add_argument('--port', type=int, default=FLASK_CONFIG['PORT'],
                        help=f'Port to run the server on (default: {FLASK_CONFIG["PORT"]})')
    parser.add_argument('--debug', action='store_true', default=FLASK_CONFIG['DEBUG'],
                        help='Run in debug mode')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Check if manim is installed
    try:
        import manim
        print(f"Manim version {manim.__version__} is installed.")
    except ImportError:
        print("WARNING: Manim is not installed. Please install it with 'pip install manim==0.17.3'")
        response = input("Continue anyway? (y/n): ")
        if response.lower() not in ['y', 'yes']:
            sys.exit(1)
    
    # Check if manim_code_generator.py exists
    if not os.path.exists('manim_code_generator.py'):
        print("ERROR: manim_code_generator.py not found in the current directory")
        sys.exit(1)
    
    print(f"\nStarting Manim Visualization API server on {args.host}:{args.port}")
    print(f"Debug mode: {'ON' if args.debug else 'OFF'}")
    print("\nAPI Endpoints:")
    print(f"  POST {FLASK_CONFIG['API_PREFIX']}/generate - Generate a visualization")
    print(f"  GET  {FLASK_CONFIG['API_PREFIX']}/status/<job_id> - Check job status")
    print(f"  GET  {FLASK_CONFIG['API_PREFIX']}/video/<job_id> - Get generated video")
    print(f"  GET  {FLASK_CONFIG['API_PREFIX']}/solution/<job_id> - Get solution text")
    print(f"  GET  {FLASK_CONFIG['API_PREFIX']}/code/<job_id> - Get generated Manim code")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()