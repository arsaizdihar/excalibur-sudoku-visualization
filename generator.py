import json

board = [[0 for _ in range(9)] for _ in range(9)]
arrows = []
i = 0
print("Board")
while i < 9:
    try:
        numbers = list(map(int, input(f"line {i}: ")))
        if len(numbers) != 9:
            raise ValueError("Invalid line")
        board[i] = numbers
        i += 1
    except ValueError as e:
        continue

print("Arrows")
while True:
    try:
        length = int(input("arrow len: "))
        if length < 1:
            break
        head_pos = tuple(map(int, input("arrow head pos: ")))
        if len(head_pos) != 2:
            raise ValueError("Invalid arrow")
        poss = []
        for i in range(length):
            poss.append(tuple(map(int, input(f"arrow pos {i}: "))))
            if len(poss[i]) != 2:
                raise ValueError("Invalid arrow")
        arrows.append((head_pos, poss))
    except ValueError as e:
        continue

filename = input("filename: ")
with open(filename, 'w') as f:
    json.dump({"board": board, "arrows": arrows}, f, indent=2)
