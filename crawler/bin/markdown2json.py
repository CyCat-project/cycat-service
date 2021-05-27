import sys

md_table = sys.stdin.readlines()
print(md_table)

result = []
for n, line in enumerate(md_table[1:-1]):
    data = {}
    if n == 0:
        header = [t.strip() for t in line.split('|')[1:-1]]
    if n > 1:
        values = [t.strip() for t in line.split('|')[1:-1]]
        for col, value in zip(header, values):
            data[col] = value
        result.append(data)

print(result)
