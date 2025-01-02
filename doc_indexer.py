import os
import re
from collections import defaultdict
import markdown
from bs4 import BeautifulSoup

class DocIndexer:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
        self.terms = defaultdict(set)  # Terms and their occurrences
        self.acronyms = defaultdict(set)  # Acronyms and their occurrences
        self.toc = defaultdict(list)  # Table of contents by file
        
    def find_markdown_files(self):
        """Recursively find all markdown files."""
        markdown_files = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(('.md', '.markdown')):
                    markdown_files.append(os.path.join(root, file))
        return markdown_files
    
    def extract_headings(self, content, file_path):
        """Extract headings and create TOC entries."""
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            level = int(heading.name[1])  # Get heading level (1-6)
            text = heading.text.strip()
            # Create GitHub-style anchor link
            anchor = text.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')
            self.toc[file_path].append((level, text, anchor))
            
    def extract_terms_and_acronyms(self, content, file_path):
        """Extract technical terms and acronyms."""
        # Find potential technical terms (CamelCase, snake_case, or hyphenated words)
        tech_terms = re.findall(r'\b(?:[A-Z][a-z]+[A-Z][a-z]+[a-zA-Z]*|[a-z]+_[a-z]+(?:_[a-z]+)*|[a-z]+-[a-z]+(?:-[a-z]+)*)\b', content)
        for term in tech_terms:
            self.terms[term].add(file_path)
            
        # Find potential acronyms (2+ uppercase letters)
        acronyms = re.findall(r'\b[A-Z]{2,}s?\b', content)
        for acronym in acronyms:
            self.acronyms[acronym].add(file_path)
    
    def process_file(self, file_path):
        """Process a single markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            rel_path = os.path.relpath(file_path, self.root_dir)
            self.extract_headings(content, rel_path)
            self.extract_terms_and_acronyms(content, rel_path)
            
            # Update the file with TOC if needed
            if self.toc[rel_path]:
                self.update_file_toc(file_path, content)
                
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    def update_file_toc(self, file_path, content):
        """Update or create TOC section in the file."""
        toc_lines = ["## Table of Contents\n"]
        for level, text, anchor in self.toc[os.path.relpath(file_path, self.root_dir)]:
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}- [{text}](#{anchor})\n")
        
        toc_content = "".join(toc_lines)
        
        # Check if TOC already exists
        toc_pattern = re.compile(r'## Table of Contents\n(?:[ \t]*-[^\n]*\n)*\n')
        if re.search(toc_pattern, content):
            new_content = re.sub(toc_pattern, toc_content + "\n", content)
        else:
            # Insert after first heading if it exists, otherwise at the start
            first_heading = re.search(r'^#[^#].*$', content, re.MULTILINE)
            if first_heading:
                pos = first_heading.end()
                new_content = content[:pos] + "\n\n" + toc_content + "\n" + content[pos:]
            else:
                new_content = toc_content + "\n" + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    def generate_index(self):
        """Generate main index file with all terms, acronyms, and file listing."""
        index_content = ["# Documentation Index\n\n"]
        
        # Add file listing with TOCs
        index_content.append("## Files\n\n")
        for file_path, headings in sorted(self.toc.items()):
            index_content.append(f"### {file_path}\n\n")
            for level, text, anchor in headings:
                indent = "  " * (level - 1)
                index_content.append(f"{indent}- [{text}]({file_path}#{anchor})\n")
            index_content.append("\n")
        
        # Add terms glossary
        index_content.append("## Technical Terms\n\n")
        for term, files in sorted(self.terms.items()):
            index_content.append(f"- **{term}**\n")
            for file_path in sorted(files):
                index_content.append(f"  - [{file_path}]({file_path})\n")
        index_content.append("\n")
        
        # Add acronyms glossary
        index_content.append("## Acronyms\n\n")
        for acronym, files in sorted(self.acronyms.items()):
            index_content.append(f"- **{acronym}**\n")
            for file_path in sorted(files):
                index_content.append(f"  - [{file_path}]({file_path})\n")
        
        # Write index file
        with open(os.path.join(self.root_dir, 'INDEX.md'), 'w', encoding='utf-8') as f:
            f.write("".join(index_content))

def main():
    indexer = DocIndexer()
    print("Finding markdown files...")
    markdown_files = indexer.find_markdown_files()
    
    print(f"Processing {len(markdown_files)} files...")
    for file_path in markdown_files:
        print(f"Processing {file_path}")
        indexer.process_file(file_path)
    
    print("Generating main index...")
    indexer.generate_index()
    print("Done! Check INDEX.md for the complete documentation index.")

if __name__ == "__main__":
    main()
