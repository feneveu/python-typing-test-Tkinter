import tkinter as tk
import time
from wonderwords import RandomWord


def create_text():
    """Creates a random paragraph that is 20 words long"""
    text = RandomWord().word()  # first word in para
    # continually adds words to the paragraph
    for i in range(20):
        word = RandomWord().word()
        text = text + ' ' + word
    #  print(text)  # would print to the screen the paragraph made
    return text


class TypingSpeedTest:

    def __init__(self, root):
        self.root = root  # the window that everything is on
        self.root.title("Typing Speed Test")
        self.root.geometry('600x400')  # size of the window everything is on
        self.root.configure(bg="#B3D8A8")  # Changed background color

        # text obj to be used later in the label
        self.text = 'Please Type the Words you see on screen after pressing start'
        # there is no start time to begin with
        self.start_time = None

        # creates the heading label
        tk.Label(root, text="Type the following:", background='#FBFFE4', font=('Arial', 10)).pack()
        self.text_label = (tk.Label(root, text=self.text, wraplength=400, font=("Arial", 12), background="#B3D8A8"))
        self.text_label.pack()

        #  creates the entry area
        self.entry = tk.Text(root, height=4, width=50, font=("Arial", 12), relief="solid", bd=2)
        self.entry.pack(pady=5)

        # at key release do the function highlight errors (see if user typed an error)
        self.entry.bind("<KeyRelease>", self.highlight_errors)
        # at enter press calculate time/accuracy
        self.entry.bind("<Return>", self.calculate_speed)

        # creates the start button which correlates to the start function
        self.start_button = tk.Button(root, text="Start", font=("Arial", 12, "bold"), bg="#3D8D7A", fg="#FBFFE4",
                                      relief="flat", padx=10, pady=5, command=self.start_test)
        self.start_button.pack(pady=5)

        # this shows the result which is shown as none at the start
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#0984e3", bg="#dfe6e9")
        self.result_label.pack(pady=5)

    def start_test(self):
        """initiates the test"""
        self.text = create_text()  # Reset text for new test
        self.text_label.config(text=self.text)  # Shows the prompt to screen
        self.entry.delete("1.0", tk.END)  # delete any previous words in entry box
        self.entry.focus()  # makes that input the active element to receiving user input
        self.start_time = time.time()  # keeps track of starting time
        self.result_label.config(text="Start typing!", fg='#FBFFE4', bg='#3D8D7A')

    def highlight_errors(self, event):
        """highlights errors in the display if user types wrong input"""
        typed_text = self.entry.get("1.0", tk.END).strip()  # gets what user types
        highlighted_text = ""  # starts with no highlighted text

        for i, char in enumerate(self.text):
            # i = index and char = element in self.text
            # if the index is inside the typed text continue
            if i < len(typed_text):
                # User typed word correctly
                if char == typed_text[i]:
                    highlighted_text += char
                # User typed the word incorrectly puts [word]
                else:
                    highlighted_text += f"[{char}]"
            else:
                highlighted_text += char

        # configure the text output
        self.text_label.config(text=highlighted_text)

    def calculate_speed(self, event):
        """calculates the speed of the user"""
        # if the user hasn't started typing there is no result
        if self.start_time is None:
            return

        # the end time is the moment this function is called
        end_time = time.time()
        # the difference
        elapsed_time = end_time - self.start_time
        # the words from para
        typed_text = self.entry.get("1.0", tk.END).strip()
        # words typed list
        words_typed = len(typed_text.split())

        # WPM is words_typed/Time * 60 since time was in seconds
        wpm = (words_typed / elapsed_time) * 60 if elapsed_time > 0 else 0
        # iterates thorough a and b at the same iteration and check if they are the same
        # if a == b then add 1, divide by total num of words * 100 for a percent value
        accuracy = sum(1 for a, b in zip(typed_text, self.text) if a == b) / len(self.text) * 100

        # output this to the screen  with decimal precision of 2
        self.result_label.config(text=f"Speed: {wpm:.2f} WPM, Accuracy: {accuracy:.2f}%", fg="#FBFFE4", bg='#3D8D7A')

        # resets timer
        self.start_time = None


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
