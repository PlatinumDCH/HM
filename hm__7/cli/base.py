from config.data_base import session

class BaseCLI:
    def __init__(self):
        self.session = session