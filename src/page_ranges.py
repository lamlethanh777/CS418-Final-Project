import json

mapping = {}

# 001
mapping["Sach-Nom-Cong-Giao-1995-001"] = {
    "page_pairs": [
        (4, 453),
    ]
}

for i in range(8, 225):
    mapping["Sach-Nom-Cong-Giao-1995-001"]["page_pairs"].append((i, 452 + 8 - i))


# 002
mapping["Sach-Nom-Cong-Giao-1995-002"] = {
    "page_pairs": [
        (9, (125, 124)),
        (10, (123, 122, 121, 120)),
        (11, (120, 119, 118, 117, 116)),
        (12, (116, 115, 114, 113, 112)),
        (13, (111, 110, 109, 108)),
        (14, (108, 107, 106, 105, 104)),
        (15, (104, 103, 102, 101, 100)),
        (16, (100, 99, 98, 97)),
        (17, (97, 96, 95, 94, 93)),
        (18, (93, 92, 91, 90, 89)),
        (19, (89, 88, 87, 86, 85)),
        (20, (85, 84, 83, 82)),
        (21, (82, 81, 80, 79)),
        (22, (79, 78, 77, 76, 75)),
        (23, (74, 73, 72, 71)),
        (24, (71, 70, 69, 68)),
        (25, (68, 67, 66, 65, 64)),
        (26, (63, 62, 61)),
        (27, (61, 60, 59, 58)),
        (28, (57, 56, 55)),
        (29, (55, 54, 53, 52, 51)),
        (30, (51, 50)),
        (31, (50, 49, 48, 47)),
        (32, (46, 45, 44, 43)),
        (33, (42, 41, 40, 39)),
        (34, (38, 37, 36)),
    ],
}


# 004
mapping["Sach-Nom-Cong-Giao-1995-004"] = {
    "page_pairs": [
        (2, 189),
        (23, 187),
    ]
}

for i in range(24, 99):
    mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((i, 186 + 24 - i))

mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((291, 345))

for i in range(291, 323):
    mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((i, 344 + 291 - i))

# 005

# 012

# 049
mapping["Sach-Nom-Cong-Giao-1995-049"] = {
    "page_pairs": [
        (22, 595),
    ]
}

for i in range(23, 302):
    mapping["Sach-Nom-Cong-Giao-1995-049"]["page_pairs"].append((i, 594 + 23 - i))


# Save to JSON
with open("../extracted_imgs/page_ranges.json", "w", encoding="utf-8") as json_file:
    json.dump(mapping, json_file, ensure_ascii=False, indent=4)

