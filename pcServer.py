# -*- coding: utf-8 -*-
import socket
import pyautogui

hostname = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8080))
s.listen(1)
print(f"{hostname} listens on port 8080")
conn, addr = s.accept()
while True:
    encoded_data = conn.recv(1024)
    if not encoded_data:
        break
    data = encoded_data.decode("utf-8").split()
    if data == "ld":
        pyautogui.mouseDown()
    elif data == "rd":
        pyautogui.mouseDown(button="right")
    elif data == "lu":
        pyautogui.mouseUp()
    elif data == "ru":
        pyautogui.mouseUp(button="right")
