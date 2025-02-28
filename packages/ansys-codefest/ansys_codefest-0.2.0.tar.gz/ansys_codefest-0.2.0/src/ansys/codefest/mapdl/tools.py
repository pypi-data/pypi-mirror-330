import pathlib
from dataclasses import dataclass
from importlib.resources import files
from importlib.abc import Traversable
from typing import Union
import json

from ansys.mapdl.core.launcher import MAPDL_DEFAULT_PORT, LOCALHOST

from . import story
from . import chambers
from .constants import Submission, BeamXn, StoryType


class ChallengeError(Exception):
    """Exception raised when an error is encountered in the creation or
    use of a Challenge object."""

    pass


@dataclass
class Challenge:
    """Instance of a challenge.

    Stores the geometry file path and the equivalent suggestion & story paths,
    IF they exist. A suggestion does not need to exist and can be None. If no
    story is given,
    """

    _geometry_filename: Union[pathlib.Path, Traversable]
    _story_filename: Union[pathlib.Path, Traversable]
    _suggestion_filename: Union[pathlib.Path, Traversable] = None

    def __repr__(self):
        return (
            f"Challenge({self._geometry_filename},"
            f" suggestion={self.has_suggestion})"
        )

    @classmethod
    def create_example(cls, number: str, story_type: StoryType = StoryType.CONCISE):
        """Create a Challenge instance from a built-in an example.

        Args:
            number: aka ID. This will be something like `'8'` or `'1a'`
            story_type: what sort of instructions should be added to the
                        challenge

        Returns:
            The new challenge instance
        """
        geometry = files(chambers).joinpath(f"geometry_{number}.json")
        suggestion = files(chambers).joinpath(f"suggestion_{number}.json")
        story_file = cls.choose_story_type(story_type)
        if not suggestion.is_file():
            suggestion = None
        return cls(geometry, story_file, suggestion)

    @staticmethod
    def choose_story_type(story_type):
        """Get the correct story file based on the chosen type.

        Args:
            story_type: enum of which story type you have chosen

        Returns:
            file path to the chosen story
        """
        if story_type == StoryType.CONCISE:
            story_file = files(story).joinpath("concise.txt")
        elif story_type == StoryType.MINIMAL:
            story_file = files(story).joinpath("minimal.txt")
        elif story_type == StoryType.VERBOSE:
            story_file = files(story).joinpath("verbose.txt")
        else:
            raise TypeError(f"Invalid StoryType option supplied {story_type}")
        return story_file

    @classmethod
    def create_challenge(
        cls,
        path_to_level: pathlib.Path,
        path_to_suggestion: pathlib.Path = None,
        story_type: StoryType = StoryType.CONCISE,
    ):
        """Create a Challenge instance from scratch.

        Args:
            path_to_level: path to where the level file should go
            path_to_suggestion: path to where the suggestion file should go
            story_type: what sort of instructions should be added to the
                        challenge

        Returns:
            The new challenge instance
        """
        story_file = cls.choose_story_type(story_type)
        return cls(path_to_level, story_file, path_to_suggestion)

    @staticmethod
    def get_available_example_ids() -> list[str]:
        """Return all available example IDs as a list.

        Returns:
            list of IDs as strings.
        """
        return [
            d.name.replace("geometry_", "").replace(".json", "")
            for d in files(chambers).iterdir()
            if "geometry_" in d.name
        ]

    @staticmethod
    def get_available_suggestion_ids():
        """Get available example IDs which also have associated suggestions.

        Returns:
            list of IDs as strings.
        """
        return [
            d.name.replace("suggestion_", "").replace(".json", "")
            for d in files(chambers).iterdir()
            if "suggestion" in d.name
        ]

    @property
    def is_available(self) -> bool:
        """Does the geometry file path point to a file?

        Returns:
            If the geometry file path points to a file.

        """
        return self.geometry_filename.is_file()

    @property
    def geometry_filename(self) -> Union[pathlib.Path, Traversable]:
        """The geometry file path.

                Returns:
        `           the location of the geometry file as a pathlib Path
        """
        return self._geometry_filename

    @property
    def suggestion_filename(self) -> Union[pathlib.Path, Traversable]:
        """The suggestion file path.

        Returns:
            the location of the suggestion json file as a pathlib Path
        """
        return self._suggestion_filename

    @property
    def story_filename(self) -> Union[pathlib.Path, Traversable]:
        """The file path to the story file.

        Returns:
            the location of the story file as a pathlib Path
        """
        return self._story_filename

    @property
    def has_suggestion(self) -> bool:
        """True if this challenge has an available suggestion.

        Returns:
            True/False depending on the presence of an available suggestion.
        """
        if self.suggestion_filename is None:
            return False
        return self.suggestion_filename.is_file()

    def get_suggestion(self) -> Submission:
        """Get suggested design dictionary (if available)

        Returns:
            suggested design dictionary
        """
        if self.has_suggestion:
            submission = json.loads(self.suggestion_filename.read_text())
            if "cross_section" in submission:
                submission["cross_section"] = [
                    BeamXn(xn) for xn in submission["cross_section"]
                ]
            return submission
        else:
            raise ChallengeError("No suggestion available for this challenge.")

    def get_fixed_nodes(self) -> list[list[int]]:
        """Get list of fixed nodes for this example

        Returns:
            list of fixed nodes as [number, x, y]
        """
        level = json.loads(self.geometry_filename.read_text())
        grid_size = level["grid_size"]
        n1, n2 = level["entry/exit"]
        node1 = [1, *n1]
        node2 = [2, *n2]
        nodes = [node1, node2]
        start_rock = (grid_size**2) + 1
        for i, coord in enumerate(level["chamber"]["fixed nodes"]):
            n = [i + start_rock, *coord]
            nodes.append(n)
        return nodes

    def get_text(self) -> str:
        """Get contents of story file as a string without the problem.

        Returns:
            string of this challenge's story file
        """
        text = self.story_filename.read_text()
        return text


@dataclass
class Server:
    """Dataclass storing server information for a remote MAPDL connection.

    Args:
        ip: ip address of the server as a string, defaults to LOCALHOST,
            usually 127.0.0.1
        port: port of the server as a string, defaults to MAPDL_DEFAULT_PORT,
              usually "50052".
    """

    ip: str = LOCALHOST
    port: str = MAPDL_DEFAULT_PORT
