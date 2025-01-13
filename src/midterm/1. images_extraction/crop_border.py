import json
from PIL import Image
import os

def crop(img_path, output_dir, scale_left, scale_top, scale_right, scale_bottom):
    """
    Cắt một hình ảnh theo tỷ lệ đã chỉ định và lưu hình ảnh đã cắt vào thư mục đầu ra.
    
    Args:
        img_path (str): Đường dẫn đến hình ảnh cần cắt.
        output_dir (str): Thư mục đầu ra để lưu hình ảnh đã cắt.
        scale_left (float): Tỷ lệ cắt từ cạnh trái.
        scale_top (float): Tỷ lệ cắt từ cạnh trên.
        scale_right (float): Tỷ lệ cắt từ cạnh phải.
        scale_bottom (float): Tỷ lệ cắt từ cạnh dưới.
    """
    img = Image.open(img_path)
    width, height = img.size
    left = width * scale_left
    top = height * scale_top
    right = width * (1 - scale_right)
    bottom = height * (1 - scale_bottom)
    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(os.path.join(output_dir, os.path.basename(img_path)))

def process_images(target_dir, output_dir, start_page, end_page, scale_left_even, scale_top_even, scale_right_even, scale_bottom_even, scale_left_odd, scale_top_odd, scale_right_odd, scale_bottom_odd):
    """
    Xử lý và cắt các hình ảnh trong phạm vi trang chỉ định.
    
    Args:
        target_dir (str): Thư mục chứa các hình ảnh gốc.
        output_dir (str): Thư mục lưu hình ảnh đã cắt.
        start_page (int): Số trang bắt đầu cần xử lý.
        end_page (int): Số trang kết thúc cần xử lý.
        scale_left (float): Tỷ lệ cắt từ cạnh trái.
        scale_top (float): Tỷ lệ cắt từ cạnh trên.
        scale_right (float): Tỷ lệ cắt từ cạnh phải.
        scale_bottom (float): Tỷ lệ cắt từ cạnh dưới.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(start_page, end_page + 1):
        img_name = f"page_{page_num}.png"
        img_path = os.path.join(target_dir, img_name)

        if os.path.exists(img_path):
            if page_num % 2 == 0:
                crop(img_path, output_dir, scale_left_even, scale_top_even, scale_right_even, scale_bottom_even)
            else:
                crop(img_path, output_dir, scale_left_odd, scale_top_odd, scale_right_odd, scale_bottom_odd)
            print(f"Processed {img_name}")
        else:
            print(f"Warning: {img_name} not found in {target_dir}")

# Thư mục chứa hình ảnh gốc và đầu ra
target_dir = r"extracted/Sach-Nom-Cong-Giao-1995-012"
output_dir = r"extracted/Sach-Nom-Cong-Giao-1995-012-cropped"

# Phạm vi trang cần xử lý
start_page = 1
end_page = 1000

# Tỷ lệ cắt (trái, trên, phải, dưới) cho mỗi trang chẵn và lẻ
# Thường trang lẻ hay bị dư bên trái, trang chẵn bị dư bên phải

scale_left_even = 0.12
scale_top_even = 0
scale_right_even = 0
scale_bottom_even = 0

scale_left_odd = 0
scale_top_odd = 0
scale_right_odd = 0.12
scale_bottom_odd = 0


# Gọi hàm xử lý
process_images(target_dir, output_dir, start_page, end_page, scale_left_even, scale_top_even, scale_right_even, scale_bottom_even, scale_left_odd, scale_top_odd, scale_right_odd, scale_bottom_odd)

# 001: 0.14 left 0.12 right
# 002: 0.04 left 0.04 right
# 004: 0.09 left 0.08 right
# 005: 0.08 left 0.08 right
# 049: 0.12 left 0.12 right

# only this one is left_even and right_odd
# 012: 0.12 left 0.12 right
