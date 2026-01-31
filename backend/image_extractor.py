
import re
import logging

class ImageExtractor:
    """
    Parses generated content for image placeholders.
    Format:
    <!-- IMAGE_PLACEHOLDER: IMG_CH01_01 -->
    <!-- DESCRIPTION: ... -->
    <!-- SUGGESTED_URLS:
      - url1
      - url2
    -->
    """
    
    def extract_placeholders(self, content: str) -> list:
        """
        Extract all image placeholders from the content.
        Returns a list of dicts: {'id': '', 'description': '', 'suggested_urls': []}
        """
        # Regex to find the whole block
        # We look for blocks starting with <!-- IMAGE_PLACEHOLDER and ending with the closing --> of parsed block
        
        placeholders = []
        
        # 1. Find all Placeholders IDs
        # Pattern for ID: <!-- IMAGE_PLACEHOLDER: (.*?) -->
        id_pattern = re.compile(r'<!-- IMAGE_PLACEHOLDER:\s*(.*?)\s*-->')
        
        # Find all matches
        # We need to scan the text and when we find an ID, we look ahead for description and urls
        # This is a bit tricky with regex alone, so let's split or iterate
        
        lines = content.split('\n')
        current_placeholder = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Start of block
            if line.startswith('<!-- IMAGE_PLACEHOLDER:'):
                match = id_pattern.match(line)
                if match:
                    current_placeholder = {
                        'id': match.group(1).strip(),
                        'description': '',
                        'suggested_urls': []
                    }
            
            # Description
            elif line.startswith('<!-- DESCRIPTION:'):
                if current_placeholder:
                    # Remove prefix and closing -->
                    desc = line.replace('<!-- DESCRIPTION:', '').replace('-->', '').strip()
                    current_placeholder['description'] = desc
            
            # URLs (Start)
            elif line.startswith('<!-- SUGGESTED_URLS:'):
                pass # Just a header
            
            # URL Item
            elif line.startswith('- http') and current_placeholder:
                # This assumes URLs are inside the comment block or just below it
                # The prompt asks for:
                # <!-- SUGGESTED_URLS:
                #   - url
                # -->
                # So these lines might be inside the comment or part of a list
                # Let's clean the line
                url = line.replace('-', '').strip()
                # Remove trailing --> if present (end of block)
                if url.endswith('-->'):
                    url = url.replace('-->', '').strip()
                
                if url:
                    current_placeholder['suggested_urls'].append(url)

            # End of block (End of URLs)
            elif '-->' in line and current_placeholder:
                # If this line closes the urls block
                if current_placeholder.get('id'):
                    placeholders.append(current_placeholder)
                    current_placeholder = {} # Reset
                    
        return placeholders
