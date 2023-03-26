"""Основная программа"""

import argparse
import os

from typing import Union, Any

from maze import generate, best_first_search
from visualization import visualization_init



def check_fields(args: Any) -> bool:
    """Проверка переданных аргументов"""
    """
    if args.width not in range(3, 91):
        print("Empty")  # TODO
        return False
    """
    return True


def parse_args() -> Union[bool, str]:
    """Обработка параметров командной строки"""
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Сжатие изображений на основе"
                                                 " квадродеревьев")

    parser.add_argument("-w", "--width", dest="width", type=int,
                        help="Ширина лабиринта (от 3 до 90)",
                        required=True)  # TODO

    parser.add_argument("--height", dest="height", type=int,
                        help="Высота лабиринта (от 3 до 80)",
                        required=True)  # TODO

    # В эту переменную попадает результат разбора аргументов командной строки.
    args = parser.parse_args()

    # Проверяем аргументы командной строки
    if check_fields(args):
        maze = generate(args.width, args.height)
        solution = best_first_search(maze)
        visualization_init(maze, solution)
    else:
        print("Переданы неверные аргументы.")


def main():
    """Точка входа"""
    parse_args()


if __name__ == "__main__":
    main()
