import random
import pygame

from queue import PriorityQueue


def generate(width, height):
    # Проверим ограничения параметров на 0
    if (width < 1) or (height < 1):
        return None

    top_limit = 2 ** 32 - 1
    # Проверим ограничения по максимальному допустимому размеру
    if ((top_limit - 1) // 2 <= width) or ((top_limit - 1) // 2 <= height):
        return None

    # Инициализируем размер конечной матрицы maze
    # Ячейки будут представлять собой фрагменты 2x2 + 1 одно значение
    # сверху и слева для стен
    output_height = height * 2 + 1
    output_width = width * 2 + 1
    # Инициализируем лабиринт
    maze = [['#' for j in range(output_width)] for i in range(output_height)]

    # Инициализируем построчно пустой лабиринт со стенами по периметру
    # и "опорами" (стенами) в нижнем правом углу ячеек 2x2
    # #######
    # #     #
    # # # # #
    # #     #
    # #######
    for i in range(output_height):
        for j in range(output_width):
            # Если этот элемент в строке является ячейкой в левом верхнем
            # угле области 2x2 - то это пустая ячейка в лабиринте
            if (i % 2 == 1) and (j % 2 == 1):
                maze[i][j] = ' '
            # Если это область для стены справа или область для стены снизу
            # - то инициализируем этот элемент пустой ячейкой в лабиринте
            elif (((i % 2 == 1) and (j % 2 == 0) and (j != 0) and (
                    j != output_width - 1)) or (
                          (j % 2 == 1) and (i % 2 == 0) and (i != 0) and (
                          i != output_height - 1))):
                maze[i][j] = ' '
            else:
                # Во всех остальных случаях устанавливаем стену
                maze[i][j] = '#'

    # 1. Создайте первую строку лабиринта. Ни одна ячейка не будет принадлежать
    # какому - либо множеству.
    # Инициализируем вспомогательную строку, которая будет содержать в себе
    # принадлежность ко множеству для ячейки из алгоритма
    # 0 - будет означать, что ячейка не принадлежит никакому множеству
    row_set = [0] * width
    # И инициализируем счетчик для множеств
    set = 1
    # Инициализируем генератор случайных чисел
    random.seed()

    # Организуем цикл алгоритма Эйлера
    for i in range(height):
        # 2. Присвоить каждой ячейке, которая не входит ни в одно множество,
        # своё уникальное множество.
        for j in range(width):
            if row_set[j] == 0:
                row_set[j] = set
                set += 1
        # 3. Создайте правые стены для ячеек, двигаясь слева направо,
        # следующим образом :
        for j in range(width - 1):
            # Случайным образом решите, добавлять стену или нет
            right_wall = random.randint(0, 1)
            # Если текущая ячейка и ячейка справа являются членами одного и того
            # же множества, всегда создавайте между ними стену
            # (это предотвратит петли)
            if right_wall == 1 or row_set[j] == row_set[j + 1]:
                # верхний ряд в i-ом ряду ячеек 2x2, Правый столбец в (i;j)
                # ячейке 2x2*
                maze[i * 2 + 1][j * 2 + 2] = '#'  # Создаём стену
            else:
                # Если вы решите не добавлять стену, то объедините множества,
                # к которым относятся текущая ячейка и ячейка справа
                changing_set = row_set[j + 1]
                for l in range(width):
                    if row_set[l] == changing_set:
                        row_set[l] = row_set[j]

        # 4. Создайте нижние стены, двигаясь слева направо:
        for j in range(width):
            # Случайным образом решите, добавлять нижнюю стену или нет.
            bottom_wall = random.randint(0, 1)
            # Если ячейка является единственным членом своего множества, то не
            # создавайте нижнюю стену
            count_current_set = sum(
                [row_set[l] == row_set[j] for l in range(width)])
            # Если ячейка является единственным членом своего множества, которая
            # не имеет нижней стены, то не создавайте нижнюю стену
            if bottom_wall == 1 and count_current_set != 1:
                maze[i * 2 + 2][j * 2 + 1] = '#'

        # 5. Решите, продолжать добавлять строки или остановиться и завершить
        # лабиринт. Если вы решите добавить еще одну строку:
        if i != height - 1:
            # Важно: Убедитесь, что каждая область имеет по крайней мере одну
            # ячейку без нижней стены(это предотвратит создание
            # изолированных областей)
            for j in range(width):
                count_hole = sum([maze[i * 2 + 2][l * 2 + 1] == ' ' and row_set[
                    l] == row_set[j] for l in range(width)])
                if count_hole == 0:
                    maze[i * 2 + 2][j * 2 + 1] = ' '
            # * скопируйте текущую строку
            # * удалите в новой строку все правые стены
            # Правые стенки в инициализированном массиве у нас уже отсутствуют
            # в каждой новой строке
            # * удалите ячейки с нижней стеной из их множества
            for j in range(width):
                # Проверим наличие нижней стены у текущего ряда
                if maze[i * 2 + 2][j * 2 + 1] == '#':
                    # Если стенка есть, то удаляем ячейку из множества
                    row_set[j] = 0
                    # * удалите все нижние стены
            # Нижние стены в каждом новом ряду ячеек отсутствуют (заложено при
            # инициализации)

        # * продолжить с шага 2.

    # * Если вы решили закончить лабиринт:
    # *добавьте нижнюю стену каждой ячейке
    # Нижняя стена построена при инициализации лабиринта
    # * перемещайтесь слева направо:
    for j in range(width - 1):
        # Если текущая ячейка
        # и ячейка справа являются членами разных множеств, то:
        if row_set[j] != row_set[j + 1]:
            # *удалить правую стену
            maze[-2][j * 2 + 2] = ' '
            # * объедините множества, к которым принадлежат текущая ячейка и
            # ячейка справа
            # Это делать не обязательно, так как row_set мы больше не будем
            # использовать,
            # а все множества в конечном итоге станут одним, после удаления стен
            # * вывод итоговой строки

    # вернём полученный лабиринт
    return maze


def print_maze(maze):
    # Проверяем указатель на None
    if maze is None:
        return

    # Построчно считываем и выводим в консоль
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end='')
        print()


