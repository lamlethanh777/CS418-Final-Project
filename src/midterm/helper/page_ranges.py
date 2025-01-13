import json

mapping = {}

# region 001
mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 001 - Van Thanh Ca Giuse"] = {"page_pairs": [([4], [433])]}

for i in range(8, 102):
    mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 001 - Van Thanh Ca Giuse"]["page_pairs"].append(([i], [432 + 8 - i]))

for i in range(104, 221):
    mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 001 - Van Thanh Ca Giuse"]["page_pairs"].append(([i], [338 + 104 - i]))

# endregion

# region 002 done
mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 002 - Ngam Thuong Khos"] = {
    "page_pairs": [
        ([9], [125, 124]),
        ([10], [123, 122, 121, 120]),
        ([11], [120, 119, 118, 117, 116]),
        ([12], [116, 115, 114, 113, 112]),
        ([13], [111, 110, 109, 108]),
        ([14], [108, 107, 106, 105, 104]),
        ([15], [104, 103, 102, 101, 100]),
        ([16], [100, 99, 98, 97]),
        ([17], [97, 96, 95, 94, 93]),
        ([18], [93, 92, 91, 90, 89]),
        ([19], [89, 88, 87, 86, 85]),
        ([20], [85, 84, 83, 82]),
        ([21], [82, 81, 80, 79]),
        ([22], [79, 78, 77, 76, 75]),
        ([23], [74, 73, 72, 71]),
        ([24], [71, 70, 69, 68]),
        ([25], [68, 67, 66, 65, 64]),
        ([26], [63, 62, 61]),
        ([27], [61, 60, 59, 58]),
        ([28], [57, 56, 55]),
        ([29], [55, 54, 53, 52, 51]),  # in book: 53 -> 51 only
        ([30], [51, 50]),
        ([31], [50, 49, 48, 47]),
        ([32], [46, 45, 44, 43]),
        ([33], [42, 41, 40, 39]),
        ([34], [38, 37, 36]),
    ],
}

# endregion

# region 004 done, may overlap
mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"] = {"page_pairs": [([4], [189])]}
for i in range(23, 63):
    mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([i], [187 + 23 - i]))
# somehow skip page_146 -> actually 2 pages
mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([63], [147, 146]))

for i in range(64, 80):
    mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([i], [145 + 64 - i]))
# somehow skip page_128 -> actually 2 pages
mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([80], [129, 128]))

for i in range(81, 98):
    mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([i], [127 + 81 - i]))
# page_109 has not been counted -> actually 2 pages
mapping["Prj_55g_Tho_APCS2_Sách Nôm công giáo 1995 - 004 - Hoi Dong Tu Giao"]["page_pairs"].append(([98], [110, 109]))

# endregion

# region 005 done
mapping["Sach-Nom-Cong-Giao-1995-005"] = {"page_pairs": []}

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [673 + 12 - i]) for i in range(12, 15)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].append(([15], [669, 668]))

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [667 + 16 - i]) for i in range(16, 35)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([35], [648, 647]), ([36], [647, 646])]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [645 + 37 - i]) for i in range(37, 111)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [
        ([111], [572, 571]),
        ([112], [571, 570]),
        ([113], [570, 569]),
        ([114], [569, 568]),
        ([115, 116], [568, 567]),
        ([117], [567, 566]),
        ([118, 119, 120], [566, 565]),
        ([121], [564]),
        ([122], [563]),
        ([123], [562]),
        ([124], [561, 560]),
        ([125], [560, 559]),
        ([126], [559, 558]),
        ([127], [557, 556]),
    ]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [555 + 129 - i]) for i in range(129, 143)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [540 + 143 - i]) for i in range(143, 154)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [527 + 154 - i]) for i in range(154, 165)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [515 + 165 - i]) for i in range(165, 174)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [505 + 174 - i]) for i in range(174, 183)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [494 + 183 - i]) for i in range(183, 258)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].append(([258, 259], [419]))

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [418 + 260 - i]) for i in range(260, 322)]
)

mapping["Sach-Nom-Cong-Giao-1995-005"]["page_pairs"].extend(
    [([i], [355 + 322 - i]) for i in range(322, 338)]
)

# cuốn 5: page_182 (179 trong sách gốc) - page_183 (182 trong sách gốc)
# 	page_527 (526 trong sách gốc) - page_530 (527 trong sách gốc)

