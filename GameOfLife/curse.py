import abc


class UI(abc.ABC):

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod:
    def run(self) -> None:
        pass