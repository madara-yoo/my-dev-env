from flask import Flask, render_template_string, request, jsonify
import subprocess

app = Flask(__name__)

# واجهة الويب التي تشبه الترمينال
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
        #output { white-space: pre-wrap; margin-bottom: 10px; }
        input { background: #000; color: #0f0; border: none; width: 100%; outline: none; }
    </style>
</head>
<body>
    <div id="output"></div>
    <form id="cmdForm"><input type="text" id="cmd" autofocus></form>
    <script>
        document.getElementById('cmdForm').onsubmit = async (e) => {
            e.preventDefault();
            const cmd = document.getElementById('cmd').value;
            const res = await fetch('/', { method: 'POST', body: new URLSearchParams({cmd}) });
            const data = await res.text();
            document.getElementById('output').innerHTML += "> " + cmd + "\\n" + data + "\\n";
            document.getElementById('cmd').value = '';
        };
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        cmd = request.form.get('cmd')
        try:
            # تنفيذ الأمر
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            result = e.output.decode()
        return result
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
