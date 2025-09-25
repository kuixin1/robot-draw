from strokes.extract_strokes import extract_strokes
from strokes.extract_strokes import convert_strokes_to_coords

if __name__ == "__main__":
    extract_strokes('input', 'output', threshold=20)
    convert_strokes_to_coords('output', 'output_strokes', canvas_size_cm=40)