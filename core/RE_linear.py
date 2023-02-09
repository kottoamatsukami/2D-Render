import math


CORD_AXIS_NAME = "xyz"
OMEGA = 2.5


class Dot:
    def __init__(self, *args) -> None:
        if 0 < len(args) < 4:
            self.cord = {CORD_AXIS_NAME[i]: args[i] for i in range(len(args))}
        else:
            raise ValueError("Class dot must be initialized with 1 to 3 coordinates, got {}".format(len(args)))

    def __repr__(self) -> str:
        return "Dot{}(".format(len(self.cord)) +", ".join(f"{key}:{self.cord[key]}" for key in self.cord)+ ")"

    def __getitem__(self, item) -> (float or int):
        if isinstance(item, int):
            return list(self.cord.values())[item]
        elif isinstance(item, str):
            return self.cord[item]
        else:
            raise TypeError("Dot.__getitem__ only accepts int or str, got {}".format(type(item)))

    def __len__(self) -> int:
        return len(self.cord)

    def set_cord(self, cord, value) -> None:
        if isinstance(cord, int):
            self.cord["xyz"[cord]] = value
        elif isinstance(cord, str):
            self.cord[cord] = value
        else:
            raise TypeError("Dot.set_cord only accepts int or str, got {}".format(type(cord)))


class Vector:
    def __init__(self, *args) -> None:
        if len(args) == 1:
            if isinstance(args[0], (float, int)):
                self.cord = Dot(args[0])
            elif isinstance(args[0], Dot):
                self.cord = args[0]
            else:
                raise TypeError("Failed to calculate vector coordinates")
        else:
            if 0 < len(args) < 4:
                if all(isinstance(x, (float, int)) for x in args):
                    self.cord = Dot(*args)
                elif isinstance(args[0], Dot) and isinstance(args[1], Dot):
                    assert len(args[0].cord) == len(args[1].cord), "Dot coordinates must be the same length"
                    self.cord = Dot(*[args[1][i] - args[0][i] for i in range(len(args[0].cord))])
                else:
                    raise TypeError("Failed to calculate vector coordinates")

    def __repr__(self) -> str:
        return "Vector{}{}".format(len(self.cord), self.cord.cord)

    def __getitem__(self, item) -> (float or int):
        if isinstance(item, (int, str)):
            return self.cord[item]
        else:
            raise TypeError("Vector.__getitem__ only accepts int or str, got {}".format(type(item)))

    def normalize(self):
        return Vector(
            *[self.cord[CORD_AXIS_NAME[i]] / self.norm() for i in range(len(self.cord))]
        )

    def normalize_(self):
        self.cord = Dot(*self.normalize().cord.cord.values())

    def norm(self) -> float:
        return math.sqrt(sum(x**2 for x in self.cord.cord.values()))

    def __len__(self) -> int:
        return len(self.cord)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] + other.cord[CORD_AXIS_NAME[i]] for i in range(len(self.cord))])
        elif isinstance(other, Dot):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] + other.cord[CORD_AXIS_NAME[i]] for i in range(len(self.cord))])
        else:
            raise TypeError("Vector.__add__ only accepts Vector or Dot, got {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] - other.cord[CORD_AXIS_NAME[i]] for i in range(len(self.cord))])
        elif isinstance(other, Dot):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] - other.cord[CORD_AXIS_NAME[i]] for i in range(len(self.cord))])
        else:
            raise TypeError("Vector.__sub__ only accepts Vector or Dot, got {}".format(type(other)))

    def __mul__(self, other):
        if isinstance(other, Vector):
            return vector_product(self, other)
        elif isinstance(other, (int, float)):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] * other for i in range(len(self.cord))])
        else:
            raise TypeError("Vector.__mul__ only accepts Vector or Dot, got {}".format(type(other)))

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(*[self.cord[CORD_AXIS_NAME[i]] / other for i in range(len(self.cord))])
        else:
            raise TypeError("Vector.__truediv__ only accepts Vector or Dot, got {}".format(type(other)))

class Pixel:
    def __init__(self, pos: Dot, char):
        self.pos = pos
        self.char = char

    def get_data(self):
        return self.pos, self.char

    def __getitem__(self, item):
        return self.pos[item]


def vector_product(v1: Vector, v2: Vector) -> float:
    assert len(v1.cord) == len(v2.cord), "Dot coordinates must be the same dimensions"
    return sum(v1.cord[CORD_AXIS_NAME[i]] * v2.cord[CORD_AXIS_NAME[i]] for i in range(len(v1.cord)))


def euclidean_distance(v1: Vector, v2: Vector) -> float:
    assert len(v1.cord) == len(v2.cord), "Dot coordinates must be the same dimensions"
    return math.sqrt(sum((v1.cord[CORD_AXIS_NAME[i]] - v2.cord[CORD_AXIS_NAME[i]]) ** 2 for i in range(len(v1.cord))))


def describe_circle(center: Dot, radius: float, char="#") -> list:
    out = []
    for x in range(center[0]-radius, center[0]+radius+1):
        for y in range(center[1]-radius, center[1]+radius+1):
            if (x - center[0])**2 + (y - center[1])**2 <= radius**2 + 2:
                out.append(Pixel(
                    convert_cord(Dot(x, y)), char))
    return out

def convert_cord(cord):
    return Dot(round(cord[0]*OMEGA), cord[1])