import pygame as pg

# Задаем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def print_maze(maze):
    # Проверяем указатель на None
    if maze is None:
        return

    # Построчно считываем и выводим в консоль
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end='')
        print()


def visualize_maze(screen, maze, scale):
    # Проверяем указатель на None
    if maze is None:
        return

    # Рисуем лабиринт
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                pg.draw.rect(screen, BLACK,
                             (j * scale, i * scale, scale, scale))
            else:
                pg.draw.rect(screen, WHITE, (j * scale, i * scale, scale,
                                             scale))

    # Обновляем экран
    pg.display.flip()

    # Выходим из Pygame
    # pygame.quit()
    return screen


def draw_solution(screen, solution, scale):
    # Проверяем указатель на None
    if solution is None:
        return

    # Рисуем решение лабиринта
    for point in solution:
        pg.draw.rect(screen, RED,
                     (point[1] * scale, point[0] * scale, scale, scale))

    # Обновляем экран
    pg.display.flip()

    # Ожидаем закрытия окна
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

    # Выходим из Pygame
    pg.quit()


def visualization_init(maze: [[]], solution: [()]):
    # Инициализируем Pygame
    pg.init()

    width = len(maze[0])
    height = len(maze)

    scale = 1000 // height if height >= width else 1900 // width

    # Создаем окно
    screen = pg.display.set_mode((width * scale, height * scale))
    visualize_maze(screen, maze, scale)
    draw_solution(screen, solution, scale)
