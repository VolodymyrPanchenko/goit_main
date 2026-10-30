import turtle

def koch_curve(t, order, length):
    if order == 0:
        t.forward(length)
    else:
        koch_curve(t, order-1, length/3)
        t.left(60)
        koch_curve(t, order-1, length/3)
        t.right(120)
        koch_curve(t, order-1, length/3)
        t.left(60)
        koch_curve(t, order-1, length/3)

def draw_koch_snowflake(order, size=300):
    wn = turtle.Screen()
    wn.bgcolor("white")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    turtle.tracer(0, 0)  # ускоряем отрисовку, отключив покадровую анимацию [web:49]

    # начальная позиция, чтобы фигура была по центру
    t.penup()
    t.goto(-size/2, size/3.5)
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)  # поворот для равностороннего треугольника [web:11]

    turtle.update()   # одно обновление экрана после рисования [web:49]
    turtle.done()

if __name__ == "__main__":
    try:
        level = int(input("Введите уровень рекурсии (0–6): ").strip())
        draw_koch_snowflake(level, 300)
    except ValueError:
        print("Введите целое число.")
