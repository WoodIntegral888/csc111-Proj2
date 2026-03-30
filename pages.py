import tkinter as tk
from tkinter import messagebox
import difflib
from PIL import Image, ImageTk

from scraper import is_vaild_movie, load_movie_image, get_movie_extra_info
from review_graph import ReviewGraph

import scraper
import asyncio


class StarterPage(tk.Frame):
    def __init__(self, container: tk.Frame, root):
        super().__init__(container, bg="#3C1D53")
        self.load_logo()
        self.load_started_btn(root)

    def load_logo(self):
        logo = tk.PhotoImage(file="images/bingeBuddyLogo1.png").subsample(2)
        logo_label = tk.Label(self, image=logo, bg="#3C1D53")
        logo_label.image = logo
        logo_label.pack()

    def load_started_btn(self, root):
        btn_static = tk.PhotoImage(file="images/startedBtn1.png").subsample(2)
        btn_hover = tk.PhotoImage(file="images/startedBtn2.png").subsample(2)

        button = tk.Label(self, image=btn_static, bg="#3C1D53")
        button.image = btn_static
        button.pack()

        button.bind("<Button-1>", lambda e: root.switch_frame("QuestionsPage"))
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )


class QuestionsPage(tk.Frame):
    genres_list = [
        "action",
        "comedy",
        "documentary",
        "drama",
        "horror",
        "mystery",
        "romance",
        "science ficition",
    ]
    genre_variables = []
    favMovieAnswerVar = ""

    def __init__(self, container: tk.Frame, root):
        super().__init__(container, bg="#3C1D53")
        title = tk.Label(
            self,
            text="Let's get to know you better...",
            font=("Futura-Bold", 75),
            bg="#3C1D53",
            anchor="w",
            fg="#AC57EA",
        )
        title.pack()

        self.load_fav_movie_question()
        self.load_fav_genre_question()
        self.load_submit_btn(root)

    def load_fav_movie_question(self):
        favMovieQuestion = tk.Label(
            self,
            text="What's your favourite movie?",
            font=("Futura-Bold", 40),
            bg="#3C1D53",
            anchor="w",
            fg="#DA34B4",
            height=2,
        )
        favMovieQuestion.pack()
        self.favMovieAnswerVar = tk.StringVar()

        favMovieAnswerBox = tk.Entry(
            self,
            bg="#85CFFF",
            font=("Futura-Bold", 20),
            fg="#3C1D53",
            textvariable=self.favMovieAnswerVar,
            width=45,
        )
        favMovieAnswerBox.pack()
        favMovieAnswerBox.focus_force()

    def load_fav_genre_question(self):
        favGenreQuestion = tk.Label(
            self,
            text="What are your favourite genres? (Pick up to 3)",
            font=("Futura-Bold", 40),
            bg="#3C1D53",
            anchor="w",
            fg="#DA34B4",
            height=2,
        )
        favGenreQuestion.pack()

        for i in range(len(self.genres_list)):
            self.genre_variables.append(tk.IntVar())

        for j in range(len(self.genres_list)):
            genreOption = tk.Checkbutton(
                self,
                text=self.genres_list[j].upper(),
                variable=self.genre_variables[j],
                onvalue=1,
                offvalue=0,
                font=("Futura-Bold", 20),
                anchor="w",
                bg="#3C1D53",
                fg="#85CFFF",
                width=17,
            )
            genreOption.pack()

    def load_submit_btn(self, root):
        btn_static = tk.PhotoImage(file="images/submitBtn1.png").subsample(3)
        btn_hover = tk.PhotoImage(file="images/submitBtn2.png").subsample(3)

        button = tk.Label(self, image=btn_static, bg="#3C1D53")
        button.image = btn_static
        button.pack(pady=30)

        button.bind("<Button-1>", lambda e: self.check_submit(root))
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def check_submit(self, root):

        movie_name = self.favMovieAnswerVar.get()

        vaild_movie = root.event_loop.run_until_complete(
            is_vaild_movie(movie_name, root.scraper)
        )

        if not vaild_movie:
            messagebox.showerror(
                "showerror",
                "Sorry, we are unable to recognize your movie input. Please try again.",
            )
        if not self.is_valid_genre_selection():
            messagebox.showerror("showerror", "Please select AT MOST 3 genres.")
        elif vaild_movie:
            root.event_loop.run_until_complete(
                load_movie_image(movie_name, root.scraper)
            )
            root.chosen_movie = movie_name
            for i in range(len(self.genre_variables)):
                if self.genre_variables[i] == 1:
                    root.genres.add(self.genres_list[i])
            root.switch_frame("MovieConfirmPage")

    def is_valid_genre_selection(self) -> bool:
        return [genre_var.get() for genre_var in self.genre_variables].count(1) <= 3


