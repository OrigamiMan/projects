cache = {
    1: {"A": 1},
}


letter_scores = {chr(i + ord('A')): i + 1 for i in range(26)}

def word_score(word: str):
    score = 0
    for l in word:
        score += letter_scores[l]
    return score

def build_cache(score: int):
    for i in range(2, score+1):
        table = {}
        for j in range(min(i, 26)):
            key = chr(j + ord('A'))
            if (i - j - 1) == 0:
                table[key] = 1
            else:
                table[key] = sum([v for k, v in cache[i - j - 1].items() if k != key])
        cache[i] = table
        
def find_order(word: str):
    score = word_score(word)
    build_cache(score)
    words_before = 0
    for l in range(len(word)):
        letter_score = letter_scores[word[l]]
        for i in range(letter_score - 1):
            key = chr(i + ord('A'))
            if key == word[l-1]:
                continue
            words_before += cache[score][key]
        score -= letter_score
    return words_before + 1


print(find_order("BAB"))
print(find_order("A"))
print(find_order("GA"))
print(find_order("DEAD"))
print(find_order("R"))
print(find_order("BIO"))
print(find_order("DOG"))
print(find_order("ALGAE"))
print(find_order("NICE"))
print(find_order("ALGOL"))
print(find_order("ZY"))
print(find_order("LIKELY"))