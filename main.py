import glfw

from rendering import Color, Rectangle, RenderingContext

if __name__ == '__main__':
    ctx = RenderingContext.instance()

    ctx.clear_color = Color.greyscale(0.8)

    scene = ctx.main_scene

    square = Rectangle(1, Color(0.2, 0.3, 0.7))
    square.transform.local_scale.set(0.5)

    scene.add_child(square)

    while not ctx.is_key_held(glfw.KEY_ESCAPE):
        ctx.render_frame()

        square.transform.rotation += 0.02
