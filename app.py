import subprocess
import tempfile
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

TUTORIALS = [
    {
        "id": 1,
        "title": "Introduction to Lightning Network Routing",
        "content": "",
        "code": 'fn main() {\n    println!("Welcome to Lightning Network Routing!");\n}'
    },
    {
        "id": 2,
        "title": "Understanding Payment Channels",
        "content": "",
        "code": 'fn main() {\n    // Your code here\n    println!("Payment channels are the foundation of Lightning!");\n}'
    },
    {
        "id": 3,
        "title": "Pathfinding Algorithms",
        "content": "",
        "code": 'fn main() {\n    // Implement a simple pathfinding algorithm\n    println!("Finding the best route...");\n}'
    }
]

@app.route('/')
def index():
    return render_template('index.html', tutorials=TUTORIALS)

@app.route('/tutorial/<int:tutorial_id>')
def tutorial(tutorial_id):
    tut = next((t for t in TUTORIALS if t['id'] == tutorial_id), None)
    if not tut:
        return "Tutorial not found", 404
    
    prev_id = tutorial_id - 1 if tutorial_id > 1 else None
    next_id = tutorial_id + 1 if tutorial_id < len(TUTORIALS) else None
    
    return render_template('tutorial.html', 
                         tutorial=tut, 
                         prev_id=prev_id, 
                         next_id=next_id,
                         total=len(TUTORIALS))

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, 'main.rs')
        exe_path = os.path.join(tmpdir, 'main')
        
        with open(src_path, 'w') as f:
            f.write(code)
        
        compile_result = subprocess.run(
            ['rustc', src_path, '-o', exe_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'output': compile_result.stderr
            })
        
        try:
            run_result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            return jsonify({
                'success': True,
                'output': run_result.stdout + run_result.stderr
            })
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'output': 'Execution timed out (10 second limit)'
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
