import os
import sys
import uuid
import subprocess
import threading
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import importlib.util
import shutil
# Import functions from manim_code_generator
from manim_code_generator import get_solution_code, get_manim_code, render_manim_code

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Directory to store generated files and videos
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ManimOutput/generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory storage for job status
job_status = {}

@app.route('/api/generate', methods=['POST'])
def generate_visualization():
    """
    API endpoint to generate Manim visualization based on user prompt
    """
    if not request.json or 'prompt' not in request.json:
        return jsonify({"error": "Missing prompt field"}), 400
    
    prompt = request.json['prompt']
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    job_status[job_id] = {
        "status": "processing",
        "prompt": prompt,
        "solution": None,
        "manim_code": None,
        "video_path": None,
        "error": None
    }
    
    # Start the generation process in a background thread
    threading.Thread(target=process_job, args=(job_id, prompt)).start()
    
    return jsonify({
        "job_id": job_id,
        "status": "processing",
        "message": "Your visualization is being generated. Check status at /api/status/"+job_id
    })

def process_job(job_id, prompt):
    """
    Background process to handle the generation and rendering
    """
    try:
        # 1. Generate solution code
        solution_content = get_solution_code(prompt)
        job_status[job_id]["solution"] = solution_content
        job_status[job_id]["status"] = "generating_manim"
        
        # 2. Generate Manim code
        manim_code = get_manim_code(solution_content)
        job_status[job_id]["manim_code"] = manim_code
        job_status[job_id]["status"] = "rendering"
        
        # 3. Save Manim code to a unique file
        base_filename = f"manim_{job_id}"
        manim_file_path = os.path.join(OUTPUT_DIR, f"{base_filename}.py")
        
        with open(manim_file_path, "w") as f:
            f.write(manim_code)
        
        # 4. Render the Manim code
        success = render_manim_code(manim_file_path)
        
        if success:
            # Find the generated video file - assuming standard Manim output location
            try:
                # Check for the video in Manim's default media directory structure
                # Adjust these paths based on your Manim configuration
                manim_media_dir = os.path.join(
                                os.getcwd(),
                                "media", "videos",
                                os.path.splitext(os.path.basename(manim_file_path))[0],
                                "480p15"
                            )
                video_files = [f for f in os.listdir(manim_media_dir) if f.endswith(".mp4")]
                
                if video_files:
                    # Get the most recent video file
                    video_path = os.path.join(manim_media_dir, video_files[0])
                    
                    # Copy video to our output directory with a predictable name
                    output_video_path = os.path.join(OUTPUT_DIR, f"{base_filename}.mp4")
                    # subprocess.run(["cp", video_path, output_video_path])
                    shutil.copyfile(video_path, output_video_path)
                    
                    job_status[job_id]["video_path"] = output_video_path
                    job_status[job_id]["status"] = "completed"
                else:
                    job_status[job_id]["status"] = "failed"
                    job_status[job_id]["error"] = "Video rendering completed but no video file found"
            except Exception as e:
                job_status[job_id]["status"] = "failed"
                job_status[job_id]["error"] = f"Error locating video file: {str(e)}"
        else:
            job_status[job_id]["status"] = "failed"
            job_status[job_id]["error"] = "Failed to render Manim code"
    
    except Exception as e:
        job_status[job_id]["status"] = "failed"
        job_status[job_id]["error"] = str(e)

@app.route('/api/status/<job_id>', methods=['GET'])
def check_status(job_id):
    """
    API endpoint to check the status of a generation job
    """
    if job_id not in job_status:
        return jsonify({"error": "Job not found"}), 404
    
    status_data = {
        "job_id": job_id,
        "status": job_status[job_id]["status"],
        "prompt": job_status[job_id]["prompt"]
    }
    
    # Add error message if there is one
    if job_status[job_id]["error"]:
        status_data["error"] = job_status[job_id]["error"]
    
    # Add video URL if completed
    if job_status[job_id]["status"] == "completed":
        status_data["video_url"] = f"/api/video/{job_id}"
    
    return jsonify(status_data)

@app.route('/api/video/<job_id>', methods=['GET'])
def get_video(job_id):
    """
    API endpoint to retrieve the generated video
    """
    if job_id not in job_status:
        return jsonify({"error": "Job not found"}), 404
    
    if job_status[job_id]["status"] != "completed":
        return jsonify({"error": "Video not ready yet"}), 400
    
    if not job_status[job_id]["video_path"] or not os.path.exists(job_status[job_id]["video_path"]):
        return jsonify({"error": "Video file not found"}), 404
    
    return send_file(job_status[job_id]["video_path"], mimetype='video/mp4')

@app.route('/api/solution/<job_id>', methods=['GET'])
def get_solution(job_id):
    """
    API endpoint to retrieve the solution explanation
    """
    if job_id not in job_status:
        return jsonify({"error": "Job not found"}), 404
    
    if not job_status[job_id]["solution"]:
        return jsonify({"error": "Solution not available"}), 400
    
    return jsonify({"solution": job_status[job_id]["solution"]})

@app.route('/api/code/<job_id>', methods=['GET'])
def get_code(job_id):
    """
    API endpoint to retrieve the generated Manim code
    """
    if job_id not in job_status:
        return jsonify({"error": "Job not found"}), 404
    
    if not job_status[job_id]["manim_code"]:
        return jsonify({"error": "Manim code not available"}), 400
    
    return jsonify({"manim_code": job_status[job_id]["manim_code"]})

# Clean up old job data periodically (add this if needed)
def cleanup_old_jobs():
    # To be implemented if job history grows too large
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)