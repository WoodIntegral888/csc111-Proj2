from __future__ import annotations
from dataclasses import dataclass
from math import log2


class _Vertex:
    """A vertex in a ReviewGraph, used to represent a user or a book.

    Each vertex item is either the name of a user or movie.

    Instance Attributes:
        - item: The user or movie stored in this vertex
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - self.kind in {'user', 'movie'}
        - all(self in u.neighbours for u in self.neighbours)
    """

    item: str
    kind: str
    neighbours: dict[_Vertex, int]

    def __init__(self, item: str, kind: str) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'movie'}
        """

        self.item = item
        self.kind = kind
        self.neighbours = {}


class ReviewGraph:
    """A weighted graph used to represent a network of movie reviews.

    Private Instance Attributes:
        - _vertices: A collection of the vertices contained in this graph.
        Maps user names or movie names to _Vertex objects.
    """

    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: str, kind: str) -> None:
        """Add a vertex to the given graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """

        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: str, item2: str, rating: int) -> None:
        """Add an edge between two vertices with weighted edge weight

        If item1 and item2 are not in the graph then we raise a ValueError

        Preconditions:
            - weight in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        """

        if item1 in self._vertices and item2 in self._vertices:
            vertex_1 = self._vertices[item1]
            vertex_2 = self._vertices[item2]

            vertex_1.neighbours[vertex_2] = rating
            vertex_2.neighbours[vertex_1] = rating
        else:
            raise ValueError

    def get_neighbours(self, item: str) -> set[str]:
        """Return a set of the neighbours names and for the given item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            vertex = self._vertices[item]
            return {neighbour.item for neighbour in vertex.neighbours}
        else:
            raise ValueError

    def get_shared_neighbours(self, item1: str, item2: str) -> set[str]:
        """"""
        if item1 in self._vertices and item2 in self._vertices:
            item1_neighbours = self.get_neighbours(item1)
            item2_neighbours = self.get_neighbours(item2)

            return item1_neighbours.intersection(item2_neighbours)
        else:
            return set()

    def get_weight(self, item1: str, item2: str) -> int:
        if item1 in self._vertices and item2 in self._vertices:
            vertex_1 = self._vertices[item1]
            vertex_2 = self._vertices[item2]

            if item2 in self.get_neighbours(item1):
                return vertex_1.neighbours[vertex_2]
            else:
                raise ValueError
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = None) -> set:
        """Return a set of all vertex names in this graph.

        Preconditions:
            - kind in {None, 'user', 'book'}
        """
        if kind:
            return {
                vertex.item for vertex in self._vertices.values() if vertex.kind == kind
            }
        else:
            return set(self._vertices.keys())

    def insert_user_and_watched_movies(
        self, username: str, movies_watched: dict[str, int]
    ) -> None:
        """Add a the user vertex, the movie vertices and the corresponding edges.

        Do nothing if the given user is already in this graph.
        """

        if username not in self._vertices:
            self.add_vertex(username, kind="user")
            for movie_name, rating in movies_watched.items():
                self.add_vertex(movie_name, kind="movie")
                self.add_edge(username, movie_name, rating)
        else:
            return

    def get_similarity_score(self, item1: str, item2: str) -> float:
        """Return a decimal number from 0.0-10.0 representing how similar the reviews are, higher better.

        Returns the average diffrence in rating for shared_neighbours.
        If there are no common neighbours then 0.0 is returned.

        Preconditions:
            - item1 is in self
            - item2 is in self
            - item1 and item2 share at least one neighbour
        """

        shared_neighbours = self.get_shared_neighbours(item1, item2)

        if shared_neighbours == {}:
            return 0.0

        total = 0.0
        for neighbour in shared_neighbours:
            rating_1 = self.get_weight(neighbour, item1)
            rating_2 = self.get_weight(neighbour, item2)
            total += abs(rating_1 - rating_2)

        return 10.0 - (total / len(shared_neighbours))

    def get_recommendation_score(self, item1: str, item2: str) -> float:
        """Return a decimal number representing how much we recommend the item2 if they've seen item1.

        Returns the average diffrence in rating for shared_neighbours times log_2 of the number of shared reviews.
        If there are no shared reviews then the recommendation score returned is 0.0.

        Preconditions:
            - item1 is in self
            - item2 is in self
            - item1 and item2 share at least one neighbour
        """

        shared_neighbours = self.get_shared_neighbours(item1, item2)

        if len(shared_neighbours) == 0:
            return 0.0

        return log2(len(shared_neighbours)) * self.get_similarity_score(item1, item2)

    def get_recommendation_list(self, movie_name: str):
        """TODO"""

        movie_list = []
        for other_movie in self.get_all_vertices("movie"):
            score = self.get_recommendation_score(movie_name, other_movie)
            movie_list += [(score, other_movie)]

        movie_list.sort(reverse=True)

        return [name for (_, name) in movie_list]
