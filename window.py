class GameObject(object):
    """basic object with an update start and window"""
    childeren = []
    window = None

    def __init__(self):
        GameObject.childeren.append(self)

    def start(self) -> None:
        "called when game starts"
        pass

    def update(self) -> None:
        """called once per frame"""
        pass


class Sprite(GameObject):
    """GameOjbects that are drawn to the screen"""
    childeren = []

    def __init__(self):
        Sprite.childeren.append(self)
        super().__init__()
    
    def update(self):
        super().update()
        self.draw()

    def draw(self) -> None:
        pass

