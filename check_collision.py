from norm import norm
from rendering import Circle, Rectangle


def check_collision(circle: Circle, rectangle: Rectangle):
    x_right = rectangle.x + rectangle.width / 2
    x_left = rectangle.x - rectangle.width / 2
    y_top = rectangle.y + rectangle.height / 2
    y_bottom = rectangle.y - rectangle.height / 2

    P1 = [x_left, y_top]
    P2 = [x_right, y_top]
    P3 = [x_left, y_bottom]
    P4 = [x_right, y_bottom]

    for point in [P1, P2, P3, P4]:
        x = point[0]
        y = point[1]

        L_x = x - circle.x
        L_y = y - circle.y
        L = [L_x, L_y]

        length = norm(L)

        radius = circle.width / 2

        if length <= radius:
            return True

    x_collision = rectangle.x - rectangle.width / 2 < circle.x < rectangle.x + rectangle.width / 2
    y_collision = abs(circle.y - rectangle.y) - rectangle.height / 2 <= radius

    if x_collision and y_collision:
        return True

    x_collision = abs(circle.x - rectangle.x) - rectangle.width / 2 <= radius
    y_collision = rectangle.y - rectangle.height / 2 < circle.y < rectangle.y + rectangle.height / 2

    if x_collision and y_collision:
        return True

    return False
