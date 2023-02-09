import core.RE_world
import core.RE_linear

viewport = core.RE_world.Viewport(
    width=60,
    height=30,
    pos=core.RE_linear.Dot(0, 0),
)

linker = core.RE_world.Linker(
    viewport=viewport,
)

#
world_0 = core.RE_world.World(name="test1")
world_1 = core.RE_world.World(name="test2")


world_0.add_object(core.RE_world.Body(name="circle",
                                      set_of_points=core.RE_linear.describe_circle(
                                          center=core.RE_linear.Dot(0, 0),
                                          radius=5,
                                          char="■"
                                      )
                                      ))
#
linker.add_world(world_0)
linker.add_world(world_1)
#

linker.load_world('test1')
linker.render()
linker.viewport.move_on(core.RE_linear.Dot(20, 20))
linker.render()