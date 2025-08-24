import tempfile
import os
import logging
from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        url = data.get("videoUrl", "").strip()
        logging.info(f"Received URL: {url}")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "video.mp4")

        # yt-dlp download
        ydl_opts = {
            "outtmpl": file_path,
            "format": "best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
