import threading
from playsound import playsound
lock = threading.Lock()


def speak(speech_to_speak):
    with lock:
        if speech_to_speak.value == 1:
            playsound("speek_files/Hello_1.mp3")
        elif speech_to_speak.value == 2:
            playsound("speek_files/No_2.mp3")
        elif speech_to_speak.value == 3:
            playsound("speek_files/There_3.mp3")
        elif speech_to_speak.value == 4:
            playsound("speek_files/Stop_4.mp3")
        elif speech_to_speak.value == 5:
            playsound("speek_files/Stop_5.mp3")
