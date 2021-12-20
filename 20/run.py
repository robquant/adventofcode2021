def minmax(it):
    min = max = None
    for val in it:
        if min is None or val < min:
            min = val
        if max is None or val > max:
            max = val
    return min, max


def key_for_pos(x, y, image_with_default):
    image, default = image_with_default
    key = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            key <<= 1
            key |= image.get((x + dx, y + dy), default)
    return key


def enhance(image_with_default, algorithm):
    enhanced = {}
    image = image_with_default[0]
    min_x, max_x = minmax(x for x, _ in image.keys())
    min_y, max_y = minmax(y for _, y in image.keys())
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            enhanced[(x, y)] = algorithm[key_for_pos(x, y, image_with_default)]
    new_default = algorithm[key_for_pos(min_x - 10, min_y - 10,
                                        image_with_default)]
    return (enhanced, new_default)


def count_lit(image):
    return sum(image.values())


image = {}
with open("input.txt") as inf:
    d = {'#': 1, '.': 0}
    algorithm = [d[c] for c in inf.readline().rstrip('\n')]
    inf.readline()
    for y, line in enumerate(inf.readlines()):
        for x, c in enumerate(line.rstrip('\n')):
            image[(x, y)] = d[c]

image_with_default = (image, 0)
for i in range(50):
    image_with_default = enhance(image_with_default, algorithm)
    if i == 1:
        print(f"Lit after {i+1} rounds: {count_lit(image_with_default[0])}")
print(f"Lit after {i+1} rounds: {count_lit(image_with_default[0])}")
