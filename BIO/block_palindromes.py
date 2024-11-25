def is_palindrome_section(section: str):
    return section == section[::-1]

def generate_sections(word):
    if not word:
        return [[]]
    
    sections = []

    for i in range(len(word)):
        first = word[:i+1]
        last = word[i+1:]
        
        other_sections = generate_sections(last)
        
        for s in other_sections:
            sections.append([first] + s)
    
    return sections

def count_block_palindromes(word):
    sections = generate_sections(word)
    
    valid_palindromes = 0
    for section in sections:
        if is_palindrome_section(section):
            valid_palindromes += 1
    
    return valid_palindromes - 1


word = "AAAAAAAAAA"
print(count_block_palindromes(word))