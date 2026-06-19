from flask import Flask, send_from_directory, request, jsonify
import subprocess
import os

app = Flask(__name__, static_folder='.hidden_os')

@app.route('/')
def index():
    return send_from_directory('.hidden_os', 'index.html')

@app.route('/execute', methods=['POST'])
def execute():
    cmd = request.json.get('cmd')
    try:
        # تنفيذ الأمر وإرجاع النتيجة
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout + result.stderr})
    except Exception as e:
        return jsonify({"output": str(e)})

if __name__ == '__main__':
    # Render يحتاج أن يستمع السيرفر على 0.0.0.0 والمنفذ الذي يحدده
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
