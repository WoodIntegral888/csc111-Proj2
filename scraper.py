import asyncio
from bs4 import BeautifulSoup
from curl_cffi import AsyncSession

LETTER_BOXD = "https://letterboxd.com"


async def load_movie_image(movie_name: str, scraper: AsyncSession) -> None:
    """Save the Letterboxd backdrop image of movie_name into the images folder

    Preconditions:
        - movie_name is a vaild movie on letterboxd
        - The images folder exists
    """

    response = await scraper.get(f"{LETTER_BOXD}/film/{movie_name}/")

    soup = BeautifulSoup(response.text, "html.parser")

    image_link = soup.find("meta", property="og:image").get("content")
    image_content = (await scraper.get(image_link)).content

    with open(f"./images/{movie_name}.jpg", "wb") as movie_image_file:
        movie_image_file.write(image_content)


async def get_movies_watched(
    username: str, scraper: AsyncSession, max_review_count=100
) -> dict[str, int]:
    """Return a dictionary of movie names and ratings from username

    The keys of the dictionary are the names of the movies watched from username
    and the values of the dictionary are the ratings of the movies.

    Preconditions:
        - username is a vaild username on letterboxd
    """

    print(username)

    reviews = {}

    movie_reviewers_link = f"/{username}/reviews/"

    while True:
        response = await scraper.get(f"{LETTER_BOXD}/{movie_reviewers_link}")

        soup = BeautifulSoup(response.text, "html.parser")
        for review in soup.select("article.production-viewing"):
            primaryname_element = review.select_one("h2.primaryname a")

            # Some people have rewatched the same movie serveral times
            # Formatted as movie_name/review_number, hence the final split
            name = (
                primaryname_element.get("href")
                .removeprefix(f"/{username}/film/")
                .strip("/")
                .split("/")[0]
            )

            if not review.select_one("svg.-rating"):
                continue
            stars = review.select_one("svg.-rating").get("aria-label")
            rating = 2 * stars.count("★") + stars.count("½")

            reviews[name] = rating

        if len(reviews) >= max_review_count:
            break
        elif soup.select_one("a.next"):
            movie_reviewers_link = soup.select_one("a.next").get("href")
        else:
            break

    return reviews


async def get_movie_viewers(
    movie_name: str, scraper: AsyncSession, max_user_count=100
) -> set[str]:
    """Return a set of usernames who have reviewed movie_name

    Once max_user_count number of users is met, no more pages are loaded.

    Preconditions:
        - movie_name is a vaild movie on letterboxd
    """

    usernames = set()

    movie_reviewers_link = f"/film/{movie_name}/reviews/by/added-earliest"

    while True:
        response = await scraper.get(f"{LETTER_BOXD}{movie_reviewers_link}")

        soup = BeautifulSoup(response.text, "html.parser")
        for review in soup.select("article.production-viewing"):
            avatar = review.select_one("a.avatar")
            username = avatar.get("href")
            usernames.add(username.strip("/"))

        if len(usernames) >= max_user_count:
            break
        elif soup.select_one("a.next"):
            movie_reviewers_link = soup.select_one("a.next").get("href")
        else:
            break

    return usernames


async def viewers_and_reviews_from_movie(
    movie_name: str, scraper: AsyncSession, viewer_count=100
) -> dict[str, dict[str, int]]:
    """Return a dictionary of of users and their reviews of movies.

    Once max_user_count number of users is met, no more pages are loaded.

    Preconditions:
        - movie_name is a vaild movie on letterboxd
    """

    viewers = list(await get_movie_viewers(movie_name, scraper, viewer_count))

    review_list = await asyncio.gather(
        *[get_movies_watched(viewer, scraper) for viewer in viewers]
    )

    reviews = {}

    for i in range(len(viewers)):
        reviews[viewers[i]] = review_list[i]

    return reviews


async def get_movie_extra_info(
    movie_names: list[str], scraper: AsyncSession
) -> list[dict]:
    """Return a dictionary containing the director of movie_name and the genres movie_name belongs to

    Preconditions:
        - movie_name is a vaild movie on letterboxd
    """

    responses = await asyncio.gather(
        *[
            scraper.get(f"{LETTER_BOXD}/film/{movie_name}/genres/")
            for movie_name in movie_names
        ]
    )

    extra_info_list = []

    for response, movie_name in zip(responses, movie_names):
        soup = BeautifulSoup(response.text, "html.parser")

        genres = set()
        themes = soup.select_one("div.text-sluglist.capitalize")
        for theme in themes.select("a"):
            genres.add(theme.text)

        director = soup.select_one("p.credits a.contributor").text

        extra_info_list.append(
            {"movie_name": movie_name, "genres": genres, "director": director}
        )

    return extra_info_list


async def is_vaild_movie(movie_name: str, scraper: AsyncSession) -> bool:

    response = await scraper.get(f"{LETTER_BOXD}/film/{movie_name}/")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").text

    return title != "Letterboxd - Not Found"
