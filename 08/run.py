import sys
from collections import Counter
import itertools

infile = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
inputs = []

for line in open(infile):
    digits, output_values = line.split("|")
    output_values = output_values.split()
    digits = digits.split()
    inputs.append((digits, output_values))

number_to_segments = {
    0: tuple("abcefg"),
    1: tuple("cf"),
    2: tuple("acdeg"),
    3: tuple("acdfg"),
    4: tuple("bcdf"),
    5: tuple("abdfg"),
    6: tuple("abdefg"),
    7: tuple("acf"),
    8: tuple("abcdefg"),
    9: tuple("abcdfg"),
}

segments_to_number = {v: k for k, v in number_to_segments.items()}


def part1(inputs):
    count = 0
    len_unique_segments = {
        len(number_to_segments[1]),
        len(number_to_segments[4]),
        len(number_to_segments[7]),
        len(number_to_segments[8]),
    }
    for _, output_values in inputs:
        for value in output_values:
            if len(value) in len_unique_segments:
                count += 1

    return count


# def part_2():
#     counts_per_segment = Counter()
#     for s in number_to_segments.values():
#         counts_per_segment.update(s)
#     print(counts_per_segment)
# 4 -> e, 6 -> b, 9 -> f,


def is_mapping_correct(mapping, digits):
    for digit in digits:
        mapped = tuple(sorted(mapping[c] for c in digit))
        if not mapped in segments_to_number:
            return False
    return True


def mapped_digit(mapping, digit):
    mapped = tuple(sorted(mapping[c] for c in digit))
    return segments_to_number[mapped]


print("Part 1:", part1(inputs))


# Brute force a soultion. Try out all possible mappings
total = 0
orig = list("abcdefg")
mappings = [dict(zip(mapping, orig)) for mapping in itertools.permutations(orig, 7)]
for digits, output_values in inputs:
    for mapping in mappings:
        if is_mapping_correct(mapping, digits):
            number = int(
                "".join(str(mapped_digit(mapping, digit)) for digit in output_values)
            )
            total += number
            break

print("Part 2: ", total)

