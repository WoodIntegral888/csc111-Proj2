import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import scraper
from scraper import is_vaild_movie, load_movie_image, get_movie_extra_info
from review_graph import ReviewGraph

BG_COLOUR = "#3C1D53"
LIGHT_PURPLE = "#AC57EA"
PINK = "#DA34B4"
LIGHT_BLUE = "#85CFFF"


class StarterPage(tk.Frame):
    """Landing page of application

    This frame displays our logo and a button that allows the user to begin the application.
    """
    def __init__(self, container: tk.Frame, root: "App") -> None:
        """Initialize the StarterPage UI components"""
        super().__init__(container, bg=BG_COLOUR)
        self.load_logo()
        self.load_started_btn(root)

    def load_logo(self) -> None:
        """Load and display the BingeBuddy logo on the page"""
        logo = tk.PhotoImage(file="images/bingeBuddyLogo1.png").subsample(2)
        logo_label = tk.Label(self, image=logo, bg=BG_COLOUR)
        logo_label.image = logo
        logo_label.pack()

    def load_started_btn(self, root: "App") -> None:
        """Load and display the 'Get Started' button on the page"""
        btn_static = tk.PhotoImage(file="images/startedBtn1.png").subsample(2)
        btn_hover = tk.PhotoImage(file="images/startedBtn2.png").subsample(2)

        button = tk.Label(self, image=btn_static, bg=BG_COLOUR)
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
    """Question form page

    This frame displays the questions the user needs to fill out so that we can collect the
    necessary information needed for our recommendation computations.

    Instance Attributes:
        - genres_list: the list of possible genres the user can select as their favourite
        - fav_movie_answer_var: the movie the user inputs as their favourite
        - genre_variables: list of the user's favourite genres
    """
    genre_list: list[str]
    fav_movie_answer_var: tk.StringVar
    genre_variables: list[tk.IntVar]

    def __init__(self, container: tk.Frame, root: "App") -> None:
        """Initialize the QuestionsPage by creating instance variables and loading GUI components"""
        super().__init__(container, bg=BG_COLOUR)

        # Instance Variables
        self.genres_list = [
            "action",
            "comedy",
            "documentary",
            "drama",
            "horror",
            "mystery",
            "romance",
            "science ficition",
        ]
        self.fav_movie_answer_var = tk.StringVar()
        self.genre_variables = []

        # GUI elements
        title = tk.Label(
            self,
            text="Let's get to know you better...",
            font=("Futura-Bold", 75),
            bg=BG_COLOUR,
            anchor="w",
            fg=LIGHT_PURPLE,
        )
        title.pack()

        self.load_fav_movie_question()
        self.load_fav_genre_question()
        self.load_submit_btn(root)

    def load_fav_movie_question(self) -> None:
        """Load and display the favourite movie question"""
        fav_movie_question = tk.Label(
            self,
            text="What's your favourite movie?",
            font=("Futura-Bold", 40),
            bg=BG_COLOUR,
            anchor="w",
            fg=PINK,
            height=2,
        )
        fav_movie_question.pack()

        fav_movie_answer_box = tk.Entry(
            self,
            bg=LIGHT_BLUE,
            font=("Futura-Bold", 20),
            fg=BG_COLOUR,
            textvariable=self.fav_movie_answer_var,
            width=45,
        )
        fav_movie_answer_box.pack()
        fav_movie_answer_box.focus_force()

    def load_fav_genre_question(self) -> None:
        """Load and display the favourite genre question"""
        fav_genre_question = tk.Label(
            self,
            text="What are your favourite genres? (Pick up to 3)",
            font=("Futura-Bold", 40),
            bg=BG_COLOUR,
            anchor="w",
            fg=PINK,
            height=2,
        )
        fav_genre_question.pack()

        # Iteratively creating variables to hold if checkboxes are checked
        for i in range(len(self.genres_list)):
            self.genre_variables.append(tk.IntVar())

        # Iteratively creating the checkboxes
        for j in range(len(self.genres_list)):
            genre_option = tk.Checkbutton(
                self,
                text=self.genres_list[j].upper(),
                variable=self.genre_variables[j],
                onvalue=1,
                offvalue=0,
                font=("Futura-Bold", 20),
                anchor="w",
                bg=BG_COLOUR,
                fg=LIGHT_BLUE,
                width=17,
            )
            genre_option.pack()

    def load_submit_btn(self, root: "App") -> None:
        """Load and display the submit button so user can submit their responses to the questions"""
        btn_static = tk.PhotoImage(file="images/submitBtn1.png").subsample(3)
        btn_hover = tk.PhotoImage(file="images/submitBtn2.png").subsample(3)

        button = tk.Label(self, image=btn_static, bg=BG_COLOUR)
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

    def check_submit(self, root: "App") -> None:
        """Check if the user's replies are valid, i.e. if they have entered a movie that exists
        in the letterboxd database and if the have selected 3 or less genres as their favourite.
        """

        movie_name = self.fav_movie_answer_var.get().lower()  # Storing their response to the movie question

        vaild_movie = root.event_loop.run_until_complete(
            is_vaild_movie(movie_name, root.scraper)  # Checking if the movie is in the letterboxd database
        )

        if not vaild_movie:  # if their movie entry is not valid...
            messagebox.showerror(
                "showerror",
                "Sorry, we are unable to recognize your movie input. Please try again.",
            )  # display the error message
        if not self.is_valid_genre_selection():   # if they selected too many genres...
            # display the error message
            messagebox.showerror("showerror", "Please select AT MOST 3 genres.")
        elif vaild_movie:
            # Load the image for the movie and save it to the images folder
            root.event_loop.run_until_complete(
                load_movie_image(movie_name, root.scraper)
            )
            # Save the movie name as the chosen movie to reference later
            root.chosen_movie = movie_name
            # Iteratively check which checkboxes have been checked
            for i in range(len(self.genre_variables)):
                if self.genre_variables[i] == 1:
                    root.fav_genres.add(self.genres_list[i])  # Adding them to the user's favourite genre list
            root.switch_frame("MovieConfirmPage")  # Switching to the next page

    def is_valid_genre_selection(self) -> bool:
        """Check if maximum 3 checkboxes are selected"""
        return [genre_var.get() for genre_var in self.genre_variables].count(1) <= 3


