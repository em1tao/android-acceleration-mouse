# -*- coding: utf-8 -*-
import socket
from plyer import accelerometer
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivymd.app import MDApp
import time
import re


class Connection(Screen):
    left_click = "l".encode("utf-8")
    right_click = "r".encode("utf-8")

    def update(self):
        content = ""
        try:
            content = f"""{accelerometer.acceleration[0]: .3f} +
            {accelerometer.acceleration[1]]: .3f} +
            {accelerometer.acceleration[2]: .3f}"""
        except Exception as E:
            print(E)
        to_send = content.encode('utf-8')
        s.send(to_send)

    def connect(self):
        ip = self.ipfield.text
        if re.match(r'\d+\.\d+\.\d+\.\d+', ip):
            print("Devka")
            try:
                s = socket.socket()
                s.connect((ip, 8080))
                accelerometer.enable()
                self.parent.current = "main"
            except Exception:
                self.infolabel.text = "Unable to connect"
                pass
        else:
            self.infolabel.text = "Incorrect IP"


class Main(Screen):

    def left_click(self):
        s.send(left_click)

    def right_click(self):
        s.send(right_click)


sm = ScreenManager(transition=NoTransition())
sm.add_widget(Connection(name='connection'))
sm.add_widget(Main(name='main'))


class androidApp(MDApp):

    def __init__(self, **kwargs):
        self.title = "Client"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = 'Orange'
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_file("androidgui.kv")


if __name__ == "__main__":
    androidApp().run()
