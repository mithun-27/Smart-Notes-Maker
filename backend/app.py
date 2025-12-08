# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

from summarizer import summarize_text
from quiz_generator import generate_quiz
from pdf_utils import extract_text_from_pdf
from youtube_utils import fetch_youtube_transcript

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/from-text", methods=["POST"])
def from_text():
    data = request.get_json() or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400

    summary = summarize_text(text)
    quiz = generate_quiz(text, summary)

    return jsonify({
        "summary": summary,
        "quiz": quiz
    })


@app.route("/api/from-pdf", methods=["POST"])
def from_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text from PDF: {e}"}), 500

    if not text.strip():
        return jsonify({"error": "No text extracted from PDF."}), 400

    summary = summarize_text(text)
    quiz = generate_quiz(text, summary)

    return jsonify({
        "summary": summary,
        "quiz": quiz
    })


@app.route("/api/from-youtube", methods=["POST"])
def from_youtube():
    data = request.get_json() or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        text = fetch_youtube_transcript(url)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch transcript: {e}"}), 500

    if not text.strip():
        return jsonify({"error": "No transcript text found."}), 400

    summary = summarize_text(text)
    quiz = generate_quiz(text, summary)

    return jsonify({
        "summary": summary,
        "quiz": quiz
    })


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Smart Notes Maker backend is running!"})


if __name__ == "__main__":
    # For dev only
    app.run(host="127.0.0.1", port=5000, debug=True)