class MovieConfirmPage(tk.Frame):
    """Movie confirmation page

    This frame shows the user the movie we have found that matches their entry under
    the favourite movie question. By clicking the movie, their choice is locked in.
    """
    def __init__(self, container: tk.Frame, root: "App") -> None:
        """Initialize the MovieConfirmPage and its GUI components"""
        super().__init__(container, bg=BG_COLOUR)
        title = tk.Label(
            self,
            text="Are we on the right track?",
            font=("Futura-Bold", 75),
            bg=BG_COLOUR,
            anchor="w",
            fg=LIGHT_PURPLE,
        )
        title.pack()

        # Create and display the button to begin retrival of the user's movie choice
        btn_static = tk.PhotoImage(file="images/seeResults1.png")
        btn_hover = tk.PhotoImage(file="images/seeResults2.png")

        button = tk.Label(self, image=btn_static, bg=BG_COLOUR)
        button.image = btn_static
        button.pack(pady="100")

        button.bind("<Button-1>", lambda e: self.load_option(root, button))
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def load_option(self, root: "App", button: tk.Label) -> None:
        """Retrieve and load in the movie the user has selected as their favourite"""
        button.destroy()
        subheading = tk.Label(
            self,
            text="Pick the movie you're talking about...",
            font=("Futura-Bold", 40),
            bg=BG_COLOUR,
            anchor="w",
            fg=PINK,
            height=2,
        )
        subheading.pack()

        image_file = Image.open(f"./images/{root.chosen_movie}.jpg")

        img_static_file = image_file.resize((800, 450))
        img_hover_file = image_file.resize((795, 447))

        static_img = ImageTk.PhotoImage(img_static_file)
        hover_img = ImageTk.PhotoImage(img_hover_file)

        result_display = tk.Label(
            self,
            text=root.chosen_movie,
            image=static_img,
            font=("Futura-Bold", 20),
            anchor="w",
            bg=BG_COLOUR,
            fg=LIGHT_BLUE,
            compound="top",
        )
        result_display.image = static_img
        result_display.pack()

        result_display.bind(
            "<Button-1>", lambda e: root.switch_frame("RecommendationsPage")
        )
        result_display.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(result_display, hover_img, static_img, True),
        )
        result_display.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(result_display, hover_img, static_img, False),
        )


