"""
Python package designed to facilitate the Ansys Codefest mapdl structured
challenges.

To tackle the challenges in the Codefest run the `Start` function and
store the objects that are returned. Each is a `challenge` which can be
tackled.

Examples:
```python-repl
    >>> import ansys.codefest.mapdl as acf
    >>> buildy = acf.Start.builtin_challenge('1a')
```

##### Accessing Sandbox Tools

In addition to the bridge-builder challenge, this library
contains sandbox tools which are used "behind the scenes"; the challenge is
built on these tools.

You can import these alongside the main codefest tools, but using them is not
recommended unless you know what you're doing.

These tools can be used to construct your own bridge-based simulations without
the restrictions in place in the main challenge.

##### `Submission` type

The `Submission` type is used in several places in the docstrings.
This corresponds to the following type:

```python
    Submission = TypedDict('Submission',
                           {'nodes': list[int], 'beams': list[list[int]],
                            'load_path': list[int], 'cross_section': list[int],
                            'dimensions': list[list[float]],
                            'materials': list[int]})
```
"""

import copy
import json
import pathlib
from dataclasses import dataclass
from importlib.resources import files
from math import cos, sin, pi
from string import Template

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colorbar import Colorbar
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .mechanics import (
    Beam,
    Simulation,
    Blueprint,
    BlueprintConstructionException,
)
from . import chambers, story
from .constants import Submission, StoryType
from .tools import Challenge, ChallengeError, Server
from .setup import TroubleMaker


class Start:
    """Collection of codefest-starting methods.

    Loading built in challenges requires a level id_, but it is also
    possible to use custom challenges as well, provided they are in
    the correct format.

    Make sure you are tackling the correct challenge!

    You can easily check which ids are available by calling
    `acf.Challenge.get_available_example_ids()` to get them as a list
    of strings.

    or you can create your own challenge/load an external one.

    Examples:
    ```python-repl
        >>> import ansys.codefest.mapdl as acf
        >>> builder = acf.Start.builtin_challenge(id_='1a')
        >>> builder = acf.Start.load_challenge(your_geometry_filepath,
                                               suggestion_file=your_corresponding_suggestion_filepath)
    ```

    """

    @staticmethod
    def builtin_challenge(
        id_: str,
        story_type: StoryType = StoryType.CONCISE,
        mapdl_loc: pathlib.Path = None,
        server: Server = None,
    ) -> "BuildyMcBuildFace":
        """Begin a builtin challenge, using a given id.

        You can also specify the story type. The concise version is the default
        but a minimalist and verbose version are both available as well.

        Args:
            id_: ID of challenge to be loaded, e.g. '1' or '11a' etc.
            story_type: enum, acf.StoryType
            mapdl_loc: path to alternative mapdl executable
            server: Optional Server object containing connection details.
                If present a remote connection will be attempted.

        Returns:
            BuildyMcBuildFace
        """
        return BuildyMcBuildFace._load_challenge(
            Challenge.create_example(id_, story_type),
            mapdl_loc=mapdl_loc,
            server=server,
        )

    @staticmethod
    def load_challenge(
        geometry_file: pathlib.Path,
        story_type: StoryType = StoryType.CONCISE,
        suggestion_file: pathlib.Path = None,
        mapdl_loc: pathlib.Path = None,
        server: Server = None,
    ) -> "BuildyMcBuildFace":
        """Load an external or custom challenge.

        If you have a corresponding suggestion dictionary it must be
        included here.

        You can also specify the story type. The concise version is the default
        but a minimalist and verbose version are both available as well.

        Args:
            geometry_file: path to the geometry json file
            story_type: enum acf.StoryType
            suggestion_file: path to suggestion json file
            mapdl_loc: path to alternative mapdl executable
            server: Optional Server object containing connection details.
                If present a remote connection will be attempted.

        Returns:
            BuildyMcBuildFace

        """
        return BuildyMcBuildFace._load_challenge(
            Challenge.create_challenge(geometry_file, suggestion_file, story_type),
            mapdl_loc=mapdl_loc,
            server=server,
        )


