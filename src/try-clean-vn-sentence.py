import re


def clean_sentences(ocr_text):
    """
    Cleans sentences from a list by removing those that start with patterns like '1)', '(1)', '(2)', etc.
    
    :param ocr_text: List of sentences (strings).
    :return: Cleaned list of sentences.
    """
    # Pattern to match lines starting with "1)", "(1)", "(2)", "(3b)", etc.
    pattern = r"^\(?-?\d+[a-zA-Z]?\)"
    cleaned_text = [sentence for sentence in ocr_text if not re.match(pattern, sentence.strip())]
    return cleaned_text


ocr_text_2 = [
        "Kính mừng Chúa Cả thiên đàng (I),",
        "Chúc cho người thế vững vàng bình yên.",
        "Lại còn những kẻ chăn chiên,",
        "Cũng kéo nhau đến cả miền reo hộ.",
        "Vô linh như giống chiên bò,",
        "Thế mà cũng đến phì phò thở hơi.",
        "Ba vua xem thấy rụng rời,",
        "Như mừng như sự lả lơi tâm tình.",
        "Lại thấy Đức Mẹ đồng trinh,",
        "Nhìn con chốc chốc như hình thảm thương.",
        "Giu Se (2) ngồi đứng lựa nương,",
        "Ra như sấp ngửa khôn lường không lo.",
        "Ba vua thẩm thữ nhỏ to,",
        "Sấp mình năn nỉ thẹn thò phần riêng.",
        "(1) Tiếng địa phương ( hạ lưu sông Hồng ) thường đọc là dùng ( thiên",
        "dàng ), thay vì đường ( thiên đường )",
        "(2) Giu Se là dưỡng phụ của Chúa Giê Su , dọc theo âm tiếng Bồ Jose",
        "(2b)"
    ]


ocr_text_3 = [
        "Trong lòng chẳng chút phàn nàn,",
        "Một cậy trông Chúa bình an tới nhà. Amen. (1)",
        "2. Bà thánh Anna (2) cựu vãn.",
        "L",
        "Ơn trên mưa dưới gió bay,",
        "Y Chê (3) đâu cũng một ngày mừng vui.",
        "Pháp mẫu Chúa định bởi trời.",
        "Đức Bà Thánh cả một người giáng sinh.",
        "Kể từ ông Giu A Kinh, (4)",
        "Dòng vua Da Vít thánh minh ai bì",
        "An Na phụng hứa xướng tùy,",
        "Ông bà ao ước đêm khuya một niềm.",
        "Mùa thu trong nhắp (5) ban đêm,",
        "Thiên thần hiện bảo ứng điềm sinh ra.",
        "(1) \"Xin được như vậy\" ( tiếng Do Thái)",
        "(2) Phiên âm tiếng Bồ Ana",
        "(3) Y-Ghê bởi tiếng Bồ Igreja' Hội Thánh\" hay \"Giáo Hội\", thường ghi",
        "là Y-ghê-ri-gia",
        "(-1) Phiên âm tiếng Bồ Joaquin, hiện nay đọc là Gioakim",
        "(5) Chợp mắt ngủ",
        "(3b)"
    ]

cleaned_text_2 = clean_sentences(ocr_text_2)

print("\nCleaned OCR Text 2:")
print(cleaned_text_2)
