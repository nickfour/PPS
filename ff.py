import subprocess
import os
import signal
import sys
import time

# ANSI escape codes สำหรับสี
RESET = "\033[0m"
CYAN = "\033[96m"  # สีฟ้าอ่อน
MAGENTA = "\033[95m"  # สีชมพูเข้ม
RED = "\033[91m"  # สีแดง
GREEN = "\033[92m"  # สีเขียว

def install_requirements():
    """ฟังก์ชันสำหรับอัปเดต pip และติดตั้งโมดูลจาก requirements.txt"""
    print(f"{CYAN}กำลังอัปเดต pip เป็นเวอร์ชันล่าสุด...{RESET}")
    try:
        # อัปเดต pip
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"{GREEN}อัปเดต pip สำเร็จ!{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}เกิดข้อผิดพลาดในการอัปเดต pip: {e.stderr.decode().strip()}{RESET}")
        sys.exit(1)

def cls(delay=1):
    """ล้างหน้าจอ Console พร้อมหน่วงเวลา"""
    print("กำลังล้างหน้าจอ...")
    time.sleep(delay)  # หน่วงเวลาเป็นวินาที
    # สำหรับ Windows
    if os.name == 'nt':
        os.system('cls')
    # สำหรับ macOS และ Linux
    else:
        os.system('clear')



def run_command(ip_address):
    """ฟังก์ชันสำหรับรันคำสั่ง"""
    command = f"python3 start.py UDP {ip_address} 100 999"
    print(f"กำลังรันคำสั่ง: {command}")
    return subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

def get_ip_or_undo(previous_ip_address):
    """ฟังก์ชันรับ IP Address หรือย้อนกลับไปใช้ IP ก่อนหน้า"""
    while True:
        user_input = input(f"{MAGENTA}(เปลี่ยน IP)  {GREEN}กรุณาป้อน IP Address ใหม่ หรือพิมพ์ 'B' เพื่อย้อนกลับ: {RESET}").strip()
        cls()
        if user_input.lower() in ['b', 'ิ']:
            if previous_ip_address:
                return previous_ip_address, True
            else:
                print(f"{RED}ไม่มี IP Address ก่อนหน้าให้ย้อนกลับ!{RESET}")
        else:
            return user_input, False

""" install_requirements() """
cls(1)


# เริ่มต้นด้วยการรับ IP Address
ip_address = input(f"{CYAN}กรุณาป้อน IP Address: {RESET}").strip()
previous_ip_address = None  # เก็บ IP Address ก่อนหน้า

if ip_address:
    process = run_command(ip_address)
    cls(1)

    try:
        while True:
            # รอคำสั่งจากผู้ใช้
            user_input = input(f"{GREEN}(Working)   {MAGENTA}พิมพ์ 'Z' เพื่อหยุด,| 'X' เพื่อรันต่อ,| 'C' เพื่อเปลี่ยน IP | หรือ 'ctrl_c' เพื่อออก: {RESET}").strip().lower()
            
            if user_input in ['z', 'ผ']:
                os.killpg(os.getpgid(process.pid), signal.SIGSTOP)
                print(f"{RED}หยุดการทำงานชั่วคราว{RESET}")
            elif user_input in ['x', 'ป']:
                if process.poll() is None:  # ตรวจสอบว่าโปรเซสยังคงทำงานอยู่
                    os.killpg(os.getpgid(process.pid), signal.SIGCONT)  # ทำงานต่อ
                    print(f"{MAGENTA}รันต่อ{RESET}")
                else:
                    print(f"{RED}โปรเซสถูกหยุดแล้ว ไม่สามารถทำงานต่อได้{RESET}")
            elif user_input in ['c', 'แ']:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # หยุดกระบวนการเดิม
                previous_ip_address = ip_address  # เก็บ IP Address ก่อนหน้า
                ip_address, is_undo = get_ip_or_undo(previous_ip_address)
                if is_undo:
                    print(f"{MAGENTA}ย้อนกลับไปใช้ IP Address ก่อนหน้า: {ip_address}{RESET}")
                process = run_command(ip_address)
            elif user_input == "exit":
                process.terminate()
                print(f"{RED}สิ้นสุดการทำงาน{RESET}")
                break
            else:
                print(f"{RED}คำสั่งไม่ถูกต้อง กรุณาลองใหม่{RESET}")
    except KeyboardInter11àlà11rupt:
        print(f"\n{RED}สิ้นสุดการทำงาน{RESET}")
        process.terminate()
else:
    print(f"{RED}กรุณาป้อน IP Address ที่ถูกต้อง!{RESET}")
