from time import time

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"



letter_scores = {chr(i + ord('A')): i + 1 for i in range(26)}

def word_score(word: str):
    score = 0
    for l in word:
        score += letter_scores[l]
    return score


def alphebetically_before(target: str, in_question: str):
    for i in range(min(len(target), len(in_question))):
        if letter_scores[target[i]] > letter_scores[in_question[i]]:
            #in_question is alphabetically before
            return False
        if letter_scores[target[i]] < letter_scores[in_question[i]]:
            #in_question is alphabetically after
            return True
    return False

def next_iterations(word: str, score: int):
    banned = word[-1]
    new = []
    for i in reversed(range(26)):
        if alph[i] == banned:
            continue
        if i >= score:
            continue
        new.append((word + alph[i], score - i - 1))
    return new
        
def all_words(target: str):
    score = word_score(target)
    queue = ([(alph[i], score - i - 1) for i in reversed(range(26))] if score >= 26 else [(alph[i], score - i - 1) for i in reversed(range(score))])

    done = []
    while queue:
        next_word, next_score = queue.pop()
        if alphebetically_before(target, next_word):
            continue
        if next_score == 0:
            done.append(next_word)
            if next_word == target:
                print(len(done))
            continue

        queue += next_iterations(next_word, next_score)


all_words("NICE")

