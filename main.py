import time
from random import randrange

import glfw

from rendering import Circle, Color, GameObject, Rectangle, RenderingContext, Text

if __name__ == '__main__':
    # Create a 800x600 pixel window.
    ctx = RenderingContext(800, 600)

    # Set the clear color (background color) to light gray.
    ctx.clear_color = Color.greyscale(0.8)

    # Create a pixel scene which allows positioning using pixels.
    # Thus, the bottom left corner will have coordinates: [x = -ctx.width / 2, y = -ctx.height / 2],
    # and the top right corner will have coordinates: [x = ctx.width / 2, y = ctx.height / 2].
    pixel_scene = GameObject(parent=ctx.main_scene)

    # Create a blue rectangle and an orange circle.
    square = Rectangle(50, Color(0.2, 0.3, 0.7))  # 50x50 pixels
    circle = Circle(50, Color(0.7, 0.3, 0.2))  # 50 pixels diameter
    text = Text("#" * 10, color=Color(0.1, 0.5, 0.2))

    # Add objects to the pixel scene.
    pixel_scene.add_child(square, circle, text)

    # Enter the main loop. Repeat it until the escape key is pressed.
    while not ctx.is_key_held(glfw.KEY_ESCAPE):
        # Setting the scale of the pixel scene like this will give us the desired positioning behaviour
        pixel_scene.transform.local_scale.set(2 / max(ctx.height, ctx.width) / min(1, ctx.width / ctx.height))

        # This makes the rectangle stick to the bottom left corner of the screen (with a 10 pixel margin)
        square.x = -ctx.width / 2 + square.width / 2 + 10
        square.y = -ctx.height / 2 + square.height / 2 + 10

        # This makes the circle stick to the bottom right corner of the screen (with a 10 pixel margin)
        circle.x = ctx.width / 2 - circle.width / 2 - 10
        circle.y = -ctx.height / 2 + circle.height / 2 + 10

        # Generate random characters for the text
        text.text = [chr(randrange(33, 127)) for _ in range(10)]

        # Position text at the bottom middle of the screen
        text.x = max(-text.width / 2, -ctx.width / 2 + 10)
        text.y = -ctx.height / 2 + 15

        # Finally, render the frame to the screen.
        ctx.render_frame()

        # Sleep for 5/60 of a second.
        time.sleep(5 / 60)
