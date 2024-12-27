import tkinter as tk
from tkinter import font
import random, json

with open("scramblelist.txt") as f:
    word_list = [item.lower() for item in json.load(f)]

# Shuffle the word list to randomize on each run
random.shuffle(word_list)

# Function to scramble a word
def jumble(word):
    random_word = random.sample(word, len(word))
    print("---------before rescramble---------------")
    print("input word: {} scrambled word {}".format(word,''.join(random_word)))
    print("---------------------------")
    if(checkScrambleQuality(oword=word,nword=''.join(random_word))):
        print("----------------after rescramble-----------------")
        print("input word: {} scrambled word {}".format(word,''.join(random_word)))
        print("---------------------------")
        return ''.join(random_word)
    else:
        return jumble(word=word)

def checkSameWord(oword,nword):
    unique1 = set(oword)
    unique2 = set(nword)
    dist1 = {char:oword.count(char) for char in unique1}
    dist2 = {char:oword.count(char) for char in unique2}
    if dist1 != dist2:
        print("The letter distribution is wrong.")
        print("words are: {} and {}".format(oword,nword))
        input("press a key to ack")
        return False
    else:
        return True

def checkScrambleQuality(oword,nword):
    if oword == nword:
        return False
    if not checkSameWord(oword=oword,nword=nword):
        return False
    allowedSamePerc = 0.5
    sameCount = 0
    for i in range(len(oword)):
        if oword[i] == nword[i]:
            sameCount =+ 1
    samePerc = float(sameCount)/float(len(oword))
    if samePerc > allowedSamePerc:
        return False
    else:
        return True

# Prepare a list of scrambled words
scrambled_words = [jumble(word) for word in word_list]
current_index = 0

# Toggle state
show_original = False

# GUI setup
root = tk.Tk()
root.title("Word Scrambler")
root.attributes('-fullscreen', True)

# Fonts for text display
display_font = font.Font(family="Helvetica", size=48, weight="bold")

# Word label
word_label = tk.Label(root, text="", font=display_font)
word_label.pack(expand=True)

def update_word():
    """Update the word display based on current state and index."""
    global show_original
    if show_original:
        word_label.config(text=word_list[current_index])
    else:
        word_label.config(text=scrambled_words[current_index])

# Button handlers
def previous_word():
    global current_index
    global show_original
    show_original = False
    current_index = (current_index - 1) % len(word_list)
    update_word()

def next_word():
    global current_index
    global show_original
    show_original = False
    current_index = (current_index + 1) % len(word_list)
    update_word()

def toggle_answer():
    global show_original
    show_original = not show_original
    update_word()

def exit_program():
    root.destroy()

# Navigation buttons
button_font = font.Font(size=20)
previous_button = tk.Button(root, text="\u2190", bg="blue", fg="white", font=button_font, command=previous_word)
previous_button.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.07)

next_button = tk.Button(root, text="\u2192", bg="blue", fg="white", font=button_font, command=next_word)
next_button.place(relx=0.85, rely=0.9, relwidth=0.1, relheight=0.07)

# Toggle button
answer_button = tk.Button(root, text="ANSWER", bg="yellow", fg="black", font=button_font, command=toggle_answer)
answer_button.place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.07)

# Exit button
exit_button = tk.Button(root, text="EXIT", bg="red", fg="white", font=button_font, command=exit_program)
exit_button.place(relx=0.9, rely=0.05, relwidth=0.08, relheight=0.05)

# Initialize display
update_word()

# Run the application
root.mainloop()
