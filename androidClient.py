# -*- coding: utf-8 -*-
import socket
from plyer import accelerometer, compass
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivymd.app import MDApp
import time
import re


leftdown = "ld".encode("utf-8")
rightdown = "rd".encode("utf-8")
leftup = "lu".encode("utf-8")
rightup = "ru".encode("utf-8")


class Connection(Screen):

    def connect(self):
        ip = self.ip_field.text
        if re.match(r'\d+\.\d+\.\d+\.\d+', ip):
            try:
                global s
                s = socket.socket()
                s.connect((ip, 8080))
                accelerometer.enable()
                compass.enable()
                self.parent.current = "clicks"
            except Exception:
                self.info_label.text = "Unable to connect"
        else:
            self.info_label.text = "Incorrect IP"


class Clicks(Screen):

    def stop(self):
        s.close()

    def start(self):
        Clock.schedule_interval(self.update, 1.0/10)
        self.start_button = "Stop"

    def update(self, *args):
        content = ""
        try:
            content = '%3f' % accelerometer.acceleration[0] + '%3f' % accelerometer.acceleration[1] + '%3f' % accelerometer.acceleration[2] + '%3f' % compass.field[0] + '%3f' % compass.field[1] + '%3f' % compass.field[2]
        except Exception as E:
            print(E)
        to_send = content.encode('utf-8')
        s.send(to_send)

    def left_down(self):
        s.send(leftdown)

    def right_down(self):
        s.send(rightdown)
    
    def left_up(self):
        s.send(leftup)

    def right_up(self):
        s.send(rightup)

sm = ScreenManager(transition=NoTransition())
sm.add_widget(Connection(name='connection'))
sm.add_widget(Clicks(name='clicks'))


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
