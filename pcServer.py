# -*- coding: utf-8 -*-
import socket
import pyautogui

hostname = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8080))
s.listen(1)
print(f"{hostname} listens on port 8080")
conn, addr = s.accept()
print(addr)

while True:
    encoded_data = conn.recv(1024)
    if not encoded_data:
        break
    data = encoded_data.decode("utf-8")
    print(data)
    if data[0] == "ld":
        pyautogui.mouseDown()
    elif data[0] == "rd":
        pyautogui.mouseDown(button="right")
    elif data[0] == "lu":
        pyautogui.mouseUp()
    elif data[0] == "ru":
        pyautogui.mouseUp(button="right")
    else:
        pyautogui.moveTo(abs(int(data.split()[0]*20)), abs(int(data.split()[1]*20)))
