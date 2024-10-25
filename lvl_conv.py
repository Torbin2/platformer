level = [[0, 0, 0, 0, 1, 6, 0, 2, 2, 9, 9, 9, 0, 8, 2, 1, 0, 0, 1, 0, 0, 2, 2, 0, 0, 0, 0, 8, 2, 1, 0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 8, 2, 2, 0, 0, 0, 1, 1, 1, 2, 2, 0, 0, 0, 8, 1, 2, 1, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 8, 1, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 8, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 8, 2, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 2, 0, 8, 2, 0, 0, 0, 1, 0, 3, 1, 0, 0, 2, 2, 0, 8, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 2, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 8, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 8, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 0, 0, 0, 2, 2, 9, 9, 9, 0, 8, 2, 1, 1, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 8, 2, 1, 1, 1, 0, 0, 1, 2, 2, 2, 0, 0, 0, 8, 2, 2, 1, 1, 0, 0, 1, 1, 2, 0, 0, 0, 0, 8, 1, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 8, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 8, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 8, 2, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 8, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 8, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2]]

text = "[\n"
for num, i in enumerate(level):
    text += "[\n"
    for num, x in enumerate(i):
        text += str(x)
        text += ", "
        if num % 14 == 13:
            text += "\n"
    text += "],\n"
text += "]"
print(text)
