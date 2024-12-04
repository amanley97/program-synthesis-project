from typing import Optional, List

class Command:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text})"

class Instance(Command):
    def __init__(self, text: str, variable: str, type_name: str, size: Optional[int]):
        super().__init__(text)
        self.variable = variable
        self.type_name = type_name
        self.size = size

    def __repr__(self):
        return (f"{self.__class__.__name__}(variable={self.variable}, type_name={self.type_name}, "
                f"size={self.size})")

        
class Invoke(Command):
    def __init__(self, text: str, variable: str, function: str, range_: str, ports: List[str]):
        super().__init__(text)
        self.variable = variable
        self.function = function
        self.range_ = range_
        self.ports = ports

    def __repr__(self):
        return (f"{self.__class__.__name__}(variable={self.variable}, function={self.function}, "
                f"range_={self.range_}, ports={self.ports})")


# Subclass for Connect commands
class Connect(Command):
    def __init__(self, text: str, target: str, source: str):
        super().__init__(text)
        self.target = target
        self.source = source

    def __repr__(self):
        return f"{self.__class__.__name__}(target={self.target}, source={self.source})"
