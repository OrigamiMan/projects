alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "/"] 
roman = ["I ", "II ", "III ", "IV ", "V ", "VI ", "VII ", "VIII ", "IX ", "X ", "XI ", "XII ", "XIII ", "XIV ", "XV ", "XVI ", "XVII ", "XVIII ", "XIX ", "XX ", "XXI ", "XXII ", "XXIII ", "XXIV ", "XXV ", "XXVI ", ", ", " / "]

#letters0 = "to access the caverns crypt" 
#letters1 = "one must enter the cave from the southern side"
#letters2 = "and throw a crystal of red into the salty blue"
#letters3 = "then to find the sacred ritual"
#letters4 = "you must go to the water hole of green"
#letters5 = "and jump down close behind it"
#letters6 = "you must hurry you endangered soul"
#letters7 = "for whoever threw the crystal"
letters8 = "has only one earths rotation left to live"
result = []
for i in letters8:
    result.append(roman[alph.index(i)])
print("".join(result))