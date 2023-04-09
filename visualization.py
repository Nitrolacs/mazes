"""Функции для визуализации лабиринта и его решения"""

import pygame as pg

# Задаем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def visualize_maze(screen: pg.display, maze: [[]], scale: int) -> None:
    """
    Визуализация лабиринта
    :param screen: Окно, в котором будет рисоваться лабиринт
    :param maze: Двумерный массив
    :param scale: Модификатор размера изображения
    :return: None
    """

    # Проверяем указатель на None
    if maze is None:
        return

    # Рисуем лабиринт
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == '█':
                pg.draw.rect(screen, BLACK,
                             (j * scale, i * scale, scale, scale))
            else:
                pg.draw.rect(screen, WHITE, (j * scale, i * scale, scale,
                                             scale))

    # Обновляем экран
    pg.display.flip()


def draw_solution(screen, solution, scale) -> None:
    """
    Визуализация решения лабиринта.
    :param screen: Окно, в котором будет рисоваться решение.
    :param solution: Решение лабиринта.
    :param scale: Модификатор размера лабиринта.
    :return: None
    """
    # Проверяем указатель на None
    if solution is None:
        return

    # Рисуем решение лабиринта
    for point in solution:
        pg.draw.rect(screen, RED,
                     (point[1] * scale, point[0] * scale, scale, scale))
        # Обновляем экран
        pg.display.flip()
        pg.time.wait(30)


def visualization_init(maze: [[]], solution: [()] = None,
                       img_path: str = None, text_path: str = None) -> None:
    """
    Инициализация визуализации.
    :param maze: Лабиринт
    :param solution: Решение
    :param img_path: Путь до изображения
    :param text_path: Путь до текстового файла
    :return: None
    """
    # Инициализируем Pygame
    pg.init()
    width = len(maze[0])
    height = len(maze)

    scale = 1000 // height if height >= width else 1900 // width

    # Создаем окно
    screen = pg.display.set_mode((width * scale, height * scale))
    visualize_maze(screen, maze, scale)

    if solution:
        print(f"Путь от начальной до конечной точки:\n{solution}")
        draw_solution(screen, solution, scale)

    if img_path:
        print(f"Изображение лабиринта сохранено в файл {img_path} в папке "
              f"maze_image")
        pg.image.save(screen, "maze_image/" + img_path)

    if text_path:
        with open("maze_text/" + text_path, "w", encoding="utf-8") as file:
            for row in maze:
                file.write(''.join(row) + "\r\n")
        print(f"Лабиринт в текстовом формате сохранён в файл {text_path}"
              f" в папке maze_text")

    # Ожидаем закрытия окна
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

    # Выходим из Pygame
    pg.quit()
