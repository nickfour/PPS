@echo off
:: ปิดการแสดงผลคำสั่งใน Batch File

:: ตรวจสอบว่ามี Python ติดตั้งอยู่หรือไม่
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ไม่พบการติดตั้ง Python ในระบบของคุณ
    echo กรุณาติดตั้ง Python ก่อนใช้งาน!
    pause
    exit /b
)

:: แสดงข้อความเพื่อเริ่มโปรแกรม
echo กำลังเปิด Nickqme7.py...

:: เรียกใช้ Python พร้อมไฟล์ .py
python Nickqme7.py

:: ตรวจสอบว่าการรันไฟล์สำเร็จหรือไม่
if %ERRORLEVEL% neq 0 (
    echo [ERROR] การรัน Nickqme7.py พบข้อผิดพลาด
    pause
    exit /b
)

:: แสดงข้อความเมื่อโปรแกรมสิ้นสุดการทำงาน
echo โปรแกรมสิ้นสุดการทำงาน
pause
exit
