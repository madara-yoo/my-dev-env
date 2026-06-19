import os
from flask import Flask, send_from_directory, request, jsonify
import subprocess

# استخدام المجلد الجديد 'webos'
app = Flask(__name__, static_folder='webos')

@app.route('/')
def index():
    # المسار المباشر لملف index.html داخل webos
    return send_from_directory('webos', 'index.html')

@app.route('/execute', methods=['POST'])
def execute():
    cmd = request.json.get('cmd')
    try:
        # تنفيذ الأمر
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({"output": result.stdout + result.stderr})
    except Exception as e:
        return jsonify({"output": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