class RecommendationsPage(tk.Frame):
    """Recommendations page

    This frame will begin the process of computing the recommendations followed by loading and
    displaying the GUI components (i.e. the images and descriptions of each recommendation)
    """
    def __init__(self, container: tk.Frame, root: "App") -> None:
        """Initializes the RecommendationsPage and it's initial GUI components (i.e. the
        title and the button that will begin the computation process).
        """
        super().__init__(container, bg=BG_COLOUR)

        title = tk.Label(
            self,
            text="Our Recommendations",
            font=("Futura-Bold", 75),
            bg=BG_COLOUR,
            anchor="w",
            fg=LIGHT_PURPLE,
        )
        title.pack()

        # A button so that the user dictates when the computation process begins
        btn_static = tk.PhotoImage(file="images/compute1.png")
        btn_hover = tk.PhotoImage(file="images/compute2.png")

        button = tk.Label(self, image=btn_static, bg=BG_COLOUR)
        button.image = btn_static
        button.pack(pady="100")

        button.bind(
            "<Button-1>", lambda e: self.calculate_recommendations(root, button)
        )  # When the button is pressed the computation process can begin
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def calculate_recommendations(self, root: "App", button: tk.Label) -> None:
        """Begin the process of computing recommendations based on the user's preference"""
        # Destroying the button to prevent the user from repeatedly beginning
        # the computation process
        button.destroy()

        users_and_reviews = root.event_loop.run_until_complete(
            scraper.viewers_and_reviews_from_movie(
                root.chosen_movie, root.scraper, viewer_count=10
            )
        )

        # Computing recommendations
        review_graph = ReviewGraph()
        for user, reviews in users_and_reviews.items():
            review_graph.insert_user_and_watched_movies(user, reviews)

        recommendation_list_long = review_graph.get_recommendation_list(root.chosen_movie)

        # Shortening the list to the top 5 and storing it in the global recommendations list
        root.recommendations = recommendation_list_long[1:6]

        # Getting extra information/details about the recommendations
        extra_info = root.event_loop.run_until_complete(
            get_movie_extra_info(root.recommendations, root.scraper)
        )

        # Loading images for recommendations
        for recommendation in root.recommendations:
            root.event_loop.run_until_complete(
                load_movie_image(recommendation, root.scraper)
            )

        # When computations are complete the button to see results shows up
        btn_static = tk.PhotoImage(file="images/seeResults1.png")
        btn_hover = tk.PhotoImage(file="images/seeResults2.png")

        button = tk.Label(self, image=btn_static, bg=BG_COLOUR)
        button.image = btn_static
        button.pack(pady="100")

        button.bind("<Button-1>", lambda e: self.load_options(root, button, extra_info))
        button.bind(
            "<Enter>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, True),
        )
        button.bind(
            "<Leave>",
            lambda e: root.switch_btn_hover(button, btn_hover, btn_static, False),
        )

    def load_options(self, root: "App", button: tk.Label, info: list[dict]) -> None:
        """Load and display the recommendations we have found based on user's favourite movie """
        button.destroy()
        subheading = tk.Label(
            self,
            text=f"Because you liked {root.chosen_movie}...",
            font=("Futura-Bold", 40),
            bg=BG_COLOUR,
            anchor="w",
            fg=PINK,
            height=2,
        )
        subheading.pack()

        # Iteratively generates the display for each recommendation
        for i in range(len(info)):
            movie_text = info[i]['movie_name'].upper().replace("-", " ")
            director_text = "Directed by " + info[i]["director"]
            genres_text = "Genres: " + str(info[i]["genres"])[1:-1].replace("'", "")
            description_txt = movie_text + "\n" + director_text + "\n" + genres_text

            image_file = Image.open(f"./images/{info[i]['movie_name']}.jpg")
            image_file = image_file.resize((600, 337))
            img = ImageTk.PhotoImage(image_file)

            result_display = tk.Label(
                self,
                text=description_txt,
                image=img,
                font=("Futura-Bold", 20),
                anchor="w",
                bg=BG_COLOUR,
                fg=LIGHT_BLUE,
                compound="top",
            )
            result_display.image = img
            result_display.pack(pady=2)
