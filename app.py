import tkinter as tk
import pages
from curl_cffi import requests
import asyncio


class App(tk.Tk):  # TODO: add how this was taken from stackOverflow
    chosen_movie = ""
    recommendations = []

    genres = set()

    scraper = requests.AsyncSession(impersonate="chrome")

    event_loop = asyncio.new_event_loop()

    def __init__(self):
        super().__init__()
        self.title("BingeBuddy: A Personalized Movie Recommendation System")
        self.geometry("1566x968")

        asyncio.set_event_loop(self.event_loop)

        canvas = tk.Canvas(self, bg="#3C1D53")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        container = tk.Frame(canvas, bg="#3C1D53")
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
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
