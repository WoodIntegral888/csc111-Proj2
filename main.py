# from app import App

# app = App()
# app.mainloop()

from curl_cffi import requests
from scraper import load_movie_image

session = requests.Session(impersonate="chrome")

load_movie_image("whiplash-2014", session)
