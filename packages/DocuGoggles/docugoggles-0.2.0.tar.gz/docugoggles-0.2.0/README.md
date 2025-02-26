# DocuGoggles 🥽
# A File Content Search and Management System with OCR 

## Project Description
My system will provide the ability of file content searching and management capabilities with OCR (Optical Character Recognition) for images. 

It allows the user to:
- Scan and index files across directories or a specific directory 
- Extract the content from both regular files (like pdf, txt, docx, etc..) and images using OCR
- Store the content, files name, location
- Enables content-based search without requiring filenames
- Provides fast and accurate search results by using Meilisearch as a search engine (after files are scanned)

## Technical Architecture
- Language: Python 3.10+
- OCR Engine: Tesseract (might change this later)
- Search Engine: Meilisearch for the content text search

## Key Features
- Support (text, images, PDFs, docx)
- OCR for images to extract its content
- Content indexing and search
- Metadata extraction and management
  
## Installation Instructions (To be added)

### Option 1: Docker Installation
[Installation steps will be added]

### Option 2: Manual Installation
1. Clone the repository:
```bash
git clone https://github.com/Duquesne-Spring-2025-COSC-481/Naif-ALqurashi.git
cd Naif-ALqurashi
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional for now, added to use later) Install Tesseract OCR (not used now since the current stage only txt file) 
   - Download the Windows installer from [GitHub Tesseract Release](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

5. Run the application:
```bash
cd src
python main.py
```


## Usage Instructions (To be added)

## Dependencies (To be added)

## Testing (To be added)
