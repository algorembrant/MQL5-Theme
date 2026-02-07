from markitdown import MarkItDown
import os

def convert_pdf():
    # Define paths
    pdf_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\Python\mql5.pdf"
    output_path = r"C:\Users\User\Desktop\VSCode\MQL5-Theme\Python\mql5.md"
    
    print(f"Initializing MarkItDown...")
    md = MarkItDown()
    
    print(f"Converting {pdf_path}...")
    try:
        # Convert the file
        result = md.convert(pdf_path)
        
        # Write content to markdown file
        print(f"Writing output to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
            
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    convert_pdf()
