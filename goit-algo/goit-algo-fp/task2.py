# pythagoras_tree_min.py
# Дерево Піфагора. Питає лише рівень рекурсії.
import turtle

def draw_tree(t, length, depth, angle=45, ratio=0.72):
    if depth == 0 or length < 1:
        return
    t.forward(length)
    t.left(angle)
    draw_tree(t, length * ratio, depth - 1, angle, ratio)
    t.right(angle)
    t.right(angle)
    draw_tree(t, length * ratio, depth - 1, angle, ratio)
    t.left(angle)
    t.backward(length)

def main():
    while True:
        try:
            depth = int(input("Вкажіть рівень рекурсії (напр. 10): ").strip())
            if depth < 0:
                print("Глибина має бути невід'ємною.")
                continue
            break
        except ValueError:
            print("Потрібне ціле число.")

    screen = turtle.Screen()
    screen.setup(1000, 800)
    screen.bgcolor("white")
    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.pensize(2)
    t.color("#8B3A3A")
    t.penup()
    t.goto(0, -screen.window_height()//2 + 60)
    t.setheading(90)
    t.pendown()

    draw_tree(t, length=120, depth=depth)
    t.hideturtle()
    print("Готово. Закрийте вікно, щоб завершити.")
    screen.mainloop()

if __name__ == "__main__":
    main()
