import re


def merge_sentences(text_lines):
    merged_lines = []
    i = 0
    while i < len(text_lines):
        # Check if the line does not end with punctuation and the next line starts with a lowercase letter
        if i < len(text_lines) - 1 and not re.search(r'[.,;!?]$', text_lines[i]) and text_lines[i+1][0].islower():
            # Merge current and next line
            merged_lines.append(
                text_lines[i].strip() + " " + text_lines[i+1].strip())
            i += 2  # Skip the next line since it's merged
        else:
            # If no merging condition met, just append the current line
            merged_lines.append(text_lines[i].strip())
            i += 1
    return merged_lines


# Example input
ocr_text = [
    "Ơn trên mưa xuống thiêng liêng,",
    "Ba vua đã biết chẳng kiêng chẳng nề.",
    "Đoạn rồi tạ Chúa ra về,",
    "Giã ơn Đức Mẹ, Giu Se cầu bầu.",
    "Lòng son rỡ rỡ một màu,",
    "Đường trăng lối gió trước sau khôn lường.",
    "Quyết lòng tìm Chúa là hơn,",
    "Chức quyền sang trọng thế gian nào bằng.",
    "Rộn ràng vừa quảy trẩy đi,",
    "Thiên thần hiện bảo phải về đường quanh.",
    "Chớ nghe lòng dữ dỗ dành,",
    "Tìm giết",
    "con trẻ cho mình khỏi lo.",
    "Ba vua hiểu biết căn do,",
    "Phải đi lối khác kẻo rồi gian nan."
]


ocr_text1 = [
    "Lễ Ba Vua",
    "cựu vãn.",
    "Đội ơn Chúa rất nhân từ,",
    "Liều mình xuống thế kẻo hư loài người.",
    "Hiền lành nhân đức tốt tươi.",
    "Nắng mưa che chở mọi người thế gian.",
    "Mưa ơn tưới xuống chứa chan,",
    "Gió nhân quét lại cho tan cơn nồng.",
    "Mừng ba vua nước phương Đông.",
    "Thấy sao ngẫm sách hợp đồng phân minh.",
    "Biết rằng Đại Đế giáng sinh.",
    "Cùng nhau hợp lại cất mình trẩy đi.",
    "Sắm lương thực đủ lễ nghi,",
    "Ngựa xe quân quốc đề huề kéo ra."
]
# Merge sentences based on the criteria
merged_text = merge_sentences(ocr_text1)

# Output the result
for line in merged_text:
    print(line)
