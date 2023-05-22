import pyttsx3
import time


def say_instrutions(msg):
    engine = pyttsx3.init()  # text to speach
    engine.setProperty('rate', 150)
    engine.say(msg)
    engine.runAndWait()
#
#
# print(1)
# t=threading.Thread(target=foo)
# t.start()
# print(2)
# t.join()
# print(3)


# phrase = "Hi everyone"
# subprocess.call(["python", "speak.py", phrase])

# from multiprocessing import Process
# def f(name):
#     print ('hello', name)
#
# if __name__ == '__main__':
#
#     print(1)
#     time.sleep(0.5)
#     print(2)
#     Process(target=foo, args=('Ilan has small dick thats why he got a big ass to cover on the small size of his dick',)).start()
#
#
#     print(3)
#     time.sleep(1)
#     print(4)
#     p = Process(target=foo,
#                 args=('Noa i love  you',))
#     p.start()
#     time.sleep(1)
#     print(5)
#     time.sleep(1)
#     print(6)
#     print(7)
#     time.sleep(1)
#     print(8)
#     print(9)
#     time.sleep(1)
#     p = Process(target=foo,
#                 args=('True story hahaha',))
#     p.start()
#
#     print(10)
#     print(11)
#     time.sleep(1)
#     print(12)
#     p = Process(target=foo,
#                 args=('Noa happy birthday',))
#     p.start()
#     print(13)
#     time.sleep(1)
#     print(15)
#     #p.join()
#     # p.start()
#     # p.join()
