import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF file in binary read mode
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get total number of pages
            num_pages = len(pdf_reader.pages)
            print(f"\nTotal pages: {num_pages}")
            
            # Extract text from all pages
            text = ""
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]
                # Extract text from page
                text += page.extract_text()
                print(f"Processed page {page_num + 1}")
            
            return text
            
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def main():
    # Folder containing PDFs
    pdf_folder = "budget_pdfs"
    
    # Create output folder for text files if it doesn't exist
    output_folder = "budget_texts"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each PDF in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            print(f"\nProcessing: {filename}")
            
            # Full path to PDF file
            pdf_path = os.path.join(pdf_folder, filename)
            
            # Extract text
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                # Create output text file
                output_file = os.path.join(output_folder, filename.replace('.pdf', '.txt'))
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Text saved to: {output_file}")

if __name__ == "__main__":
    main()