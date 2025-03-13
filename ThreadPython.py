import time
import threading

class Process(threading.Thread):
    def __init__(self, texte):
        threading.Thread.__init__(self)
        self.texte=texte

    def run(self):
        i = 0 
        while i < 5:
            print(self.texte)
            i += 1
            time.sleep(0.5)

pr1 = Process('un')
pr2 = Process('deux')

pr1.start()
pr2.start()

pr1.join()
pr2.join()