@dataclass
class Bridge:
    """Bridge class returned after a simulation has been executed.

    Possesses a few simple post-processing methods for simulations.
    """

    simulation: Simulation
    design: Submission

    def __repr__(self):
        return (
            f"<Bridge({len(self.simulation.nodes)} nodes, "
            f"{len(self.simulation.beams)} beams)>"
        )

    def _display_feedback(self, string: str):
        preamble = f'{" ": ^50}\n{"RESULTS":=^50}\n{" ": ^50}\n\n'
        string = preamble + string
        print(string)

    def assess_for_breaks(self, display: bool = False) -> tuple[bool, str, list[Beam]]:
        """Assess which beams have broken, if any, and return a report.

        Returns a bool to say if the bridge was successful or not, as well
        as the feedback as a string and a list of beam objects containing the
        stresses of each beam.


        Args:
            display: defaults to False

        Returns:
            tuple of the success, details by beam (as a string), and a list of
            Beam objects
        """
        it_broke, feedback = self.simulation.assess_for_breaks()
        if display:
            self._display_feedback(feedback)
        if it_broke:
            success = False
            if display:
                print(f'{"YOU DIED":-^50}')
        else:
            success = True
        return success, feedback, self.simulation.beams

    def plot(self) -> tuple[plt.Figure, plt.Axes, Colorbar]:
        """Plot the simulation's stresses and return the figure, axes,
         and colorbar objects.

        Returns:
            the figure, axes and colorbar of the plot, respectively
        """
        f, a, c = self.simulation.plot_result()
        return f, a, c


