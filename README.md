# Quran Text to Image Visualization

This project processes Quranic text and converts it into a grayscale image by transforming each character to its ASCII value, creating a matrix from these values, and normalizing them for visual representation. The program reads a Quran text file where each line is in the format `SurahNumber|VerseNumber|VerseText`, filters the verse text, and visualizes it in an image.

## Features
- Reads and processes Arabic Quran text.
- Reshapes and displays Arabic text properly for correct rendering.
- Converts text to ASCII values and builds a matrix.
- Saves the matrix as a grayscale image, representing the Quranic text visually.

## Requirements

To run this project, you need the following packages installed:

```bash
pip install numpy pillow arabic-reshaper python-bidi

## Project Structure

- **process_quran_text**: Reads and reshapes the text for correct Arabic display.
- **text_to_ascii_codes**: Converts Arabic text to ASCII values, normalizing each to the 0-255 range.
- **create_matrix**: Constructs a matrix from ASCII values and pads it to fit evenly.
- **matrix_to_image**: Normalizes the matrix and converts it into a grayscale image.
- **process_quran_visualization**: The main function to run all processing steps and save the final image.

## Usage

1. **Prepare the Quran text file**: Ensure your input file is formatted as `SurahNumber|VerseNumber|VerseText`, with each verse on a new line. For example:
   ```
   1|1|بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
   1|2|ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ
   ...
   ```

2. **Run the Script**: Use the following command to generate the visualization:

   ```bash
   python main.py
   ```

   Replace `main.py` with the name of the file containing the script if different.

3. **Output**: The processed image will be saved as `quran_visualization.png` (or a custom name you set in the script). You should see a message confirming the image's location and the shape of the generated matrix.

## Example Code

```python
if __name__ == "__main__":
    input_file = "quran.txt"  # Path to the Quran text file
    output_file = "quran_visualization.png"  # Output path for the image
    
    matrix, image = process_quran_visualization(input_file, output_file)
    if matrix is not None:
        print(f"Matrix shape: {matrix.shape}")
        print(f"Image saved to: {output_file}")
```

## Example Output

An example output will look like a grayscale image representing ASCII values derived from the Quranic text. The image is a unique visual interpretation of the Quran, based on its characters' ASCII codes.

## Error Handling

- **File Not Found**: If the input file is not found, an error message will be printed.
- **Unexpected File Format**: If a line in the file is not in the expected format, it will be skipped, and processing will continue.
- **Other Errors**: Any other exceptions encountered during processing are caught and displayed.

## Notes
- Ensure that the input file encoding is UTF-8 to handle Arabic characters correctly.
- Modify the `matrix_height` parameter in `create_matrix` if you want to change the matrix dimensions.

## Author
Ebrahim akbari
