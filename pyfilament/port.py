from typing import Optional

class Port:
    def __init__(self, name: str, direction: str, range_: Optional[str], width: int):
        self.name = name
        self.direction = direction
        self.range_ = range_
        self.width = width

    def __repr__(self):
        return (f"Port(name={self.name}, direction={self.direction}, "
                f"range_={self.range_}, width={self.width})")