@dataclass
class BuildyMcBuildFace:
    """Instance of the bridge-building machine: BuildyMcBuildFace.

    You can submit attempts and look at the challenge input via this class.
    Instances of this class should NOT be created directly, but should be
    created by one of the `Start` methods. Hence, constructor args are
    all private parameters.

    Args:
        _blueprint: the blueprint to build designs from
        _challenge: Challenge object representing what is being tackled
        _mapdl_loc: path to alternative mapdl executable
        _server: Optional Server object containing connection details.
    """

    _blueprint: Blueprint
    _challenge: Challenge
    _mapdl_loc: pathlib.Path = None
    _server: Server = None

    def __repr__(self):
        return f"<Bridge Builder: {self._challenge}>"

    @classmethod
    def _load_challenge(
        cls, challenge: Challenge, mapdl_loc: pathlib.Path = None, server: Server = None
    ) -> "BuildyMcBuildFace":
        blueprint = Blueprint._from_challenge(challenge)
        return cls(blueprint, challenge, _mapdl_loc=mapdl_loc, _server=server)

    @property
    def has_suggestion(self) -> bool:
        """Returns True if this challenge has a suggestion, otherwise, False.

        Returns:
            if the instance has a suggested design available
        """
        return self._challenge.has_suggestion

    def suggest_a_design(self) -> Submission:
        """Return a working design that solves the problem if one is available.

        If a design is not available, then an empty dictionary is returned and
        a warning raised.

        Notes:
            This design will work, but it will not be optimal and may be
            extremely inefficient and/or costly. It is meant as an example
            and a starting point.

        Returns:
            the suggested design, if it is available
        """
        if self.has_suggestion:
            return self._challenge.get_suggestion()
        else:
            raise ChallengeError(
                "BuildyMcBuildFace has no " "suggestions for this chamber"
            )

    def get_fixed_nodes(self) -> list[list[int]]:
        """Get a list of the fixed nodes (rocks + start + end).

        Returns a list of all rock nodes as well as the start and end nodes.
        A "node" in this list is a list of 3 integers:

        `[node_number, x_coord, y_coord]`


        Notes:
            Rock node numbers start at N + 1, where N is the id_ of nodes
            on the problem square. E.g. if your problem square is 23 x 23,
            then N = 23^2 N = 529, so the first rock node id_ will be 530,
            the second 531, and so on.

            The Start and End nodes are ALWAYS numbered 1 and 2, respectively.

        Returns:
            A list of the fixed nodes ordered [number, x, y]
        """
        return self._challenge.get_fixed_nodes()

    def display_problem(self) -> None:
        """Print the summary text of the challenge.

        Returns:
            None
        """
        text = self._challenge.get_text()
        template = Template(text)
        xlims, ylims = self._blueprint.grid_lims
        xlim = max(abs(xlims[0]), abs(xlims[1]))
        ylim = max(abs(ylims[0]), abs(ylims[1]))
        text = template.substitute(
            {
                "ascii_chamber_drawing": self._render_level_as_ascii(),
                "xmin": -xlim,
                "xmax": xlim,
                "ymin": -ylim,
                "ymax": ylim,
            }
        )
        print(text)

    def _render_level_as_ascii(self, number_of_spaces: int = 2) -> str:
        """Return a string rendering of the chamber in ascii art.

        This is a visualisation method and returns an ascii representation
        of the current chamber, like the following

        ```
        · · · · · · · · · · ·
        · · · · · · · · · · ·
        · · · · · · · · · · 2
        1 · · · · · · · · · ·
        o · · · · · · · · · o
        o · · · · · · · · · o
        o · · · · · · · · · o
        · · · · · · · o · o o
        · · · · · · o o o o o
        · · · · · o o o o o o
        · · · · o o o o o o o

        · - empty grid spaces
        o - rocks
        1 - entrance
        2 - exit
        ```
        Args:
            number_of_spaces: the number of spaces between each character

        Returns:
            the string representation of the problem
        """
        data = files(chambers).joinpath(self._challenge.geometry_filename)
        level = json.loads(data.read_text())
        string = TroubleMaker.dict_to_string(level)
        return string.replace(" ", " " * number_of_spaces)

    def build_bridge(self, design: Submission, mapdl_version: int = None) -> Bridge:
        """Construct bridge from a design.

        Depending on the design this step may take time. The method does
        three things in this order:

            1. Validate the design can be used to create a simulation

            2. Create a simulation blueprint from the design

            3. Create a simulation from the blueprint and execute it

            4. Create a Bridge object with the simulation and return it

        Steps 1 and 2 are typically very fast, but 3 can take significantly
        longer depending on the complexity of your design.

        If your submission does not pass the validation
        step, it does not count as an attempt. Include plot=True
        as an arg if you'd like matplotlib to plot the result as well.

        Materials can optionally be included in the design as a list of IDs
        (integers) that correspond to the list of beams.
        See all the materials available (and their IDs) by accessing the
        `acf.MATERIALS` dict.

        Args:
            design: the design you wish to build from
            mapdl_version: mapdl version to use (when multiple available
            and not remote)

        Returns:
            instantiated Bridge object, which can be used to gather results

        Examples:

            In the following examples we step through the whole simulation loop
            from start to finish. In Example 2 we connect to a server instead
            of a local connection.

        ```python
            # Example 1
            import ansys.codefest.mapdl as acf
            example = acf.Start.builtin_challenge('1a')
            design = example.suggest_a_design()
            bridge = example.build_bridge(design, mapdl_version=231)
            success, feedback, beams = bridge.assess_for_breaks()
            print(feedback)  # should print feedback as a string if no success

            # Example 2
            import ansys.codefest.mapdl as acf
            example = acf.Start.builtin_challenge('1a',
                                                  server=acf.Server())
            design = example.suggest_a_design()
            bridge = example.build_bridge(design)
            success, feedback, beams = bridge.assess_for_breaks()
        ```
        """
        blueprint_for_sim = self._build_design_blueprint(design)
        simulation = Simulation(
            blueprint_for_sim,
            mapdl_version=mapdl_version,
            mapdl_loc=self._mapdl_loc,
            server=self._server,
        )
        simulation.execute()
        return Bridge(simulation, design)

    def plot_design(self, design: Submission) -> tuple[plt.Figure, plt.Axes, Colorbar]:
        """Plot a bridge design using matplotlib, return fig, ax, and colorbar.

        Optionally you can include the list of beams with results to plot the
        stresses on each as well.

        Args:
            design: the design you wish to plot
            beams: list of beam objects. Must be in same order (and quantity) as those in `design`

        Returns:
            the figure, axes and colorbar of the plot

        """
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        ax.set_aspect(1)
        cmap = cm.get_cmap("tab20", 16)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("top", size="5%", pad=0.5)
        fixed_list = self.get_fixed_nodes()
        nodes = {n[0]: (n[1], n[2]) for n in design["nodes"] + fixed_list}
        constructed = {n[0] for n in design["nodes"]}
        fixed = {n[0] for n in fixed_list}
        for beam, mat in zip(design["beams"], design["materials"]):
            color = cmap((mat - 1.0) / 15.0)
            node1 = nodes[beam[0]]
            node2 = nodes[beam[1]]
            ax.plot(
                [node1[0], node2[0]],
                [node1[1], node2[1]],
                color=color,
                linewidth=8,
            )
        x_bridge_nodes = []
        y_bridge_nodes = []
        x_start_node = []
        y_start_node = []
        x_end_node = []
        y_end_node = []
        x_rocks = []
        y_rocks = []
        x_load_path = []
        y_load_path = []
        for num, coord in nodes.items():
            if num in constructed:
                x_bridge_nodes.append(coord[0])
                y_bridge_nodes.append(coord[1])
            elif num in fixed and num not in {1, 2}:
                x_rocks.append(coord[0])
                y_rocks.append(coord[1])
            elif num == 1:
                x_start_node.append(coord[0])
                y_start_node.append(coord[1])
            elif num == 2:
                x_end_node.append(coord[0])
                y_end_node.append(coord[1])
            if num in design["load_path"]:
                x_load_path.append(coord[0])
                y_load_path.append(coord[1])

        ax.plot(
            x_bridge_nodes,
            y_bridge_nodes,
            linestyle=" ",
            marker="X",
            color="w",
            label="Bridge",
            ms=3,
            mfc="None",
            mec="silver",
            mew=1,
        )
        ax.plot(
            x_start_node,
            y_start_node,
            linestyle=" ",
            marker=5,
            color="k",
            label="START",
            ms=8,
            mfc="w",
            mew=3,
        )
        ax.plot(
            x_end_node,
            y_end_node,
            linestyle=" ",
            marker=4,
            color="k",
            label="END",
            ms=8,
            mfc="w",
            mew=3,
        )
        ax.plot(
            x_rocks,
            y_rocks,
            linestyle=" ",
            marker="h",
            color="gray",
            label="Rocks",
            ms=5,
            mfc="None",
            mew=2,
        )
        ax.plot(
            x_load_path,
            y_load_path,
            marker=7,
            linestyle=" ",
            color="k",
            label="loaded nodes",
        )
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend(loc="best")
        norm = mpl.colors.Normalize(vmin=0.5, vmax=16.5)
        cb = fig.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            cax=cax,
            orientation="horizontal",
            label="Material IDs",
            ticks=[i + 1 for i in range(16)],
        )
        return fig, ax, cb

    def calculate_design_cost(self, design: Submission) -> float:
        """Calculate how much the provided design would cost

        This does not perform a simulation and the result is returned as
        a float in dollars.

        Args:
            design: design dictionary to be used for the calculation

        Returns:
            the cost of the design in dollarydoos
        """
        blueprint = self._build_design_blueprint(design)
        return blueprint.cost

    def _build_design_blueprint(self, design: Submission):
        blueprint_for_sim = copy.deepcopy(self._blueprint)
        blueprint_for_sim.with_challenge_attempt_geometry(design)
        valid, reasons = blueprint_for_sim.is_valid()
        if not valid:
            raise BlueprintConstructionException(reasons)
        return blueprint_for_sim


