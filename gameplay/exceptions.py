class InactivityException(Exception):
    """
    Исключение для случая, когда игрок бездействует слишком долго
    """
    def __init__(self, message="Игрок бездействовал слишком долго."):
        super().__init__(message)

class SnakeTooLongException(Exception):
    """
    Исключение для случая, когда змейка заполняет всё поле
    """
    def __init__(self, message="Змейка заполнила всё игровое поле."):
        super().__init__(message)

class BoarderCollision(Exception):
    """
    Исключение для случая столкновения змейки с границой поля
    """
    def __init__(self, message = "Змейка врезалась в границу поля!"):
        super().__init__(message)
