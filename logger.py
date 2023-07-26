from pubsub import pub

class Logger:
    def __init__(self):
        self.log = []

    def add_log(self, entry):
        print("Test", entry)
        self.log.append(entry)
        self.log = self.log[-5:]
        pub.sendMessage("log")

    def get_log(self):
        return self.log
