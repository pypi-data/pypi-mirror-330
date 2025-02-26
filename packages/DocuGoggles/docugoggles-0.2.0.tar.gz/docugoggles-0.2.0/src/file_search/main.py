from file_search.file_scanner.scanner import FileScanner
from file_search.text_extractor.text_extractor import TextExtractor
from file_search.search.searcher import ContentSearcher
import os
from typing import Dict, List
from tabulate import tabulate
from tqdm import tqdm

def format_file_count(count: int) -> str:
    """Format file count with thousands separator"""
    return f"{count:,}"

def categorize_extensions(files: Dict[str, List]) -> Dict[str, Dict[str, int]]:
    """Categorize file extensions into groups"""
    categories = {
        'Documents': ['.txt', '.pdf', '.docx'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
        'Code': ['.py', '.js', '.java', '.cpp', '.h', '.css', '.html', '.ts', '.jsx', '.php'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Media': ['.mp3', '.mp4', '.wav', '.avi', '.mov', '.ogg'],
        'Data': ['.json', '.xml', '.csv', '.sql', '.db'],
        'Executables': ['.exe', '.dll', '.msi'],
        'Other': []
    }
    
    result = {category: {} for category in categories}
    
    for ext, files_list in files.items():
        categorized = False
        for category, extensions in categories.items():
            if ext.lower() in extensions:
                result[category][ext] = len(files_list)
                categorized = True
                break
        if not categorized:
            result['Other'][ext] = len(files_list)
    
    return result

def extract_and_store_content(files: Dict[str, List], extractor: TextExtractor):
    """Extract content from supported files"""
    extracted_contents = {}
    total_files = sum(len(files_list) for files_list in files.values())
    
    with tqdm(total=total_files, desc="Extracting content") as pbar:
        for ext, files_list in files.items():
            if extractor.is_supported_extension(ext):
                for file_info in files_list:
                    try:
                        result = extractor.read_file(file_info['path'])
                        extracted_contents[file_info['path']] = {
                            'content': result['content'],
                            'metadata': result['metadata']
                        }
                    except Exception as e:
                        print(f"\nError processing {file_info['name']}: {str(e)}")
                    pbar.update(1)
            else:
                pbar.update(len(files_list))
    
    return extracted_contents

def print_category_results(category_name: str, extensions: Dict[str, int]):
    """Print results for a specific category"""
    if not extensions:
        return
    
    data = [[ext, format_file_count(count)] for ext, count in 
            sorted(extensions.items(), key=lambda x: x[1], reverse=True)]
    
    print(f"\n{category_name}")
    print("=" * len(category_name))
    print(tabulate(data, headers=['Extension', 'Count'], tablefmt='simple'))
    print(f"Total {category_name.lower()}: {format_file_count(sum(extensions.values()))}")

def display_search_results(results: List[Dict]):
    """Display search results with context"""
    if not results:
        print("\nNo matches found.")
        return
    
    print(f"\nFound matches in {len(results)} files:")
    print("=" * 60)
    
    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. File: {os.path.basename(result['file_path'])}")
        print(f"   Path: {result['file_path']}")
        print(f"   Matches: {result['match_count']}")
        print("\n   Context snippets:")
        
        for i, snippet in enumerate(result['snippets'][:3], 1):
            print(f"   {i}. {snippet}")
        
        if len(result['snippets']) > 3:
            print(f"   ... and {len(result['snippets']) - 3} more matches")
        print("-" * 60)

def main():
    default_dir = "/home"  
    print(f"\nCurrent directory: {default_dir}")
    custom_dir = input("Press Enter to use current directory or enter a new path: ").strip()
    directory_to_scan = custom_dir if custom_dir else default_dir
    
    # Initialize scanner and extractor
    scanner = FileScanner(directory_to_scan)
    extractor = TextExtractor()
    
    print(f"\nScanning directory: {directory_to_scan}")
    print("=" * 50)
    
    try:
        print("\nScanning files...")
        # Ask user about PDF processing
        process_pdfs = input("Process PDF files? (This may take longer) [y/N]: ").lower().strip()
        
        supported_extensions = list(extractor.supported_extensions.keys())
        if process_pdfs != 'y':
            supported_extensions.remove('.pdf')
            print("Skipping PDF files.")
        
        files = scanner.scan_directory(supported_extensions)
        
        if not files:
            print("\nNo supported files found in the directory.")
            return
        
        stats = scanner.get_directory_statistics()
        
        extracted_contents = extract_and_store_content(files, extractor)
        searcher = ContentSearcher(extracted_contents)
        
        while True:
            print("\nOptions:")
            print("1. Search in files")
            print("2. View file statistics")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                query = input("\nEnter search term: ").strip()
                if query:
                    case_sensitive = input("Case sensitive search? (y/N): ").lower().strip() == 'y'
                    results = searcher.search(query, case_sensitive=case_sensitive)
                    display_search_results(results)
                else:
                    print("Search term cannot be empty.")
                    
            elif choice == '2':
                categorized_files = categorize_extensions(files)
                for category in categorized_files:
                    print_category_results(category, categorized_files[category])
                
                print("\nSummary")
                print("=======")
                print(f"Total files: {format_file_count(stats['total_files'])}")
                print(f"Total directories: {format_file_count(stats['total_directories'])}")
                print(f"Total size: {format_file_count(stats['total_size'])} bytes")
                print(f"Unique file types: {len(stats['extension_counts'])}")
                print(f"Extracted content from: {len(extracted_contents)} files")
                
            elif choice == '3':
                print("\nGoodbye!")
                break
                
            else:
                print("\nInvalid choice. Please try again.")
                
    except FileNotFoundError:
        print(f"\nError: Directory '{directory_to_scan}' not found.")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()