def visualize_maze_pygame(maze):
    # Проверяем указатель на None
    if maze is None:
        return

    # Инициализируем Pygame
    pygame.init()

    # Создаем окно
    screen = pygame.display.set_mode((len(maze[0]) * 20, len(maze) * 20))

    # Задаем цвета
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Рисуем лабиринт
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                pygame.draw.rect(screen, BLACK, (j * 20, i * 20, 20, 20))
            else:
                pygame.draw.rect(screen, WHITE, (j * 20, i * 20, 20, 20))

    # Обновляем экран
    pygame.display.flip()

    # Выходим из Pygame
    # pygame.quit()
    return screen


def draw_solution_pygame(solution, screen):
    # Проверяем указатель на None
    if solution is None:
        return

    RED = (255, 0, 0)

    # Рисуем решение лабиринта
    for point in solution:
        pygame.draw.rect(screen, RED,
                         (point[1] * 20, point[0] * 20, 20, 20))

    # Обновляем экран
    pygame.display.flip()

    # Ожидаем закрытия окна
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Выходим из Pygame
    pygame.quit()


def best_first_search(maze):
    start = (1, 1)
    goal = (len(maze) - 2, len(maze[0]) - 2)

    # Создаем очередь с приоритетами и добавляем в нее начальную точку
    frontier = PriorityQueue()
    frontier.put(start, False)

    # Словарь для хранения путей
    came_from = {start: None}

    while not frontier.empty():
        # Получаем следующую точку из очереди с приоритетами
        current = frontier.get()

        # Если мы достигли цели, то выходим из цикла
        if current == goal:
            break

        # Получаем соседние точки
        for next in get_neighbors(current, maze):
            # Если мы еще не были в этой точке
            if next not in came_from:
                # Вычисляем приоритет для этой точки
                priority = heuristic(goal, next)
                # Добавляем эту точку в очередь с приоритетами
                frontier.put(next, priority)
                # Добавляем путь до этой точки в словарь came_from
                came_from[next] = current

    # Восстанавливаем путь до цели из словаря came_from
    return reconstruct_path(came_from, start, goal)


def get_neighbors(pos, maze):
    neighbors = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        if maze[neighbor[0]][neighbor[1]] != '#':
            neighbors.append(neighbor)
    return neighbors


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


maze = generate(30, 23)
print_maze(maze)
screen = visualize_maze_pygame(maze)
solution = best_first_search(maze)
draw_solution_pygame(solution, screen)
