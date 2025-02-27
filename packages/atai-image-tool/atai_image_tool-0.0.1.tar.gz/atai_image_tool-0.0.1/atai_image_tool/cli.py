import argparse
import sys
from .core import extract_image_content, save_as_json

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Extract text from images using OCR and save to JSON or print to console'
    )
    parser.add_argument(
        'image_path', 
        help='Path to the image file'
    )
    parser.add_argument(
        'output_file', 
        nargs='?',
        default=None,
        help='Path to the output JSON file (optional, if omitted will print to console)'
    )
    parser.add_argument(
        '--languages', 
        nargs='+', 
        default=['en'],
        help='Languages to use for OCR (default: en)'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    try:
        extracted_text = extract_image_content(args.image_path, args.languages)
        if extracted_text:
            if args.output_file:
                save_as_json(extracted_text, args.output_file)
                print(f"Text extracted from image saved to {args.output_file} in JSON format.")
            else:
                print("Extracted text:")
                print(extracted_text)
            return 0
        else:
            print("No text was extracted from the image.")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())