# endregion

# region 012 done
mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 001 - Van Thanh Ca Giuse"] = {"page_pairs": []}

mapping["Prj_55g_Lam_APCS2_Sách Nôm công giáo 1995 - 001 - Van Thanh Ca Giuse"]["page_pairs"].extend(
    [
        ([18], [103, 102]),
        ([19], [102, 101]),
        ([20], [101, 100, 99]),
        ([21], [98, 97]),
        ([22], [97, 96]),
        ([23], [96, 95, 94]),
        ([24], [94, 93, 92]),
        ([25], [92, 91, 90]),
        ([26], [90, 89]),
        ([27], [89, 88, 87]),
        ([28], [87, 86]),
        ([29], [86, 85, 84]),
        ([30], [84, 83, 82]),
        ([31], [82, 81, 80]),
        ([32], [80, 79]),
        ([33], [79, 78, 77]),
        ([34], [77, 76]),
        ([35], [75, 74]),
        ([36], [74, 73]),
        ([37], [72, 71]),
        ([38], [70, 69]),
        ([39], [69, 68]),
        ([40], [68, 67, 66]),
        ([41], [65, 64]),
        ([42, 43], [64, 63, 62]),
        ([44], [62, 61, 60]),
        ([45], [60, 59, 58]),
        ([46], [58, 57, 56]),
        ([47], [56, 55, 54]),
        ([48], [54, 53]),
        ([49], [52, 51]),
        ([111], [162]),
        ([112], [162, 161, 160]),
        ([113], [160, 159, 158]),
        ([114], [158, 157]),
        ([115], [157, 156, 155]),
        ([116], [155, 154, 153]),
        ([117], [153, 152]),
        ([118], [152, 151, 150]),
        ([119], [150, 149, 148]),
        ([120], [149, 148, 147]),
        ([121], [147, 146, 145]),
        ([122], [145, 144]),
        ([123], [144, 143, 142]),
        ([124], [142, 141, 140]),
        ([125], [140, 139, 138]),
        ([126], [138, 137]),
        ([127], [137, 136, 135]),
        ([128], [135, 134, 133, 132]),
        ([129], [132, 131]),
        ([163], [266]),
        ([164], [265]),
        ([165], [264]),
        ([166], [264, 263, 262]),
        ([167], [262, 261]),
        ([168], [261, 260, 259]),
        ([169], [259, 258]),
        ([170], [258, 257, 256]),
        ([171], [256, 255, 254]),
        ([172], [254, 253]),
        ([173], [253, 252]),
        ([174], [251, 250]),
        ([175], [250, 249, 248]),
        ([176], [248, 247, 246]),
        ([177], [245, 244, 243]),
        ([178], [242, 241]),
        ([179], [241, 240]),
        ([180], [239, 238]),
        ([181], [238, 237]),
        ([182], [237, 236, 235]),
        ([183], [235, 234, 233]),
        ([184], [233, 232, 231]),
        ([185], [231, 230]),
        ([186], [230, 229, 228]),
        ([187], [228, 227, 224]),
        ([188], [224, 223]),
        ([189], [223, 222, 221]),
        ([190], [221, 220]),
        ([191], [220, 219, 218]),
        ([192], [218, 217, 216]),
        ([193], [216, 215, 214]),
        ([194], [214, 213]),
        ([195], [213, 212, 211]),
        ([196], [210, 209]),
        ([197], [209, 208]),
        ([198], [208, 207]),
        ([199], [207, 206, 205, 204]),
        ([200], [204, 203]),
    ]
)

# cuốn 12: page_224 (224 TSG) - page_227 (225 TSG)

# endregion

# region 049 done
mapping["Prj_55g_Nam_APCS2_Sách Nôm công giáo 1995 - 049"] = {"page_pairs": []}

for i in range(22, 55):
    mapping["Prj_55g_Nam_APCS2_Sách Nôm công giáo 1995 - 049"]["page_pairs"].append(([i], [591 + 22 - i]))

for i in range(55, 300):
    mapping["Prj_55g_Nam_APCS2_Sách Nôm công giáo 1995 - 049"]["page_pairs"].append(([i], [55 + 556 - i]))

# endregion

# Save to JSON
with open("page_ranges.json", "w", encoding="utf-8") as json_file:
    json.dump(mapping, json_file, ensure_ascii=False, indent=4)