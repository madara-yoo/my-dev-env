from flask import Flask, send_from_directory, request, jsonify
import pexpect
import os

app = Flask(__name__, static_folder='.hidden_os')
current_dir = "/app"

@app.route('/')
def index():
    return send_from_directory('.hidden_os', 'index.html')

@app.route('/execute', methods=['POST'])
def execute():
    global current_dir
    cmd = request.json.get('cmd')
    
    # التعامل مع cd
    if cmd.startswith("cd "):
        target = cmd.split(" ")
        new_path = os.path.abspath(os.path.join(current_dir, target))
        if os.path.exists(new_path):
            current_dir = new_path
            return jsonify({"output": f"Changed directory to {current_dir}"})
        return jsonify({"output": "Directory not found"})

    # تنفيذ الأوامر مع دعم التفاعل (pexpect)
    try:
        # تشغيل الأمر في جلسة تفاعلية
        child = pexpect.spawn(f'/bin/bash -c "{cmd}"', cwd=current_dir, encoding='utf-8')
        
        # إذا طلب النظام مدخلاً (Y/n)
        index = child.expect(['[Y/n]', '[y/N]', pexpect.EOF], timeout=10)
        if index == 0 or index == 1:
            child.sendline('y') # إرسال الموافقة تلقائياً
            child.expect(pexpect.EOF)
            
        output = child.before
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"output": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
