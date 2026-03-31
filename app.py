import tkinter as tk
import asyncio
from curl_cffi import requests

import pages

BG_COLOUR = "#3C1D53"


class App(tk.Tk):
    """Main application class for the GUI

    This class initializes the root Tkinter window and manages global variables whose values
    are updated throughout the program (e.g. chosen_movie and recommendations).

    Instance Attributes:
        - chosen_movie: the movie the user chooses as their favourite
        - recommendations: the list of recommendations we compute based on their favourite movie
        - fav_genres: the user's favourite genres stored in a set
        - scraper: the scraper tool used to get information from letterboxd
        - frames: a dict to hold instances of all frames in this application with their names as keys
    """
    chosen_movie: str
    recommendations: list[str]
    fav_genres: set
    scraper: requests.AsyncSession
    event_loop: asyncio.AbstractEventLoop
    frames: dict[str, tk.Frame]

    def __init__(self) -> None:
        super().__init__()

        self.title("BingeBuddy: A Personalized Movie Recommendation System")
        self.geometry("1566x968")

        # Instance variables
        self.chosen_movie = ""
        self.recommendations = []
        self.fav_genres = set()
        self.scraper = requests.AsyncSession(impersonate="chrome")
        self.event_loop = asyncio.new_event_loop()
        self.frames = {}

        asyncio.set_event_loop(self.event_loop)

        # GUI elements
        canvas = tk.Canvas(self, bg=BG_COLOUR)  # canvas to hold scrollbar
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)  # creating scrollbar

        container = tk.Frame(canvas, bg=BG_COLOUR)  # container to hold other frames
        container.pack(fill="both", expand=True)

        for page in (
            pages.StarterPage,
            pages.QuestionsPage,
            pages.MovieConfirmPage,
            pages.RecommendationsPage,
        ):  # iteratively creating each frame. NOTE: This is inspired by the following on StackOverflow:
            # https: // stackoverflow.com / questions / 7546050 / switch - between - two - frames - in -tkinter
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

        self.switch_frame("StarterPage")  # Displaying the starter page

    def switch_frame(self, frame_name: str) -> None:
        """Raise given frame so that it is visible"""
        frame = self.frames[frame_name]
        frame.tkraise()

    def switch_btn_hover(
        self,
        btn: tk.Label,
        image_hover: tk.PhotoImage,
        image_static: tk.PhotoImage,
        is_hover: bool,
    ) -> None:
        """Switch button cover to hover version or static version based on if is_hover is True."""
        if is_hover:
            btn.config(image=image_hover)
        else:
            btn.config(image=image_static)
