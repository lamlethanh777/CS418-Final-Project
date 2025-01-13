from nom_ocr import load_ocr_results_from_json_dir
import os


def main():
    EXTRACTED_OCR_DIR = r"../../OCR_NOM/Sach-Nom-Cong-Giao-1995-004_Processed"
    EXTRACTED_IMAGES_DIR = r"../extracted_imgs"
    nom_ocr_results = load_ocr_results_from_json_dir(EXTRACTED_OCR_DIR)

    # print ocr results in xlsx file contains 5 cols: Image_name, ID, Image Box, SinoNom OCR, Chữ Quốc Ngữ
    import pandas as pd
    
    df = pd.DataFrame(
        columns=["Image_name", "ID", "Image Box", "SinoNom OCR", "Chữ Quốc Ngữ"]
    )
    count = 0
    for page, result in nom_ocr_results.items():
        count += 1
        for box in result:
            df = df._append(
                {
                    "Image_name": "page_" + str(page) + ".png",
                    "ID": "",
                    "Image Box": str(box["points"]),
                    "SinoNom OCR": box["transcription"],
                    "Chữ Quốc Ngữ": "",
                },
                ignore_index=True,
            )

    output_dir = "."
    output_path = os.path.join(output_dir, "result.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Result has been saved to {output_dir}")

main()
