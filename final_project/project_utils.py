import threading
from playsound import playsound
lock = threading.Lock()


def speak(speech_to_speak):
    with lock:
        if speech_to_speak.value == 1:
            playsound("speak_files/Hello_1.mp3")
        elif speech_to_speak.value == 2:
            playsound("speak_files/No_2.mp3")
        elif speech_to_speak.value == 3:
            playsound("speak_files/There_3.mp3")
        elif speech_to_speak.value == 4:
            playsound("speak_files/Stop_4.mp3")
        elif speech_to_speak.value == 5:
            playsound("speak_files/Stop_5.mp3")
        elif speech_to_speak.value == 6:
            playsound("speak_files/collision_6.mp3")
        elif speech_to_speak.value == 7:
            playsound("speak_files/collision_7.mp3")
        elif speech_to_speak.value == 8:
            playsound("speak_files/collision_8.mp3")
        elif speech_to_speak.value == 9:
            playsound("speak_files/Warning_9.mp3")
        elif speech_to_speak.value == 10:
            playsound("speak_files/Warning_10.mp3")
        elif speech_to_speak.value == 11:
            playsound("speak_files/Warning_11.mp3")
        elif speech_to_speak.value == 12:
            playsound("speak_files/Stop_12.mp3")
        elif speech_to_speak.value == 13:
            playsound("speak_files/Stop_13.mp3")
