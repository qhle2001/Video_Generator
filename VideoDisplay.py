# media_player_control.py

import ctypes
import os
import time

class WindowsMediaPlayer:
    def __init__(self):
        self.current_media = None

    def open_file(self, file_path):
        absolute_path = os.path.abspath(file_path)
        self.current_media = absolute_path

    def send_key(self, key):
        VK_MEDIA_PLAY_PAUSE = 0xB3
        VK_MEDIA_STOP = 0xB2
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1

        key_mapping = {
            'play_pause': VK_MEDIA_PLAY_PAUSE,
            'stop': VK_MEDIA_STOP,
            'next_track': VK_MEDIA_NEXT_TRACK,
            'prev_track': VK_MEDIA_PREV_TRACK
        }

        vk_code = key_mapping.get(key)
        if vk_code is not None:
            ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk_code, 0, 0x0002, 0)

    def play(self):
        if self.current_media:
            os.startfile(self.current_media)
            time.sleep(1)  # Allow time for the player to start

    def play_pause(self):
        self.send_key('play_pause')

    def stop(self):
        self.send_key('stop')

    def next_track(self):
        self.send_key('next_track')

    def prev_track(self):
        self.send_key('prev_track')

    def main(self, video_path):
        self.open_file(video_path)

        # Example: Play, Stop, Play-Pause, Next Track, Previous Track
        self.play()
        time.sleep(2)
        self.stop()
        time.sleep(1)
        self.play_pause()
        time.sleep(1)
        self.next_track()
        time.sleep(1)
        self.prev_track()
