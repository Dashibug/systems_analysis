import csv
import math


def task(csv_str: str) -> float:

    lines = csv_str.strip().split('\n')
    reader = csv.reader(lines)

    data = [list(map(int, row)) for row in reader]
    row_count = len(data)

    total_entropy = 0

    for row in data:
        for value in row:
            if value > 0:
                probability = value / (row_count - 1)
                total_entropy += -probability * math.log2(probability)

    return round(total_entropy, 1)


if __name__ == "__main__":
    csv_input = """1,0,4,0,0
                   2,1,2,0,0
                   2,1,0,1,1
                   0,1,0,1,1
                   0,1,0,2,1
                   0,1,0,2,1"""

    result = task(csv_input)
    print(f"Энтропия: {result}")
