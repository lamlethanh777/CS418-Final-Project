import json

mapping = {}

# region 001
mapping["Sach-Nom-Cong-Giao-1995-001"] = {
    "page_pairs": [
        (4, 453),
    ]
}

for i in range(8, 225):
    mapping["Sach-Nom-Cong-Giao-1995-001"]["page_pairs"].append((i, 452 + 8 - i))


# region 002
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


# region 004 done
mapping["Sach-Nom-Cong-Giao-1995-004"] = {
    "page_pairs": [
        (4, 189),
        (23, 187),
    ]
}
# 0.08 for 2 sides

for i in range(24, 64):
    mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((i, 187 + 23 - i))

for i in range(64, 81):
    mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((i, 145 + 64 - i))

for i in range(81, 99):
    mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((i, 127 + 81 - i))

# mapping["Sach-Nom-Cong-Giao-1995-004"]["page_pairs"].append((range(289, 320), range(343, 322, -1)))



# region 005

# region 012

# region 049 done
mapping["Sach-Nom-Cong-Giao-1995-049"] = {
    "page_pairs": [
        (22, 591),
        # (55,556),
    ]
}

for i in range(23, 55):
    mapping["Sach-Nom-Cong-Giao-1995-049"]["page_pairs"].append((i, 591+22 - i))

for i in range(55, 300):
    mapping["Sach-Nom-Cong-Giao-1995-049"]["page_pairs"].append((i, 55+556 - i))


# Save to JSON
with open("../extracted_imgs/page_ranges.json", "w", encoding="utf-8") as json_file:
    json.dump(mapping, json_file, ensure_ascii=False, indent=4)