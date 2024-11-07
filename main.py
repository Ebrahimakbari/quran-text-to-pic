import numpy as np
from PIL import Image
import arabic_reshaper
from bidi.algorithm import get_display
import codecs

def process_quran_text(file_path):
    """
    خواندن فایل قرآن و استخراج تنها متن آیات
    """
    verses = []
    with codecs.open(file_path, 'r', 'utf-8') as file:
        for line in file:
            # جدا کردن متن آیه از سوره و شماره آیه
            parts = line.strip().split('|')
            if len(parts) == 3:
                verses.append(parts[2])  # فقط متن آیه اضافه شود

    # ادغام متن آیه‌ها به صورت یک رشته واحد
    text = ' '.join(verses)

    # بازسازی متن عربی برای نمایش صحیح
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)

    return bidi_text

def text_to_ascii_codes(text):
    return np.fromiter((ord(char) % 256 for char in text), dtype=np.uint8)

def create_matrix(ascii_codes, matrix_height=None):
    if matrix_height is None:
        matrix_height = int(np.sqrt(len(ascii_codes)))
    
    matrix_width = (len(ascii_codes) + matrix_height - 1) // matrix_height
    ascii_codes = np.pad(ascii_codes, (0, matrix_height * matrix_width - len(ascii_codes)), mode='constant')
    
    matrix = ascii_codes.reshape(matrix_height, matrix_width)
    return matrix

def matrix_to_image(matrix, output_path):
    normalized_matrix = ((matrix - matrix.min()) * (255 / (matrix.max() - matrix.min()))).astype(np.uint8)
    img = Image.fromarray(normalized_matrix)
    img.save(output_path)
    return img

def process_quran_visualization(input_file_path, output_image_path):
    try:
        text = process_quran_text(input_file_path)
        ascii_codes = text_to_ascii_codes(text)
        matrix = create_matrix(ascii_codes)
        image = matrix_to_image(matrix, output_image_path)

        return matrix, image
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    input_file = "quran.txt"
    output_file = "quran_visualization.png"

    matrix, image = process_quran_visualization(input_file, output_file)
    if matrix is not None:
        print(f"Matrix shape: {matrix.shape}")
        print(f"Image saved to: {output_file}")
