import json
import pathlib
from importlib.resources import files
from importlib.abc import Traversable
from dataclasses import dataclass
from typing import Union, TypedDict
from .. import chambers

ChamberFixedNodes = TypedDict("ChamberFixedNodes", {"fixed nodes": list[list[int]]})
ChamberDict = TypedDict(
    "ChamberDict",
    {
        "grid_size": int,
        "entry/exit": list[list[int]],
        "chamber": ChamberFixedNodes,
    },
)


@dataclass
class TroubleMaker:
    """This class can be used to create problems for use with the main package.

    This class has two key properties: paths (as `pathlib.Path`s)
    to the equivalent ascii art representation of the problem (as a .txt file)
    and to the json version that is understood by the package (.json).

    The methods on this class can translate between the two formats and
    generate blank versions as well. In addition, it allows the use of an
    existing design as a template which can be edited without losing the
    original.
    """

    ascii_file: Union[pathlib.Path, Traversable] = None
    json_file: Union[pathlib.Path, Traversable] = None

    @classmethod
    def new_blank_problem(
        cls,
        grid_size: int = 23,
        destination_directory: pathlib.Path = pathlib.Path("/"),
    ):
        """Create blank design template files for a custom problem.

        Args:
            grid_size: The size of the grid, must be an odd number
            destination_directory: directory to save ascii new files in

        Returns:
            None
        """
        new = cls(
            ascii_file=cls.new_blank_ascii(grid_size, destination_directory / "new.txt")
        )
        new.ascii_to_json()
        return new

    @staticmethod
    def new_blank_ascii(
        grid_size: int = 23,
        destination_path: pathlib.Path = pathlib.Path("./new.txt"),
    ):
        """Create a blank design template for a custom problem.

        Args:
            grid_size: The size of the grid, must be an odd number
            destination_path: file to save ascii design to

        Returns:
            destination_path: path to the created file
        """
        TroubleMaker._check_grid_size(grid_size)
        mid = (grid_size - 1) // 2
        base = {
            "grid_size": grid_size,
            "entry/exit": [[-mid, mid], [mid, mid]],
            "chamber": {"fixed nodes": []},
        }
        string = TroubleMaker.dict_to_string(base)
        with open(destination_path) as f:
            f.write(string)
        return destination_path

    @staticmethod
    def _check_grid_size(grid_size):
        if grid_size % 2 != 0 or grid_size <= 2 or not isinstance(grid_size, int):
            raise ValueError(
                f"grid_size must be an odd, "
                f"positive "
                f'integer greater than 2 and not "{grid_size}"'
            )

    @staticmethod
    def new_blank_json(
        grid_size: int = 23,
        destination_path: pathlib.Path = pathlib.Path("./new.json"),
    ):
        """Create a blank design template json for a custom problem.

        Args:
            grid_size: The size of the grid, must be an odd number
            destination_path: file to save ascii design to

        Returns:
            destination_path: path to the created file
        """
        TroubleMaker._check_grid_size(grid_size)
        mid = (grid_size - 1) // 2
        base = {
            "grid_size": grid_size,
            "entry/exit": [[-mid, mid], [mid, mid]],
            "chamber": {"fixed nodes": []},
        }
        with open(destination_path) as f:
            json.dump(base, f)
        return destination_path

    @classmethod
    def from_builtin(
        cls,
        id_: str,
        ascii_destination: pathlib.Path,
        json_destination: pathlib.Path = None,
    ):
        """Construct a problem from a built-in problem.

        Args:
            cls: the constructor
            id_: id of the problem to be loaded
            ascii_destination: file to save ascii design to
            json_destination: file to save json version to

        """
        geometry = files(chambers).joinpath(f"geometry_{id_}.json")
        new = cls(ascii_destination, geometry)
        new.json_to_ascii(ascii_destination)
        new.json_file = None
        new.ascii_to_json(json_destination)
        return new

    def ascii_to_json(self, destination: pathlib.Path = None) -> None:
        """Convert ascii design, in a file, to JSON format.

        Args:
            destination: file to save json to.

        Returns:
              None
        """
        assert self.ascii_file is not None, (
            "An ASCII problem design file "
            "must be supplied in order to "
            "call this method."
        )
        with open(self.ascii_file) as f:
            string = f.read()

        if destination is None:
            output_json_file_name = self.ascii_file.with_suffix(".json")
        else:
            output_json_file_name = destination
        output_ = self.string_to_dict(string)
        with open(output_json_file_name, "w", encoding="utf8") as f:
            json.dump(output_, f)
        self.json_file = output_json_file_name

    @staticmethod
    def string_to_dict(string: str) -> ChamberDict:
        """Convert string of chamber into chamber dictionary/

        Args:
            string: string in question

        Returns:
            None

        """
        lines = [s.strip("\n").split(" ") for s in string.split("\n")]
        num_lines = len(lines)
        max_num_lines = num_lines - 1
        x0, y0 = (num_lines - 1) // 2, (num_lines - 1) // 2
        fixed_nodes = []
        start, end = None, None
        for j, row in enumerate(lines):
            for i, cell in enumerate(row):
                coord = [i - x0, max_num_lines - j - y0]
                if cell == "o":
                    fixed_nodes.append(coord)
                elif cell == "1":
                    start = coord
                elif cell == "2":
                    end = coord
                else:
                    pass
        assert start and end, (
            "Something went wrong, start and end nodes "
            "were not found in the ascii input."
        )
        output_ = {
            "grid_size": num_lines,
            "entry/exit": [start, end],
            "chamber": {"fixed nodes": fixed_nodes},
        }
        return output_

    def json_to_ascii(self, destination: pathlib.Path = None):
        assert self.json_file is not None, (
            "A JSON problem design file "
            "must be supplied in order to "
            "call this method."
        )
        with open(self.json_file) as f:
            data = json.load(f)
        output_ = self.dict_to_string(data)
        if destination is None:
            output_ascii_file_name = self.json_file.with_suffix(".txt")
        else:
            output_ascii_file_name = destination
        with open(output_ascii_file_name, "w", encoding="utf8") as f:
            f.write(output_)
        self.ascii_file = output_ascii_file_name

    @staticmethod
    def dict_to_string(data: ChamberDict) -> str:
        """Convert dict of chamber into string.

        Args:
            data: dictionary to be converted.

        Returns:
            None

        """
        grid_size = data["grid_size"]
        chamber = [["·" for _ in range(grid_size)] for __ in range(grid_size)]
        entry, exit_ = data["entry/exit"]
        offset = (grid_size - 1) // 2
        chamber[entry[0] + offset][entry[1] + offset] = "1"
        chamber[exit_[0] + offset][exit_[1] + offset] = "2"
        for node in data["chamber"]["fixed nodes"]:
            chamber[node[0] + offset][node[1] + offset] = "o"
        chamber = list(zip(*chamber[::-1]))
        output_ = "\n".join([" ".join(row[::-1]) for row in chamber[::-1]])
        return output_
