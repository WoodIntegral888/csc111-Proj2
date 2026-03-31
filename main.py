from app import App


if __name__ == '__main__':
    app = App()
    app.mainloop()

# import asyncio
# from curl_cffi import requests

# from scraper import get_movie_extra_info

# session = requests.AsyncSession(impersonate="chrome")

# data = asyncio.run(get_movie_extra_info(["dune-2021", "project-hail-mary"], session))

# import pprint

# pprint.pprint(data)


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
