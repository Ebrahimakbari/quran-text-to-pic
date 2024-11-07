import numpy as np
from PIL import Image
import arabic_reshaper
from bidi.algorithm import get_display
import codecs

def process_quran_text(file_path):
    """
    Reads a Quran text file and extracts only the verses (ignoring surah and verse numbers).
    Returns the reshaped and bidi-corrected text for proper Arabic display.
    """
    verses = []  # List to store each verse's text
    with codecs.open(file_path, 'r', 'utf-8') as file:
        for line in file:
            # Split each line by '|' to separate surah number, verse number, and verse text
            parts = line.strip().split('|')
            if len(parts) == 3:
                verses.append(parts[2])  # Add only the verse text (third part) to the list
    
    # Join all verses into a single string separated by spaces
    text = ' '.join(verses)
    
    # Reshape and reorder the text for correct Arabic display
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    
    return bidi_text

def text_to_ascii_codes(text):
    """
    Converts the Arabic text to ASCII codes and normalizes them to a range of 0-255.
    """
    # Generate ASCII codes with modulo 256 normalization
    return np.fromiter((ord(char) % 256 for char in text), dtype=np.uint8)

def create_matrix(ascii_codes, matrix_height=None):
    """
    Creates a matrix from ASCII codes. Determines the optimal height if not provided.
    """
    # If no matrix height is specified, estimate it based on the square root of total ASCII codes
    if matrix_height is None:
        matrix_height = int(np.sqrt(len(ascii_codes)))
    
    # Calculate matrix width, adjusting for any remainder
    matrix_width = (len(ascii_codes) + matrix_height - 1) // matrix_height
    
    # Pad the ASCII code list with zeros if needed to fill the matrix completely
    ascii_codes = np.pad(ascii_codes, (0, matrix_height * matrix_width - len(ascii_codes)), mode='constant')
    
    # Reshape the padded ASCII codes into a matrix of the desired shape
    matrix = ascii_codes.reshape(matrix_height, matrix_width)
    return matrix

def matrix_to_image(matrix, output_path):
    """
    Normalizes the matrix values to 0-255 and saves it as a grayscale image.
    """
    # Normalize the matrix to fit within the 0-255 grayscale range for image creation
    normalized_matrix = ((matrix - matrix.min()) * (255 / (matrix.max() - matrix.min()))).astype(np.uint8)
    
    # Convert the normalized matrix to a PIL image and save it to the specified path
    img = Image.fromarray(normalized_matrix)
    img.save(output_path)
    return img

def process_quran_visualization(input_file_path, output_image_path):
    """
    Main function to process Quran text, convert it to ASCII codes, create a matrix, and save it as an image.
    """
    try:
        # Step 1: Read and process the Quran text to extract and reshape the verses
        text = process_quran_text(input_file_path)
        
        # Step 2: Convert the text to ASCII codes
        ascii_codes = text_to_ascii_codes(text)
        
        # Step 3: Create a matrix from the ASCII codes
        matrix = create_matrix(ascii_codes)
        
        # Step 4: Convert the matrix to an image and save it
        image = matrix_to_image(matrix, output_image_path)
        
        return matrix, image
    except Exception as e:
        # Handle errors, such as file not found or unexpected data formats
        print(f"An error occurred: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    input_file = "quran.txt"  # Path to the Quran text file
    output_file = "quran_visualization.png"  # Path where the image will be saved
    
    # Process the Quran file and generate the visualized image
    matrix, image = process_quran_visualization(input_file, output_file)
    if matrix is not None:
        print(f"Matrix shape: {matrix.shape}")  # Display the shape of the generated matrix
        print(f"Image saved to: {output_file}")  # Confirm where the image is saved
