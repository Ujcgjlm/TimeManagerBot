class Statistic:
    __hours = 0

    def IncreaseStat(self, minutes) -> str:
        print(minutes / 60)
        self.__hours += minutes / 60

    def __str__(self) -> str:
        return str(self.__hours)

    def __init__(self, hours):
        self.__hours = hours