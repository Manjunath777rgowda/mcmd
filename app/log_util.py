# Define color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class Log:
    @staticmethod
    def error(message):
        print(f"{RED}{message}{RESET}")

    @staticmethod
    def info(message):
        print(f"{GREEN}{message}{RESET}")

    @staticmethod
    def warn(message):
        print(f"{YELLOW}{message}{RESET}")