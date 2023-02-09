from core import RE_linear
import os


class Body:
    def __init__(self, name: str, set_of_points: list) -> None:
        self.name = name
        self.body = set_of_points

    def get_pixels(self):
        return self.body


class Viewport:
    def __init__(self, width: int, height: int, pos: RE_linear.Dot) -> None:
        self.width = width
        self.height = height
        self.pos = pos
        self.EXPERIMENTAL_distance = 1
        self.neutral_char = ' '
        self.screen = [[self.neutral_char for _ in range(round(self.width*RE_linear.OMEGA))] for _ in range(self.height)]
        self.master_point = None
    def clear_screen(self) -> None:
        self.screen = [[self.neutral_char for _ in range(round(self.width*RE_linear.OMEGA))] for _ in range(self.height)]

    def move_to(self, new_cord: RE_linear.Dot) -> None:
        self.pos = new_cord

    def move_on(self, new_cord: RE_linear.Dot) -> None:
        self.pos = RE_linear.Dot(
            *[self.pos[i] + new_cord[i] for i in range(len(self.pos))]
        )

    def render(self, obj: list or Body):
        if isinstance(obj, Body):
            for pixel in obj.get_pixels():
                if isinstance(pixel, RE_linear.Pixel):
                    delta_x = abs(pixel[0] - self.pos[0])
                    delta_y = abs(pixel[1] - self.pos[1])
                    if delta_x <= self.width//2 and delta_y <= self.height//2:
                        new_x = abs(self.pos[0] - pixel[0] - self.width//2)
                        new_y = abs(self.pos[1] - pixel[1] + self.height//2)
                        self.draw(
                            point=(new_x, new_y),
                            char=pixel.char,
                        )

                else:
                    raise TypeError(f"Object {obj} is not of type Pixel")
            self.display()
        elif isinstance(obj, list):
            for i in obj:
                self.render(i)
        else:
            raise TypeError(f'obj must be a list or Body, not {type(obj)}')

    def draw(self, point, char):
        self.screen[point[1]][point[0]] = char

    def display(self):
        for row in self.screen:
            print("".join(row))


class World:
    def __init__(self, name):
        self.name = name
        self.objects = []
        self.viewport_pos = RE_linear.Dot(0, 0)

    def add_object(self, obj: Body) -> None:
        self.objects.append(obj)

    def get_objects(self):
        return self.objects

    def __repr__(self) -> str:
        return "World({} object(s))".format(len(self.objects))


class Linker:
    def __init__(self, viewport: Viewport) -> None:
        self.viewport = viewport
        self.last_info = {
            "world" : None,
            "pos"   : None,
        }
        self.worlds = dict()

    def add_world(self, world: World) -> None:
        self.worlds[len(self.worlds)] = world.name, world

    def load_world(self, id: int or str):
        if isinstance(id, int):
            self.last_info["world"] = self.worlds[id]
            self.last_info["pos"] = self.worlds[id][1].viewport_pos
            self.viewport.move_to(self.worlds[id][1].viewport_pos)

        elif isinstance(id, str):
            for i in range(len(self.worlds)):
                if self.worlds[i][0] == id:
                    self.last_info["world"] = self.worlds[i]
                    self.last_info["pos"]   = self.worlds[i][1].viewport_pos
                    self.viewport.move_to(self.worlds[i][1].viewport_pos)
                    break
            else:
                raise ValueError(f"World with name {id} not found")
        else:
            raise TypeError(f'id must be an int or str, not {type(id)}')

    def settings(self):
        if os.path.exists(os.path.join(os.getcwd(), 'settings', 'linker.ENCP')):
            with open('settings/linker.encparams', 'rw') as f:
                None
        else:
            None

    def render(self):
        self.viewport.clear_screen()
        self.viewport.render(self.last_info["world"][1].get_objects())

    def __repr__(self) -> str:
        out = "Linker({} world(s))".format(len(self.worlds))
        for world_ind in self.worlds:
            out += "\n\t{} - {}".format(world_ind, self.worlds[world_ind]) + ("\tcurrent" if self.last_info["world"] == self.worlds[world_ind][0] else "")
        return out
