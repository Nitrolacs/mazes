"""Основная программа"""

import argparse

from typing import Any

from maze import generate, best_first_search
from visualization import visualization_init


def check_fields(args: Any) -> bool:
    """Проверка переданных аргументов"""

    if args.width not in range(3, 401):
        print("Ширина лабиринта должна быть от 3 до 400.")
        return False

    if args.height not in range(3, 401):
        print("Высота лабиринта должна быть от 3 до 400.")
        return False

    if args.save_maze_image and args.save_maze_image[-3:] not in ["jpg", "png"]:
        return False

    if args.save_maze_text and args.save_maze_text[-3:] not in ["txt"]:
        return False

    return True


def parse_args() -> None:
    """Обработка параметров командной строки"""
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Сжатие изображений на основе"
                                                 " квадродеревьев")

    parser.add_argument("-wh", "--width", dest="width", type=int,
                        help="Ширина лабиринта (от 3 до 400)",
                        required=True)

    parser.add_argument("-hg", "--height", dest="height", type=int,
                        help="Высота лабиринта (от 3 до 400)",
                        required=True)

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
        maze = generate(args.width, args.height)
        if args.solution:
            solution = best_first_search(maze)
            visualization_init(maze, solution, args.save_maze_image,
                               args.save_maze_text)
        else:
            visualization_init(maze, img_path=args.save_maze_image,
                               text_path=args.save_maze_text)
    else:
        print("Переданы неверные аргументы.")


def main():
    """Точка входа"""
    parse_args()


if __name__ == "__main__":
    main()
