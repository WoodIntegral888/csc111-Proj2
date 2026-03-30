from app import App

app = App()
app.mainloop()


# import asyncio
# from curl_cffi import requests

# from scraper import viewers_and_reviews_from_movie
# from review_graph import ReviewGraph

# session = requests.AsyncSession(impersonate="chrome")

# data = asyncio.run(
#     viewers_and_reviews_from_movie("dune-2021", session, viewer_count=10)
# )

# import pprint


# review_graph = ReviewGraph()
# for user, reviews in data.items():
#     review_graph.insert_user_and_watched_movies(user, reviews)

# rec_list = review_graph.get_recommendation_list("dune-2021")

# pprint.pprint(rec_list)


# # from review_graph import ReviewGraph


# # review_graph = ReviewGraph()

# # review_graph.insert_user_and_watched_movies("Joshua", {"whiplash": 10, "dune": 9})
# # review_graph.insert_user_and_watched_movies("Jacob", {"whiplash": 7, "dune": 10})

# # n = review_graph.get_shared_neighbours("whiplash", "dune")

# # print(n)
