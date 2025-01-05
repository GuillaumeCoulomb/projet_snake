class SpeedError(Exception):
    def __init__(self, value):
        super().__init__(f"Unexpected measured speed: {value} km/h.")

def foo():
    raise SpeedError(1300)

try:
    foo()
except SpeedError as e:
    print("Caught a SpeedError exception: %s" % e)

class SnakeException(Exception):


class GameOver(SnakeException):

