import pytest
from pathlib import Path
import tempfile
import os
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_search.file_scanner.scanner import FileScanner
from file_search.text_extractor.text_extractor import TextExtractor
from file_search.search.searcher import ContentSearcher

class TestFileSearch:
    @pytest.fixture
    def temp_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # create files
            files = {
                "test.txt": "This is a test file.",
                "empty.txt": "",
                "test.docx": "DOCX test content"
            }
            
            for filename, content in files.items():
                file_path = Path(temp_dir) / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            yield temp_dir

    def test_file_scanner_basic(self, temp_directory):
        scanner = FileScanner(temp_directory)
        files = scanner.scan_directory(['.txt'])
        
        assert files is not None
        assert '.txt' in files
        assert len(files['.txt']) > 0
        assert any('test.txt' in f['path'] for f in files['.txt'])

    def test_file_scanner_multiple_extensions(self, temp_directory):
        scanner = FileScanner(temp_directory)
        files = scanner.scan_directory(['.txt', '.docx'])
        
        assert '.txt' in files
        assert '.docx' in files

    def test_file_scanner_statistics(self, temp_directory):
        scanner = FileScanner(temp_directory)
        stats = scanner.get_directory_statistics()
        
        assert 'total_files' in stats
        assert 'total_directories' in stats
        assert 'total_size' in stats
        assert 'extension_counts' in stats

    def test_file_scanner_empty_directory(self):
        with tempfile.TemporaryDirectory() as empty_dir:
            scanner = FileScanner(empty_dir)
            files = scanner.scan_directory(['.txt'])
            stats = scanner.get_directory_statistics()
            
            assert not files
            assert stats['total_files'] == 0

    def test_text_extractor_metadata(self, temp_directory):
        extractor = TextExtractor()
        txt_file = str(Path(temp_directory) / "test.txt")
        result = extractor.read_file(txt_file)
        
        metadata = result['metadata']
        assert metadata['name'] == "test.txt"
        assert metadata['extension'] == '.txt'
        assert metadata['size'] > 0
        assert isinstance(metadata['created'], datetime)
        assert isinstance(metadata['modified'], datetime)
        assert metadata['parent_dir']

    def test_searcher_basic(self, temp_directory):
        extractor = TextExtractor()
        txt_file = str(Path(temp_directory) / "test.txt")
        content = extractor.read_file(txt_file)
        
        extracted_contents = {txt_file: content}
        searcher = ContentSearcher(extracted_contents)
        
        results = searcher.search('test')
        assert len(results) > 0
        assert results[0]['file_path'] == txt_file
        assert len(results[0]['snippets']) > 0

    def test_searcher_case_sensitivity(self, temp_directory):
        extractor = TextExtractor()
        txt_file = str(Path(temp_directory) / "test.txt")
        content = extractor.read_file(txt_file)
        
        extracted_contents = {txt_file: content}
        searcher = ContentSearcher(extracted_contents)
        
        results_sensitive = searcher.search('TEST', case_sensitive=True)
        results_insensitive = searcher.search('TEST', case_sensitive=False)
        
        assert len(results_sensitive) == 0
        assert len(results_insensitive) > 0

    def test_searcher_multiple_files(self, temp_directory):
        extractor = TextExtractor()
        extracted_contents = {}
        
        # Create multiple text files with different content
        test_files = {
            "test1.txt": "This is test file one",
            "test2.txt": "This is test file two"
        }
        
        # Create and extract content from files
        for filename, content in test_files.items():
            file_path = Path(temp_directory) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            extracted_content = extractor.read_file(str(file_path))
            extracted_contents[str(file_path)] = extracted_content
        
        searcher = ContentSearcher(extracted_contents)
        results = searcher.search('test')
        
        assert len(results) == 2  # Should find matches in both files
        assert all(len(r['snippets']) > 0 for r in results)

    def test_filter_results(self, temp_directory):
        extractor = TextExtractor()
        extracted_contents = {}
        
        # Create test files with different content
        test_files = {
            "test1.txt": "This contains test multiple times: test test",
            "test2.txt": "This contains test once"
        }
        
        # Create and extract content from files
        for filename, content in test_files.items():
            file_path = Path(temp_directory) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            extracted_content = extractor.read_file(str(file_path))
            extracted_contents[str(file_path)] = extracted_content
        
        searcher = ContentSearcher(extracted_contents)
        results = searcher.search('test')
        
        # Test extension filtering
        txt_results = searcher.filter_results(results, extensions=['.txt'])
        assert len(txt_results) == 2
        assert all(Path(r['file_path']).suffix == '.txt' for r in txt_results)
        
        # Test min matches filtering
        min_match_results = searcher.filter_results(results, min_matches=2)
        assert len(min_match_results) == 1  # Only one file has multiple matches
        assert all(r['match_count'] >= 2 for r in min_match_results)

    def test_error_handling(self, temp_directory):
        # Test nonexistent file
        extractor = TextExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.read_file('nonexistent.txt')
        
        # Test nonexistent directory
        nonexistent_dir = os.path.join(temp_directory, 'nonexistent')
        scanner = FileScanner(nonexistent_dir)
        with pytest.raises(FileNotFoundError):
            scanner.scan_directory(['.txt'])
    def test_text_extractor_error_cases(self, temp_directory):
        extractor = TextExtractor()
        
        # Test unsupported file type
        unsupported_file = Path(temp_directory) / "test.xyz"
        with open(unsupported_file, 'w') as f:
            f.write("test")
        with pytest.raises(ValueError, match="Unsupported file type"):
            extractor.read_file(str(unsupported_file))
        
        # Test non-existent file
        with pytest.raises(FileNotFoundError):
            extractor.read_file("nonexistent.txt")
        
        # Test directory instead of file
        dir_path = Path(temp_directory) / "testdir"
        dir_path.mkdir()
        with pytest.raises(ValueError, match="Path is not a file"):
            extractor.read_file(str(dir_path))

    def test_searcher_advanced_features(self, temp_directory):
        extractor = TextExtractor()
        extracted_contents = {}
        
        # Create test files with specific content
        test_files = {
            "test1.txt": "Line with UPPERCASE and lowercase test",
            "test2.txt": "Multiple\nline\ntest\ncontent"
        }
        
        for filename, content in test_files.items():
            file_path = Path(temp_directory) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            extracted_content = extractor.read_file(str(file_path))
            extracted_contents[str(file_path)] = extracted_content
        
        searcher = ContentSearcher(extracted_contents)
        
        # Test case-sensitive
        case_sensitive_results = searcher.search('UPPERCASE', case_sensitive=True)
        assert len(case_sensitive_results) == 1
        
        # Test complex filtering
        results = searcher.search('test')
        filtered_results = searcher.filter_results(
            results,
            extensions=['.txt'],
            min_matches=1
        )
        assert len(filtered_results) > 0

    def test_main_functionality(self, temp_directory, monkeypatch):
        """Test main functionality using mocked inputs"""
        from file_search.main import main
        
        # Create test files
        test_files = {
            "test1.txt": "Test content one",
            "test2.txt": "Test content two"
        }
        
        for filename, content in test_files.items():
            file_path = Path(temp_directory) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Mock input/output
        inputs = iter([
            temp_directory,  # directory to scan
            'n',            # skip PDF processing
            '1',            # search option
            'test',         # search term
            'n',            # case sensitive
            '2',            # view statistics
            '3'             # exit
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        # Capture stdout
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # output
        output = captured_output.getvalue()
        assert "test1.txt" in output
        assert "test2.txt" in output
        assert "Total files:" in output