from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__, template_folder='.hidden_os')

# مسار لجلب الملفات من المجلد المخفي
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    cmd = request.json.get('cmd')
    # هنا نستخدم Popen للحفاظ على جلسة الترمينال مفتوحة
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    out, err = process.communicate()
    return jsonify({"output": out + err})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
