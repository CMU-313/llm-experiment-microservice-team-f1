import os

from flask import Flask
from flask import request, jsonify
from src.translator import translate_content

app = Flask(__name__)

@app.route("/")
def translator():
    content = request.args.get("content", default = "", type = str)
    is_english, translated_content = translate_content(content)
    return jsonify({
        "is_english": is_english,
        "translated_content": translated_content,
    })


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(debug=debug, host=host, port=port)
