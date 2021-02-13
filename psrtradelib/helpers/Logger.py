class Logger():
    def Log(self, text):
        print(text)
    
    def Warning(self, text):
        print(bcolors.WARNING + str(text) + bcolors.ENDC)

    def Error(self, text):
        print(bcolors.FAIL + str(text) + bcolors.FAIL)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\u001b[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'