"""Основная программа"""

import os
import argparse

from typing import Any

from maze import generate, best_first_search
from visualization import visualization_init
from reading_maze_from_file import reading_maze_from_text, \
    reading_maze_from_image


def check_fields(args: Any) -> bool:
    """
    Проверка переданных аргументов
    :param args: Аргументы
    :return: Булевое значение
    """

    if args.width_height:
        if args.width_height[0] not in range(3, 401):
            print("Ширина лабиринта должна быть от 3 до 400.")
            return False

        if args.width_height[1] not in range(3, 401):
            print("Высота лабиринта должна быть от 3 до 400.")
            return False

    if args.load_maze_text and (not os.path.exists(
            args.load_maze_text) or not args.load_maze_text.endswith('.txt')):
        print("Неверный файл.")
        return False

    if args.load_maze_image and (not os.path.exists(
            args.load_maze_image) or not args.load_maze_image.endswith(
            ('.png', '.jpg'))):
        print("Неверный файл.")
        return False

    if args.save_maze_image and (args.save_maze_image[-3:] not in ["jpg",
                                                                   "png"] or
                                 "/" in args.save_maze_image):
        return False

    if args.save_maze_text and (args.save_maze_text[-3:] not in ["txt"] or
                                "/" in args.save_maze_text):
        return False

    return True


def parse_args() -> None:
    """
    Обработка параметров командной строки
    :return: None
    """
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Сжатие изображений на основе"
                                                 " квадродеревьев")

    # Метод add_mutually_exclusive_group() создает взаимоисключающую группу
    # параметров командной строки
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-wh', '--width_height', nargs=2, dest="width_height",
                       type=int,help='Ширина и высота лабиринта (от 3 до 400)')

    group.add_argument('-lmi', '--load-maze-image', dest="load_maze_image",
                       type=str,
                       help='Загрузка лабиринта из изображения')

    group.add_argument('-lmt', '--load-maze-text', dest="load_maze_text",
                       type=str,
                       help='Загрузка лабиринта из текста')

    parser.add_argument("-sol", "--solution", dest="solution",
                        action="store_true", help="Решение лабиринта")

    parser.add_argument("-smi", "--save-maze-image", dest="save_maze_image",
                        type=str, help="Выходной файл для сохранения лабиринта"
                                       "в виде изображения (jpg/png)")

    parser.add_argument("-smt", "--save-maze-text", dest="save_maze_text",
                        type=str, help="Выходной файл для сохранения лабиринта"
                                       "в виде текста (txt)")

    # В эту переменную попадает результат разбора аргументов командной строки.
    args = parser.parse_args()

    # Проверяем аргументы командной строки
    if check_fields(args):
        maze = [[]]

        if args.width_height:
            maze = generate(args.width_height[0], args.width_height[1])

        elif args.load_maze_text:
            maze = reading_maze_from_text(args.load_maze_text)

        elif args.load_maze_image:
            try:
                maze = reading_maze_from_image(args.load_maze_image)
            except ValueError:
                pass

        if args.solution:
            try:
                solution = best_first_search(maze)
                visualization_init(maze, solution, args.save_maze_image,
                                   args.save_maze_text)
            except (IndexError, KeyError):
                print("Ошибка выполнения. Завершение программы...")
        else:
            visualization_init(maze, img_path=args.save_maze_image,
                               text_path=args.save_maze_text)
    else:
        print("Переданы неверные аргументы.")


def main() -> None:
    """
    Точка входа
    :return: None
    """
    parse_args()


if __name__ == "__main__":
    main()
