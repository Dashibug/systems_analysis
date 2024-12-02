#!/bin/python

# class Lesson1:
#     def __init__(self, num_top):
#         self.num_top = num_top
#         self.matrix = [[0] * num_top for i in range(num_top)]
#
#     def add_edge(self, v1, v2, weight = 1):
#         if v1 == v2:
#             print("ведет в саму себя")
#         else:
#             self.matrix[v1-1][v2-2] = weight
#             self.matrix[v2-1][v1-1] = weight
#
#     def print_matrix(self):
#         for row in self.matrix:
#             print(row)
#
#     def is_connected(self, v1, v2):
#         return self.matrix[v1][v2] != 0
#
# g = Lesson1(8)
# g.add_edge(1, 2)
# g.add_edge(2, 3)
# g.add_edge(2, 4)
# g.add_edge(4, 5)
# g.add_edge(4, 6)
# g.add_edge(3, 7)
# g.add_edge(3, 8)
# g.print_matrix()

import csv
import argparse


# def task(file: str, row: int, column: int):
#     try:
#         with open(file, 'r') as csvfile:
#             reader = csv.reader(csvfile, delimiter=',')
#             data = list(reader)
#             return data[row - 1][column - 1]
#     except IndexError:
#         return f"Ошибка: указанная строка {row} или столбец {column} вне диапазона."
#     except FileNotFoundError:
#         return "Ошибка: файл не найден."
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Извлечение значения из CSV-файла по строке и столбцу")
#     parser.add_argument('filepath', type=str, help='Полный путь к CSV-файлу')
#     parser.add_argument('row', type=int, help='Номер строки (начиная с 1)')
#     parser.add_argument('column', type=int, help='Номер столбца (начиная с 1)')
#     args = parser.parse_args()
#     result = task(args.filepath, args.row, args.column)
#     print(result)



from collections import defaultdict
import csv


def task(csv_str: str):
    children = defaultdict(list)
    parents = defaultdict(list)

    reader = csv.reader(csv_str.splitlines(), delimiter=',')

    for line in reader:
        if not line:
            continue

        a, b = line
        children[a].append(b)
        parents[b].append(a)

        if a not in parents:
            parents[a] = []

        if b not in children:
            children[b] = []

    root = next(key for key in parents if not parents[key])
    leaves = [key for key in children if not children[key]]

    certain_ans = {key: {'r1': set(children[key]),
                         'r2': set(parents[key]),
                         'r3': set(),
                         'r4': set(),
                         'r5': set()}
                   for key in parents}

    stack = [root]
    while stack:
        cur_node = stack.pop()
        for child in children[cur_node]:
            certain_ans[child]['r4'] |= certain_ans[cur_node]['r2'] | certain_ans[cur_node]['r4']
            certain_ans[child]['r5'] |= certain_ans[cur_node]['r1'] - {child, }
            stack.append(child)

    stack = list(leaves)
    while stack:
        cur_node = stack.pop()
        for parent in parents[cur_node]:
            certain_ans[parent]['r3'] |= certain_ans[cur_node]['r1'] | certain_ans[cur_node]['r3']
            if parent not in stack:
                stack.append(parent)

    fields = ('r1', 'r2', 'r3', 'r4', 'r5')
    csv_output = '\n'.join([','.join([str(len(certain_ans[node][field])) for field in fields]) for node in sorted(certain_ans)]) + '\n'

    return csv_output

if __name__ == '__main__':
    # Пример использования функции
    input_data = "1,2\n1,3\n3,4\n3,5\n"
    print(task(input_data))