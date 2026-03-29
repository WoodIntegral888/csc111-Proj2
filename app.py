import tkinter as tk
import pages
from curl_cffi import requests


class App(tk.Tk):  # TODO: add how this was taken from stackOverflow
    # movies = {"ape", "apple", "peach", "puppy"}
    chosen_movie = ""
    # recommendations = {"ape", "apple"}  # TODO: replace this with the actual reccs
    recommendations = []

    genres = set()

    scraper = requests.Session(impersonate="chrome")

    def __init__(self):
        super().__init__()
        self.title("BingeBuddy: A Personalized Movie Recommendation System")
        self.geometry("1566x968")

        container = tk.Frame(self, bg="#3C1D53")
        container.pack(fill="both", expand=True)

        self.frames = {}  # TODO: add this to class variants

        for page in (
            pages.StarterPage,
            pages.QuestionsPage,
            pages.MovieConfirmPage,
            pages.RecommendationsPage,
        ):
            page_name = page.__name__
            frame = page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.switch_frame("StarterPage")

    def switch_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def switch_btn_hover(
        self,
        btn: tk.Label,
        image_hover: tk.PhotoImage,
        image_static: tk.PhotoImage,
        is_hover: bool,
    ) -> None:
        if is_hover:
            btn.config(image=image_hover)
        else:
            btn.config(image=image_static)
