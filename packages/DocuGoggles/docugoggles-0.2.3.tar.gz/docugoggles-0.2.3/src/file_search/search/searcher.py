from typing import Dict, List, Optional
from pathlib import Path
import re

class ContentSearcher:
    """
    A class to handle searching through extracted document content.
    """
    def __init__(self, extracted_contents: Dict[str, Dict]):
        """
        Initialize the searcher with extracted contents.
        
        Args:
            extracted_contents: Dictionary mapping file paths to their content and metadata
        """
        self.contents = extracted_contents

    def search(self, query: str, case_sensitive: bool = False) -> List[Dict]:

        results = []
        search_query = query if case_sensitive else query.lower()
        
        for file_path, data in self.contents.items():
            content = data['content']
            if not case_sensitive:
                content = content.lower()
            
            if search_query in content:
                # Get context around matches
                context_snippets = self._get_context_snippets(
                    data['content'], 
                    query, 
                    case_sensitive
                )
                
                results.append({
                    'file_path': file_path,
                    'metadata': data['metadata'],
                    'snippets': context_snippets,
                    'match_count': len(context_snippets)
                })
        
        # Sort by number of matches
        results.sort(key=lambda x: x['match_count'], reverse=True)
        return results

    def _get_context_snippets(self, content: str, query: str, case_sensitive: bool, 
                            context_chars: int = 50) -> List[str]:

        search_content = content if case_sensitive else content.lower()
        search_query = query if case_sensitive else query.lower()
        
        snippets = []
        start = 0
        
        while True:
            index = search_content.find(search_query, start)
            if index == -1:
                break
                
            snippet_start = max(0, index - context_chars)
            snippet_end = min(len(content), index + len(query) + context_chars)
            
            snippet = content[snippet_start:snippet_end]
            
            if snippet_start > 0:
                snippet = f"...{snippet}"
            if snippet_end < len(content):
                snippet = f"{snippet}..."
                
            snippets.append(snippet)
            start = index + 1
            
        return snippets

    def filter_results(self, results: List[Dict], 
                      min_matches: Optional[int] = None,
                      extensions: Optional[List[str]] = None) -> List[Dict]:

        filtered = results.copy()
        
        if min_matches is not None:
            filtered = [r for r in filtered if r['match_count'] >= min_matches]
            
        if extensions:
            extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                        for ext in extensions]
            filtered = [r for r in filtered 
                       if Path(r['file_path']).suffix.lower() in extensions]
            
        return filtered