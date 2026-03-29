from app import App

app = App()
app.mainloop()


# import asyncio
# from curl_cffi import requests

# from scraper import viewers_and_reviews_from_movie

# session = requests.AsyncSession(impersonate="chrome")

# data = asyncio.run(
#     viewers_and_reviews_from_movie("friday-the-13th", session, viewer_count=10)
# )

# import pprint

# pprint.pprint(data)
