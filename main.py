# import time

import glfw
import random

from check_collision import check_collision
from norm import norm
from rendering import Circle, Color, GameObject, Rectangle, RenderingContext
from math import cos, sin, pi


if __name__ == '__main__':
    # Create a 800x600 pixel window.
    ctx = RenderingContext(800, 600)

    # Set the clear color (background color) to light gray.
    ctx.clear_color = Color.greyscale(0.8)

    # Create a pixel scene which allows positioning using pixels.
    # Thus, the bottom left corner will have coordinates: [x = -ctx.width / 2, y = -ctx.height / 2],
    # and the top right corner will have coordinates: [x = ctx.width / 2, y = ctx.height / 2].
    pixel_scene = GameObject(parent=ctx.main_scene)

    pad = Rectangle(100, 55, Color(1, 1, 0))
    # Create a blue rectangle and an orange circle.
    # square = Rectangle(50, Color(0.2, 0.3, 0.7))  # 50x50 pixels
    # text = Text("#" * 10, color=Color(0.1, 0.5, 0.2))

    circle = Circle(50, Color(0.7, 0.3, 0.2))  # 50 pixels diameter
    circle.x = pad.x
    circle.y = -ctx.height / 2 + pad.height + circle.height / 2 + 10
    angle = random.random() * 90 - 45
    angle = angle * pi / 2 / 90
    print("angle =", angle)

    speed_circle = 0.5
    speed_pad = 0.5
    speed_x = sin(angle) * speed_circle
    speed_y = cos(angle) * speed_circle

    direction = "none"

    # Add objects to the pixel scene.
    # pixel_scene.add_child(square, circle, text)
    pixel_scene.add_child(pad, circle)

    # Enter the main loop. Repeat it until the escape key is pressed.
    while not ctx.is_key_held(glfw.KEY_ESCAPE):
        # Setting the scale of the pixel scene like this will give us the desired positioning behaviour
        pixel_scene.transform.local_scale.set(2 / max(ctx.height, ctx.width) / min(1, ctx.width / ctx.height))

        # This makes the rectangle stick to the bottom left corner of the screen (with a 10 pixel margin)
        # square.x = -ctx.width / 2 + square.width / 2 + 10
        # square.y = -ctx.height / 2 + square.height / 2 + 10
        maxX = ctx.width / 2 - pad.width / 2 - 10
        minX = -ctx.width / 2 + pad.width / 2 + 10
        pad.y = -ctx.height / 2 + pad.height / 2 + 10
        pad.width = ctx.width * 0.2

        if ctx.is_key_pressed(glfw.KEY_RIGHT):
            if direction == "right":
                direction = "none"
            else:
                direction = "right"

        if ctx.is_key_pressed(glfw.KEY_LEFT):
            if direction == "left":
                direction = "none"
            else:
                direction = "left"

        if direction == "right":
            pad.x += speed_pad
            if pad.x > maxX:
                pad.x = maxX
        else:
            if direction == "left":
                pad.x -= speed_pad  # pad.x = pad.x - 1
                if pad.x < minX:
                    pad.x = minX

        circle.x = circle.x + speed_x
        circle.y = circle.y + speed_y

        if circle.x >= ctx.width / 2 - circle.width / 2 or circle.x <= -ctx.width / 2 + circle.width / 2:
            # speed_y = speed_y
            speed_x = -speed_x

        if circle.y >= ctx.height / 2 - circle.height / 2 or circle.y <= -ctx.height / 2 + circle.height / 2:
            speed_y = -speed_y
            # speed_x = speed_x

        collision = check_collision(circle, pad)
        if collision:
            pc = [circle.x - pad.x, circle.y - pad.y]
            pc_length = norm(pc)
            pc_norm = [1 / pc_length * pc[0], 1 / pc_length * pc[1]]
            s = [pc_norm[0] * speed_circle, pc_norm[1] * speed_circle]
            speed_x = s[0]
            speed_y = s[1]

        # This makes the circle stick to the bottom right corner of the screen (with a 10 pixel margin)
        # circle.x = ctx.width / 2 - circle.width / 2 - 10
        # circle.y = -ctx.height / 2 + circle.height / 2 + 10

        # Generate random characters for the text
        # text.text = [chr(randrange(33, 127)) for _ in range(10)]

        # Position text at the bottom middle of the screen
        # text.x = max(-text.width / 2, -ctx.width / 2 + 10)
        # text.y = -ctx.height / 2 + 15

        # Finally, render the frame to the screen.
        ctx.render_frame()

        # Sleep for 5/60 of a second.
        # time.sleep(1 / 60)