class MovieConfirmPage(tk.Frame):
    def __init__(self, container: tk.Frame, root):
        super().__init__(container, bg="#3C1D53")
        title = tk.Label(
            self,
            text="Are we on the right track?",
            font=("Futura-Bold", 75),
            bg="#3C1D53",
            anchor="w",
            fg="#AC57EA",
        )
        title.pack()

        btn_static = tk.PhotoImage(file="images/seeResults1.png")
        btn_hover = tk.PhotoImage(file="images/seeResults2.png")

        button = tk.Label(self, image=btn_static, bg="#3C1D53")
        button.image = btn_static
        button.pack(pady="100")

        button.bind("<Button-1>", lambda e: self.load_options(root, button))
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def load_options(self, root, button):
        button.destroy()
        subheading = tk.Label(
            self,
            text="Pick the movie you're talking about...",
            font=("Futura-Bold", 40),
            bg="#3C1D53",
            anchor="w",
            fg="#DA34B4",
            height=2,
        )
        subheading.pack()

        # for result in search_results:
        image_file = Image.open(f"./images/{root.chosen_movie}.jpg")

        imgStatic_file = image_file.resize((356, 200))
        imgHover_file = image_file.resize((360, 202))

        self.load_interact_option(
            root, imgStatic_file, imgHover_file, root.chosen_movie
        )

    def load_interact_option(
        self, root, static_img_file, hover_img_file, movie_name: str
    ):
        staticImg = ImageTk.PhotoImage(static_img_file)
        hoverImg = ImageTk.PhotoImage(hover_img_file)

        resultDisplay = tk.Label(
            self,
            text=movie_name,
            image=staticImg,
            font=("Futura-Bold", 20),
            anchor="w",
            bg="#3C1D53",
            fg="#85CFFF",
            compound="top",
        )
        resultDisplay.image = staticImg
        resultDisplay.pack()

        resultDisplay.bind(
            "<Button-1>", lambda e: self.set_selected_movie(root, movie_name)
        )
        resultDisplay.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(resultDisplay, hoverImg, staticImg, True),
        )
        resultDisplay.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(resultDisplay, hoverImg, staticImg, False),
        )

    def set_selected_movie(self, root, movie_name):
        root.chosen_movie = movie_name
        print(root.chosen_movie)
        root.switch_frame("RecommendationsPage")


class RecommendationsPage(tk.Frame):
    def __init__(self, container: tk.Frame, root):
        super().__init__(container, bg="#3C1D53")

        title = tk.Label(
            self,
            text="Our Recommendations",
            font=("Futura-Bold", 75),
            bg="#3C1D53",
            anchor="w",
            fg="#AC57EA",
        )
        title.pack()

        btn_static = tk.PhotoImage(file="images/startedBtn1.png")
        btn_hover = tk.PhotoImage(file="images/startedBtn2.png")

        button = tk.Label(self, image=btn_static, bg="#3C1D53")
        button.image = btn_static
        button.pack(pady="100")

        button.bind(
            "<Button-1>", lambda e: self.calculate_recommendations(root, button)
        )
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def calculate_recommendations(self, root, button):
        button.destroy()

        genres = root.genres

        print(genres)

        users_and_reviews = root.event_loop.run_until_complete(
            scraper.viewers_and_reviews_from_movie(
                root.chosen_movie, root.scraper, viewer_count=10
            )
        )

        import pprint

        review_graph = ReviewGraph()
        for user, reviews in users_and_reviews.items():
            pprint.pprint(user)
            pprint.pprint(reviews)
            review_graph.insert_user_and_watched_movies(user, reviews)

        recommendation_list_long = review_graph.get_recommendation_list(
            root.chosen_movie
        )

        extra_info = root.event_loop.run_until_complete(
            get_movie_extra_info(recommendation_list_long, root.scraper)
        )

        top_five_movies = extra_info[1:6]

        # root.event_loop.run_until_complete(
        #     asyncio.gather(
        #         *[
        #             load_movie_image(recommendation, root.scraper)
        #             for recommendation in recommendation_list_five
        #         ]
        #     )
        # )

        # root.recommendations = recommendation_list_five

        # print(recommendation_list_five)

        # print("recs: " + str(root.recommendations))

        # btn_static = tk.PhotoImage(file="images/seeResults1.png")
        # btn_hover = tk.PhotoImage(file="images/seeResults2.png")

        # button = tk.Label(self, image=btn_static, bg="#3C1D53")
        # button.image = btn_static
        # button.pack(pady="100")

        # button.bind("<Button-1>", lambda e: self.load_options(root, button))
        # button.bind(
        #     "<Enter>",
        #     lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        # )
        # button.bind(
        #     "<Leave>",
        #     lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        # )

    def load_options(self, root, button):
        button.destroy()
        subheading = tk.Label(
            self,
            text=f"Because you liked {root.chosen_movie}...",
            font=("Futura-Bold", 40),
            bg="#3C1D53",
            anchor="w",
            fg="#DA34B4",
            height=2,
        )
        subheading.pack()

        for recommendation in root.recommendations:
            print(recommendation)
            # image_file = Image.open(f"../images/{recommendation}.jpg")
            # image_file = image_file.resize((356, 200))
            # img = ImageTk.PhotoImage(image_file)
            # resultDisplay = tk.Label(
            #     self,
            #     text=recommendation,
            #     image=img,
            #     font=("Futura-Bold", 20),
            #     anchor="w",
            #     bg="#3C1D53",
            #     fg="#85CFFF",
            #     compound="top",
            # )
            # resultDisplay.image = img
            # resultDisplay.pack(side="left")
            # fake_text = {}
            # descrip = tk.Label(
            #     self,
            #     text=recommendation,
            #     font=("Futura-Bold", 20),
            #     bg="#3C1D53",
            #     fg="#85CFFF",
            #     compound="top",
            # )
            # descrip.pack()
