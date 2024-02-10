from abc import ABC, abstractmethod


class AbsAI(ABC):

    def __init__(self):
        self.client = None

    @abstractmethod
    def ai_summary(self, user_input):
        pass

    @abstractmethod
    def find_text(self, user_input):
        pass
