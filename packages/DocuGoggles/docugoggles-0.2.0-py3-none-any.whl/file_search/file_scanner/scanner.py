import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class FileScanner:
    """
    A class to handle recursive directory scanning and file metadata collection.
    """
    def __init__(self, base_directory: str):
        """
        Initialize the FileScanner with a base directory.
        Args:
            base_directory: The root directory path to start scanning from
        """
        self.base_directory = Path(base_directory)
    
    def scan_directory(self, file_types: Optional[List[str]] = [".txt"]) -> Dict[str, List[Dict[str, any]]]:
        """
        Recursive scan of the base directory for files.
        """
        if not self.base_directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.base_directory}")
        
        found_files: Dict[str, List[Dict[str, any]]] = {}
        
        for root, _, files in os.walk(self.base_directory):
            for file in files:
                file_path = Path(root) / file
                extension = file_path.suffix.lower()
                
                if file_types and extension not in file_types:
                    continue
                
                metadata = self._get_file_metadata(file_path)
                
                if extension not in found_files:
                    found_files[extension] = []
                
                found_files[extension].append(metadata)
        
        return found_files
    
    def _get_file_metadata(self, file_path: Path) -> Dict[str, any]:
        """
        Collect metadata for a single file.
        
        Args:
            file_path: Path object pointing to the file
            
        Returns:
            Dictionary containing file metadata
        """
        stats = file_path.stat()
        
        return {
            'name': file_path.name,
            'path': str(file_path.absolute()),
            'size': stats.st_size,  # Size in bytes
            'created': datetime.fromtimestamp(stats.st_ctime),
            'modified': datetime.fromtimestamp(stats.st_mtime),
            'extension': file_path.suffix.lower(),
            'is_hidden': file_path.name.startswith('.'),
            'parent_dir': str(file_path.parent)
        }
    
    def get_directory_size(self) -> int:
        """
        Calculate the total size of all files in the scanned directory.
        """
        total_size = 0
        for root, _, files in os.walk(self.base_directory):
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
        return total_size
    
    def get_directory_statistics(self) -> Dict[str, any]:
        """
        Get statistics about the scanned directory.
        """
        file_count = 0
        dir_count = 0
        extension_counts: Dict[str, int] = {}
        
        for root, dirs, files in os.walk(self.base_directory):
            dir_count += len(dirs)
            file_count += len(files)
            
            for file in files:
                extension = Path(file).suffix.lower()
                extension_counts[extension] = extension_counts.get(extension, 0) + 1
        
        return {
            'total_files': file_count,
            'total_directories': dir_count,
            'total_size': self.get_directory_size(),
            'extension_counts': extension_counts
        }