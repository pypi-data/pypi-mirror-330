from dataclasses import dataclass


@dataclass
class RGBA:
    r: int
    g: int
    b: int
    a: int

    def __str__(self):
        return f"rgba({self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x})"
