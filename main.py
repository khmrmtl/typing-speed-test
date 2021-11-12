import tkinter as tk

from random import randint
from words import WORDS_USED

class TypingSpeedTest(tk.Frame):
    def __init__(self, parent):
        super(TypingSpeedTest, self).__init__(parent)
        self.pack(padx=10, pady=20)
        self.create_widgets()

        # variables for checking
        self.entered_word = ""
        self.index = 0

        # user score
        self.typed_correct = 0

        self.timer = 60
        self.first_try = True

        self.ongoing = False

    def create_widgets(self):
        self.winfo_toplevel().title("Typing Speed Test")
        self.label = tk.Label(self, text="Calculates your cpm and wpm based on your performance", font=("Courier", 20))
        self.label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)


        self.start_button = tk.Button(self, text='Start', command=self.start)
        self.start_button.grid(row=1, column=0, columnspan=4)


    def get_user_input(self, key):
        if self.ongoing:
            self.entered_word += key.char
            if key.char == " ":
                self.check_user_input()
                self.user_input.delete(0, len(self.entered_word))
                self.entered_word = ""
                self.index += 1
                print(self.index)
            if self.index == 5:
                for index in range(0, len(self.words_generated)):
                    self.words_generated[index].grid_forget()
                self.generate_sentence()
                print(self.index)
                self.index = 0

    def check_user_input(self):
        print(f"|{self.entered_word}|{self.generated_sentencce[self.index]}|")
        if self.entered_word == f"{self.generated_sentencce[self.index]} ":
            self.words_generated[self.index].config(bg="green")
            self.typed_correct += len(self.entered_word)
        else:
            self.words_generated[self.index].config(bg="red")

    def generate_sentence(self):
        self.generated_sentencce = [WORDS_USED[randint(0, len(WORDS_USED) - 1)] for index in range(5)]
        self.words_generated = [tk.Label(self, text=word, font=("Courier", 20)) for word in self.generated_sentencce]
        print(self.generated_sentencce)
        for index in range(0, len(self.words_generated)):
            self.words_generated[index].grid(row=2, column=index, padx=1, pady=1)

    def start(self):
        self.ongoing = True
        self.start_button.grid_forget()
        self.generate_sentence()
        self.label.config(text="Begin typing")

        self.user_input = tk.Entry(self, bg="white", font=("Courier", 20))
        self.user_input.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
        self.user_input.bind("<Key>", self.get_user_input)

        if self.first_try:
            self.timer_label = tk.Label(text=self.timer, font=("Courier", 20))
            self.timer_label.pack()

        print(self.timer)
        self.after(1000, self.countdown)

        try:
            self.time_up_label.config(text="")
            self.timer_label.config(text=self.timer)
            self.cpm_label.config(text="")
            self.wpm_label.config(text="")
        except AttributeError:
            pass

    def countdown(self):

        if self.timer < 1:
            self.ongoing = False
            self.index = 0
            self.timer = 60
            self.update()

            self.wpm = int((self.typed_correct / 5))
            self.cpm = self.typed_correct

            self.typed_correct = 0

            if self.first_try:
                self.time_up_label = tk.Label(text="Time's Up")
                self.time_up_label.pack()

                self.cpm_label = tk.Label(text=f"Your CPM: {self.cpm}", font=("Courier", 20))
                self.cpm_label.pack()

                self.wpm_label = tk.Label(text=f"Your WPM: {self.wpm}", font=("Courier", 20))
                self.wpm_label.pack()

                self.first_try = False
            else:
                self.time_up_label.config(text="Time's Up")
                self.cpm_label.config(text=f"Your CPM: {self.cpm}")
                self.wpm_label.config(text=f"Your WPM: {self.wpm}")


            self.start_button.grid(row=1, column=0, columnspan=4)
            self.label.config(text="Try again")

            self.user_input.grid_forget()

            for index in range(0, len(self.words_generated)):
                self.words_generated[index].grid_forget()

        else:
            self.timer -= 1
            self.timer_label.config(text=self.timer)
            print(self.timer)
            self.after(1000, self.countdown)

if __name__ == "__main__":
    root = tk.Tk()

    app = TypingSpeedTest(root)
    root.minsize(900, 500)
    app.mainloop()
