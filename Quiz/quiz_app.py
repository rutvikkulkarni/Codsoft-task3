import tkinter as tk
from tkinter import ttk
import json
import random
from ttkthemes import ThemedStyle


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz App")
        self.root.geometry("500x400")
        self.questions = self.load_questions("quiz_questions.json")
        self.total_questions = len(self.questions)
        self.score = 0

        self.style = ThemedStyle(self.root)
        self.style.set_theme("plastik")

        self.question_label = ttk.Label(
            root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.option_var = tk.IntVar()
        self.option_buttons = []

        for i in range(4):
            button = ttk.Radiobutton(
                root,
                text="",
                variable=self.option_var,
                value=i,
                command=self.enable_submit_button,
                style="Dark.TRadiobutton"
            )
            self.option_buttons.append(button)
            button.pack()

        self.submit_button = ttk.Button(
            root, text="Submit", command=self.submit_answer, state=tk.DISABLED)
        self.submit_button.pack(pady=10)

        self.restart_button = ttk.Button(
            root, text="Restart Quiz", command=self.restart_quiz, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        self.current_question_idx = -1
        self.load_question()

    def load_questions(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
        return data["questions"]

    def load_question(self):
        self.current_question_idx += 1
        if self.current_question_idx < self.total_questions:
            question = self.questions[self.current_question_idx]
            self.current_question = question
            self.question_label.config(text=question["question"])

            options = random.sample(
                question["options"], len(question["options"]))
            for i in range(4):
                self.option_buttons[i].config(text=options[i], state=tk.NORMAL)

            self.option_var.set(-1)
            self.submit_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.DISABLED)
        else:
            self.show_result()

    def enable_submit_button(self):
        self.submit_button.config(state=tk.NORMAL)

    def submit_answer(self):
        user_answer = self.option_buttons[self.option_var.get()]["text"]
        if user_answer == self.current_question["answer"]:
            self.score += 1

        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

        self.submit_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)
        self.root.after(1000, self.load_question)

    def show_result(self):
        self.question_label.config(
            text=f"Quiz completed! You got {self.score}/{self.total_questions} questions correct.")
        self.submit_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def restart_quiz(self):
        self.score = 0
        self.current_question_idx = -1
        random.shuffle(self.questions)
        self.load_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