def rotate_coordinates(nodes: list[list[int]], rotation: float) -> list[list[int]]:
    """Rotate coordinates in the x-y plane about the origin by degrees.

    Works on nodes with any dimension greater than or equal to two.

    Args:
        nodes: list of x, y coordinates. node number NOT included.
        rotation: degrees rotation anti-clockwise from the horizontal

    Returns:
        the rotated node list
    """
    rotation = degrees_to_radians(rotation)
    rotated_nodes = []
    for node in nodes:
        x = node[0] * cos(rotation) - node[1] * sin(rotation)
        y = node[1] * cos(rotation) + node[0] * sin(rotation)
        new = [int(round(x)), int(round(y))]
        rotated_nodes.append(new)
    return rotated_nodes


def degrees_to_radians(theta: float) -> float:
    """Convert degrees to radians.

    Parameters:
        theta: angle in degrees

    Returns:
        angle in radians
    """
    return theta * pi / 180.0


def save_pymapdl_script(
    save_path: pathlib.Path = pathlib.Path("./pymapdl_bridge_simulator.py"),
) -> None:
    """Save the PyMAPDL script version of the builder to file.

    This package comes with a pre-built example PyMAPDL script that can be
    used to streamline testing using pure PyMAPDL and bypassing the codefest
    library entirely. This function lets you access it.

    In order to get this script to work you will have to provide a design
    dictionary and set of fixed nodes yourself.

    Defaults to your local directory.

    Args:
        save_path: path to be saved to. Must end in a `.py` file

    Returns:
        None
    """
    script = files(story).joinpath("example.py").read_text(encoding="utf8")
    with open(save_path, "w") as f:
        f.write(script)


def save_simple_pymapdl_script(
    save_path: pathlib.Path = pathlib.Path("./pymapdl_simple.py"),
) -> None:
    """Save a super-simple PyMAPDL example bridge script to file.

    This package comes with a pre-built example PyMAPDL script that can be
    used to streamline testing using pure PyMAPDL and bypassing the codefest
    library entirely. This function lets you access it. This version is a
    simpler pymapdl script.

    This example has been tailored to be as simple as possible whilst still
    running and does not require additional input to work.

    Defaults to your local directory.

    Args:
        save_path: path to be saved to. Must end in a `.py` file

    Returns:
        None
    """
    script = (
        files(story).joinpath("simplest_mapdl_example.py").read_text(encoding="utf8")
    )
    with open(save_path, "w") as f:
        f.write(script)
