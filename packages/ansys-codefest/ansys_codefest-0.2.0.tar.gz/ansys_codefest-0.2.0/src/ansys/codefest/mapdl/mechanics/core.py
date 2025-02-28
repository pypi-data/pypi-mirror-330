"""
`mechanics`

`mapdl` sandbox. This is the PyMAPDL wrapper that the library uses
behind-the-scenes. It is available for use if wanted.

Work-in-progress; the interface is still subject to change.

The broad structure of using the wrapper is as follows.

1. Create the nodes & the boundary conditions at each node
    * including degrees of freedom and forces
2. Create the beams, and set the materials for each beam
3. Create a blueprint from the nodes and beams
4. Create a simulation from the blueprint
5. Run the simulation
6. Process the results

> Nodes -> Beams -> Blueprint -> Simulation

## Examples

In this simple example we create a pair of nodes, connected by a horizontal
beam with a downward force applied to one of the nodes, perpendicular to the
beam. The other node we fix in space.

```python
import ansys.codefest.mapdl as acf
import matplotlib.pyplot as plt

nodes = [acf.Node(1, acf.Vector.zero(),
         acf.NodalBoundaryCondition.fixed_point()),
         acf.Node(2, acf.Vector(.8, 0., 0.),
         acf.NodalBoundaryCondition.free_point(acf.Vector(0., -100., 0.)))]
beams = [acf.Beam(nodes[0], nodes[1])]

blueprint = acf.Blueprint(nodes, beams)

sim = acf.Simulation(blueprint)
sim.execute()
sim.plot_result()
plt.show()
```

"""

import pathlib
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, pi

import matplotlib as mpl
from matplotlib.colorbar import Colorbar
import matplotlib.pyplot as plt
from ansys.mapdl.core import launch_mapdl, Mapdl
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from ..constants import BeamXn, Submission
from ..constants import Material, MATERIALS, COORD_2D, MAX_EDGE_LENGTH, STEEL
from ..validation import is_valid_attempt
from ..tools import Challenge, Server

try:
    from ansys.mapdl.core.mapdl import _MapdlCore as MapdlBase
except ImportError:
    from ansys.mapdl.core.mapdl import MapdlBase as MapdlBase


class BlueprintConstructionException(Exception):
    """Exception raised when a blueprint is transformed into a simulation
    and an error is encountered.
    """

    pass


class TypeNode(IntEnum):
    """Enum for the type a node can be.

    START nodes are those at which you enter a cavern.
    END nodes are the exit nodes for the caverns.
    CONSTRUCTED nodes are built by yourself or your machine.
    ROCK nodes are fixed nodes that are pre-existing in the caverns.

    Examples:
    ```python-repl
        >>> new = TypeNode.START
        >>> new
        <TypeNode.START: 1>
    ```

    """

    START = 1
    END = 2
    CONSTRUCTED = 3
    ROCK = 4


@dataclass
class Vector:
    """3D Float vector dataclass

    Simple 3D vector class for simple operations. Typically used for position,
    velocity, force, etc. The z-value can be assumed to be 0 because this
    framework deals only with 2D problems for now.

    Examples:
    ```python-repl
        >>> import ansys.codefest.mapdl as acf
        >>> v = acf.Vector(1., 2., 3.)
    ```

    """

    x: float
    y: float
    z: float = 0.0

    def __str__(self) -> str:
        return f"Vector({self.x:.6g}, {self.y:.6g}, {self.z:.6g})"

    @classmethod
    def zero(cls) -> "Vector":
        """Class method to generate a zero-vector

        Returns:
            all-zero Vector
        """
        return cls(0.0, 0.0, 0.0)

    def is_non_zero(self) -> bool:
        """Return True if any component in the vector is non-zero.

        Returns:
            True if any value is non-zero, else False
        """
        return self.x != 0.0 or self.y != 0.0 or self.z != 0.0


@dataclass(frozen=True)
class BooleanVector:
    """3D Boolean vector dataclass.

    Simple 3D vector class for simple boolean operations.
    Typically used for vectors where components are optional.

    The components are explicitly refewrred to as x, y and z.

    Examples:
    ```python-repl
        >>> import ansys.codefest.mapdl as acf
        >>> bv = acf.BooleanVector(True, False, True)
        >>> bv.y
        False
        >>> bv.z
        True
    ```

    """

    x: bool
    y: bool
    z: bool

    def __str__(self) -> str:
        return f"BVector({self.x}, {self.y}, {self.z})"

    @classmethod
    def all_true(cls) -> "BooleanVector":
        """Return an instance of BooleanVector which is True in all components

        Returns:
            a BooleanVector with all True properties
        """
        return cls(True, True, True)

    @classmethod
    def all_false(cls) -> "BooleanVector":
        """Return an instance of BooleanVector which is False in all components

        Returns:
            a BooleanVector with all False properties
        """
        return cls(False, False, False)

    @property
    def true(self) -> bool:
        """If the vector is True in all components return True.

        Returns:
            True if all components are True, otherwise False
        """
        return self.x and self.y and self.z

    @property
    def false(self) -> bool:
        """If the vector is False in all components return True.

        Returns:
            True if all components are False, otherwise False
        """
        return not self.x and not self.y and not self.z


@dataclass()
class NodalBoundaryCondition:
    """Dataclass storing the boundary conditions at a node.

    Warp freedom currently ignored."""

    force: Vector
    translational_freedoms: BooleanVector = BooleanVector.all_true()
    rotational_freedoms: BooleanVector = BooleanVector.all_true()

    def __str__(self) -> str:
        return (
            f"NodalBC(Force({self.force.x}, {self.force.y}, "
            f"{self.force.z}), "
            f"translation DOF={self.translational_freedoms},"
            f" rotational DOF={self.rotational_freedoms})"
        )

    def remove_all_freedoms(self) -> None:
        """Remove all degrees of freedom from the node

        Returns:
            None
        """
        self.translational_freedoms = BooleanVector.all_false()
        self.rotational_freedoms = BooleanVector.all_false()

    def remove_translation_freedoms(self) -> None:
        """Remove all translational degrees of freedom from the node

        Returns:
            None
        """
        self.translational_freedoms = BooleanVector.all_false()

    def remove_rotational_freedoms(self) -> None:
        """Remove all rotational degrees of freedom from the node

        Returns:
            None
        """
        self.rotational_freedoms = BooleanVector.all_false()

    def add_translation_freedoms(self) -> None:
        """Add all translational degrees of freedom to the node

        Returns:
            None
        """
        self.translational_freedoms = BooleanVector.all_true()

    def add_rotational_freedoms(self) -> None:
        """Add all rotational degrees of freedom to the node

        Returns:
            None
        """
        self.rotational_freedoms = BooleanVector.all_true()

    def has_applied_force(self) -> bool:
        """If any force has been applied to the node, return True,
        else False.

        Returns:
            True if force has been applied, False if not.
        """
        for component in [self.force.x, self.force.y, self.force.z]:
            if component != 0.0:
                return True
        return False

    @classmethod
    def fixed_point(cls, force: Vector = Vector.zero()) -> "NodalBoundaryCondition":
        """Create a fixed point boundary condition with no degrees of freedom

        optionally, you can also supply a force to be applied to the node.

        Args:
            force: a vector of the force to be applied to the node

        Returns:
            The nodal boundary condition
        """
        return cls(force, BooleanVector.all_false(), BooleanVector.all_false())

    @classmethod
    def free_point(cls, force: Vector = Vector.zero()) -> "NodalBoundaryCondition":
        """Create a free point boundary condition with all degrees of freedom

        optionally, you can also supply a force to be applied to the node.

        Args:
            force: a vector of the force to be applied to the node

        Returns:
            The nodal boundary condition
        """
        return cls(force, BooleanVector.all_true(), BooleanVector.all_true())


@dataclass
class Node:
    """Point used to join beams together and specify BCs."""

    number: int
    position: Vector
    _boundary_condition: NodalBoundaryCondition = None
    type: TypeNode = TypeNode.CONSTRUCTED

    def __str__(self) -> str:
        return f"Node({self.number}, {self.position})"

    @property
    def boundary_condition(self) -> NodalBoundaryCondition:
        """Getter & setter for the nodal boundary condition.

        Returns:
            The nodal boundary condition
        """
        if self._boundary_condition is None:
            self._boundary_condition = NodalBoundaryCondition.free_point()
        return self._boundary_condition

    @boundary_condition.setter
    def boundary_condition(self, value: NodalBoundaryCondition):
        if isinstance(value, NodalBoundaryCondition) is not True:
            raise TypeError(f"{value} must be of type NodalBoundaryCondition")
        self._boundary_condition = value

    @classmethod
    def start_node(cls, coord: COORD_2D) -> "Node":
        """Create an instance of a 'start' node at a given coordinate.

        Args:
            coord: x,y coordinate

        Returns:
            The created node object
        """
        cx, cy = coord
        return cls(
            1,
            Vector(float(cx), float(cy), 0.0),
            NodalBoundaryCondition.fixed_point(),
            TypeNode.START,
        )

    @classmethod
    def end_node(cls, coord: COORD_2D) -> "Node":
        """Create an instance of an 'end' node at a given coordinate.

        Args:
            coord: x,y coordinate

        Returns:
            The created node object
        """
        cx, cy = coord
        return cls(
            2,
            Vector(float(cx), float(cy), 0.0),
            NodalBoundaryCondition.fixed_point(),
            TypeNode.END,
        )

    @classmethod
    def rock_node(cls, coord: COORD_2D, num: int) -> "Node":
        """Create an instance of a 'rock' node at a given coordinate.

        AKA a fixed point node.

        Unlike start and end nodes which have fixed node numbers the rock node
        must have a node id_ specified. This can not be a id_ in-use
        elsewhere.

        Args:
            coord: x,y coordinate
            num: node number

        Returns:
            The created node object
        """
        cx, cy = coord
        return cls(
            num,
            Vector(float(cx), float(cy), 0.0),
            NodalBoundaryCondition.fixed_point(),
            TypeNode.ROCK,
        )

    @classmethod
    def constructed_node(cls, coord: COORD_2D, num: int) -> "Node":
        """Create a 'constructed' node. AKA a node from a design.

        Unlike start and end nodes which have fixed node numbers constructed
        nodes must have a node id_ specified.
        This can not be an id_ in-use elsewhere.

        Args:
            coord: x,y coordinate
            num: node number

        Returns:
            The created node object
        """
        cx, cy = coord
        return cls(
            num,
            Vector(float(cx), float(cy), 0.0),
            NodalBoundaryCondition.fixed_point(),
            TypeNode.CONSTRUCTED,
        )

    def is_valid(self) -> tuple[bool, list[str]]:
        """Returns (True, feedback) if this Node instance is valid for use.

        If not valid feedback will be a list of strings explaining why the Node
        is invalid.

        Returns:
            result and feedback.
        """
        valid = True
        reasons = []
        if not isinstance(self.number, int):
            valid = False
            reasons.append("No node id_ provided")
        if valid and self.number <= 0:
            valid = False
            reasons.append("Node numbers must be integers greater than 0")
        if not isinstance(self.number, int):
            valid = False
            reasons.append("No node id_ provided")
        if not isinstance(self.position, Vector):
            valid = False
            reasons.append("No node position provided")
        if not isinstance(self.boundary_condition, NodalBoundaryCondition):
            valid = False
            reasons.append("No boundary condition provided")
        if not isinstance(self.type, TypeNode):
            valid = False
            reasons.append("No node type provided")
        return valid, reasons


@dataclass(frozen=True)
class CrossSection:
    """Beam cross-section details.

    There are 4 cross-sections available.;

        - RECT - BeamXn.RECTANGLE
        - HREC - BeamXn.RECTANGLETUBE
        - CSOLID - BeamXn.CIRCLE
        - CTUBE - BeamXn.CYLINDER

    Args:
        shape: Beam cross-section shape
        dimensions: Dimensions list to accompany the shape
    """

    shape: BeamXn
    dimensions: list[float]

    @property
    def area(self) -> float:
        """Return the cross-sectional area of the beam.

        Returns:
            Beam area as a float
        """
        if self.shape == BeamXn.CIRCLE:
            area = pi * self.dimensions[0] ** 2.0
        elif self.shape == BeamXn.CYLINDER:
            area = pi * max(self.dimensions) ** 2.0 - pi * min(self.dimensions) ** 2.0
        elif self.shape == BeamXn.RECTANGLE:
            area = self.dimensions[0] * self.dimensions[1]
        elif self.shape == BeamXn.RECTANGLETUBE:
            width, height = self.dimensions[0], self.dimensions[1]
            t1, t2, t3, t4 = (
                self.dimensions[2],
                self.dimensions[3],
                self.dimensions[4],
                self.dimensions[5],
            )
            area = width * height - (width - t1 - t2) * (height - t3 - t4)
        else:
            raise NotImplementedError(
                f"Unrecognised cross-section " f"type {self.shape}"
            )
        return area

    def is_valid(self) -> tuple[bool, list[str]]:
        """Return True if this instance of CrossSection has valid param values.

        If it is not valid, feedback will be a list of strings explaining
        why the Node is invalid.

        Returns:
            answer to question posed by function name as well as feedback.
        """
        valid = True
        reasons = []
        if not isinstance(self.shape, BeamXn):
            valid = False
            reasons.append("No beam cross-section provided")
        if not isinstance(self.dimensions, list):
            valid = False
            reasons.append("invalid dimension list provided")
        return valid, reasons


@dataclass
class Beam:
    """Dataclass for continuous material linking two nodes.

    Args:
        start: starting node of beam
        end: ending node of beam
        section: cross-section of beam
        material: material of beam
        number: beam number
        stress: maximum stress experienced by beam. Initialises as 0.
    """

    start: Node
    end: Node
    section: CrossSection = CrossSection(BeamXn.CIRCLE, [0.01])
    material: Material = STEEL
    number: int = None
    stress: float = 0.0

    def __str__(self) -> str:
        return (
            f"Beam({self.number: ^3}"
            f"Nodes {self.start.number: ^3} - {self.end.number: ^3} "
            f"-- Mat: {self.material.id: ^2} -- Stress: {self.stress:g} Pa)"
        )

    @property
    def length(self) -> float:
        """Return beam length

        Returns:
            beam length as float
        """
        length = calc_distance_between_vectors(self.start.position, self.end.position)
        return length

    @property
    def cross_section_area(self) -> float:
        """Return beam cross-section area.

        Returns:
            beam area as a float
        """
        return self.section.area

    @property
    def mass(self) -> float:
        """Return Beam mass

        Returns:
            beam mass ass a float
        """
        return self.length * self.cross_section_area * self.material.density

    @property
    def cost(self) -> float:
        """Return Beam cost

        Returns:
            beam cost as a float, in dollarydoos
        """
        return self.mass * self.material.price_per_kg

    def has_been_broken(self) -> bool:
        """Return True if the beam has experienced stress >= its yield.

        Returns:
            True if any of the bridge has exceeded the equivalent yield stress
        """
        return abs(self.stress) > abs(self.material.yield_strength)

    def is_valid(self) -> tuple[bool, list[str]]:
        """Return True if this instance of Beam is valid.

        list tuple will contain feedback on why False, or will be empty when
        True.

        Returns:
            answer to the question posed by the function name as well as
            feedback
        """
        reasons = []
        valid = True
        if not isinstance(self.start, Node):
            valid = False
            reasons.append("No start node was provided.")
        if not isinstance(self.end, Node):
            valid = False
            reasons.append("No end node was provided.")
        if valid and self.length > MAX_EDGE_LENGTH:
            valid = False
            reasons.append(
                f"Beam {self.number} - "
                f"({self.start.number}, {self.end.number}) "
                f"is too long"
            )
        if not isinstance(self.section, CrossSection):
            valid = False
            reasons.append("No beam cross-section was provided.")
        if not isinstance(self.material, Material):
            valid = False
            reasons.append("No material was provided for this beam.")

        return valid, reasons

    def is_beam_allowed(self) -> tuple[bool, list[str]]:
        """Return True if beam is allowed by the environment.

        Difference between 'allowed' and 'valid'.
        All allowed beams are valid but not all valid beams are allowed.

        Returns:
            answer to function question as well as feedback
        """
        reasons = []
        allowed = True
        if abs(self.length) > MAX_EDGE_LENGTH:
            allowed = False
            reasons.append(f"Beam {self.number}'s nodes are too far apart.")
        return allowed, reasons


@dataclass
class Blueprint:
    """The Plan/Blueprint for a simulation. Contains nodes, beams and BCs.

    Args:
        nodes: list of nodes created for the blueprint
        beams: list of beams created for the blueprint
    """

    nodes: list[Node]
    beams: list[Beam]

    @classmethod
    def _from_challenge(cls, challenge: Challenge) -> "Blueprint":
        """Create a blueprint from a particular level

        Args:
            challenge: The challenge object

        Returns:
            a new Blueprint object
        """
        fixed_nodes = challenge.get_fixed_nodes()
        nodes = []
        for coord in fixed_nodes:
            if coord[0] == 1:
                n = Node.start_node(coord[1:])
            elif coord[0] == 2:
                n = Node.end_node(coord[1:])
            else:
                n = Node.rock_node(coord[1:], coord[0])
            nodes.append(n)
        return cls(nodes, [])

    @property
    def grid_lims(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the populated grid limits.

        Returns:
            the resulting grid limits
        """
        xes = [n.position.x for n in self.nodes]
        yes = [n.position.y for n in self.nodes]
        xmin = min(xes) if xes else 0
        xmax = max(xes) if xes else 0

        ymin = min(yes) if yes else 0
        ymax = max(yes) if yes else 0

        return (xmin, xmax), (ymin, ymax)

    def is_valid(self) -> tuple[bool, str]:
        """Returns True if this Blueprint instance is ready to be
        converted to a sim.

        A blueprint must contain a list of nodes, a list of beams, a load path
        (going from node 1 to node 2 via nodes connected by beams), a beam
        cross-section value and the dimensions of that cross-section.

        Returns:
            answer to function question as well as feedback
        """
        valid = True
        reasons = []
        # nodes
        node_nums = set()
        node_coords = set()
        for node in self.nodes:
            valid_node, node_reasons = node.is_valid()
            reasons.extend(node_reasons)
            if not valid_node:
                valid = False
            if valid_node and node.number in node_nums:
                valid = False
                reasons.append(f"Node {node.number} appears multiple times.")
            node_nums.add(node.number)
            node_coord = (node.position.x, node.position.y)
            if valid_node and node_coord in node_coords:
                valid = False
                reasons.append(f"Multiple nodes found at point {node_coord}")
            node_coords.add(node_coord)

        for beam in self.beams:
            valid_beam, beam_reasons = beam.is_valid()
            if not valid_beam:
                valid = valid_beam
            reasons.extend(beam_reasons)
            if valid_beam:
                allowed_beam, allowance_reasons = beam.is_beam_allowed()
                if not allowed_beam:
                    valid = allowed_beam
                reasons.extend(allowance_reasons)
        return valid, "\n".join(reasons)

    @property
    def mass(self) -> float:
        """Return total mass of material in the blueprint.

        Returns:
            mass of material as a float
        """
        mass = 0.0
        for beam in self.beams:
            length = beam.length
            area = beam.cross_section_area
            mass += length * area * beam.material.density
        return mass

    @property
    def cost(self) -> float:
        """Return total cost of material in the blueprint.

        Returns:
            cost of the material in dollary doos
        """
        cost = 0.0
        for beam in self.beams:
            length = beam.length
            area = beam.cross_section_area
            cost += length * area * beam.material.density * beam.material.price_per_kg
        return cost

    def save_as(self, file_path: pathlib.Path = pathlib.Path("./input.txt")) -> None:
        """save blueprint to specified file path.

        Defaults to "input.txt" in your current working directory.

        Args:
            file_path: path to where you wish to save the file

        Returns:
            None
        """
        lines = [
            "\nNODES",
            "\nNumber\tx [m]\ty [m]\tnode type" "\tnodal boundary condition",
        ]
        for node in self.nodes:
            line = (
                f"\n{node.number}\t{node.position.x}\t"
                f"{node.position.y}\t{node.type}\t{node.boundary_condition}"
            )
            lines.append(line)

        lines.extend(["\n"] * 2)
        lines.append("\nBEAMS")
        lines.append("\nNumber\tStart\tEnd\tMaterialSection")
        for beam in self.beams:
            line = (
                f"\n{beam.number}\t{beam.start.number}"
                f"\t{beam.end.number}\t{beam.material.id}\t{beam.section}"
            )
            lines.append(line)

        with open(file_path, "w") as f:
            f.writelines(lines)

    def with_challenge_attempt_geometry(self, attempt: Submission) -> None:
        """Add challenge attempt geometry to blueprint.

        Args:
            attempt: design dictionary for this attempt

        Returns:
            None
        """
        valid, reasons = is_valid_attempt(attempt)
        if not valid:
            raise BlueprintConstructionException(reasons)
        for node in attempt["nodes"]:
            n = Node(
                node[0],
                Vector(node[1], node[2], 0),
                NodalBoundaryCondition.free_point(),
                TypeNode.CONSTRUCTED,
            )
            self.nodes.append(n)
        beam_node_nums = {b for beam in attempt["beams"] for b in beam}
        all_node_nums = {n.number for n in self.nodes}
        if not beam_node_nums.issubset(all_node_nums):
            raise BlueprintConstructionException(
                "Beam list contains nodes "
                "that are not in the node "
                "list OR the fixed node "
                "list."
            )
        result, reason = self._does_load_path_link_up(attempt)
        if not result:
            raise BlueprintConstructionException(reason)
        if "materials" in attempt:
            mats = attempt["materials"]  # type: list[int]
        else:
            mats = [1] * len(attempt["beams"])
        all_cross_sections: list[BeamXn] = [BeamXn(c) for c in attempt["cross_section"]]
        all_dimensions: list[list[float]] = attempt["dimensions"]
        cross_sections = [
            CrossSection(c, d) for c, d in zip(all_cross_sections, all_dimensions)
        ]
        for beam, mat, xn in zip(attempt["beams"], mats, cross_sections):
            n1 = [n for n in self.nodes if n.number == beam[0]][0]
            n2 = [n for n in self.nodes if n.number == beam[1]][0]
            b = Beam(n1, n2, xn, material=MATERIALS[mat])
            self.beams.append(b)
        for node_number in attempt["load_path"]:
            node = [n for n in self.nodes if n.number == node_number][0]
            node.boundary_condition.force = Vector(0.0, -9.81 * 1.0e3, 0.0)

        node1 = [n for n in self.nodes if n.number == 1][0]
        node2 = [n for n in self.nodes if n.number == 2][0]
        node1.boundary_condition.remove_all_freedoms()
        node2.boundary_condition.remove_all_freedoms()

        if not (reasons := self.is_valid()):
            raise BlueprintConstructionException(reasons)

    def _does_load_path_link_up(self, design: Submission) -> tuple[bool, str]:
        start, design_start, end, design_end = None, None, None, None
        start_num = design["load_path"][1]
        end_num = design["load_path"][-2]
        for n in self.nodes:
            if n.number == start_num:
                design_start = n
            if n.number == end_num:
                design_end = n
            if n.number == 1:
                start = n
            if n.number == 2:
                end = n

        if not all([start, design_start, end, design_end]):
            return False, "load path is missing a node."
        start_dist = calc_distance_between_vectors(
            start.position, design_start.position
        )
        end_dist = calc_distance_between_vectors(end.position, design_end.position)
        if start_dist > MAX_EDGE_LENGTH:
            return (
                False,
                f"Distance between nodes 1 and " f"{design_start.number} is too great",
            )
        if end_dist > MAX_EDGE_LENGTH:
            return (
                False,
                f"Distance between nodes 2 and " f"{design_start.number} is too great",
            )
        return True, ""


@dataclass
class Simulation:
    """Simulation class. Consumes 1 blueprint instance in order to perform.

    Most args are left as defaults and calculated during the building phase.

    Args:
        blueprint: a blueprint object
        nodes: list of nodes to be simulated
        beams: list of beams to be simulated
        mapdl: base mapdl object (or existing session object)
        mapdl_version: version number if specific one is needed
        mapdl_loc: location on your harddrive of the mapdl executable if needed
        server: server url if connection to remote server needed.

    """

    blueprint: Blueprint
    nodes: list[Node] = None
    beams: list[Beam] = None
    mapdl: MapdlBase = None
    mapdl_version: int = None
    mapdl_loc: pathlib.Path = None
    server: Server = None

    def setup(self) -> MapdlBase:
        """Run the standard MAPDL set up commands and return mapdl namespace.

        Returns:
            MapdlBase
        """
        if self.server is not None:
            mapdl = Mapdl(ip=self.server.ip, port=self.server.port, local=False)
        elif self.mapdl_loc is not None:
            mapdl = launch_mapdl(override=True, exec_file=self.mapdl_loc.as_posix())
        elif self.mapdl_version is not None:
            mapdl = launch_mapdl(override=True, version=self.mapdl_version)
        else:
            mapdl = launch_mapdl(override=True)
        mapdl.clear()
        mapdl.prep7()
        mapdl.units("SI")  # SI - International system (m, kg, s, K).
        self.mapdl = mapdl
        return mapdl

    def set_materials(self) -> None:
        """Set the materials as dictated by the blueprint

        Returns:
            None
        """
        self.mapdl.et(1, "BEAM188")
        # We just need to supply EX; APDL assumes isotropy if we do
        for id_, material in MATERIALS.items():
            self.mapdl.mp("EX", id_, material.elastic_modulus)
            self.mapdl.mp("PRXY", id_, material.poissons_ratio)
            self.mapdl.mp("DENS", id_, material.density)

    def set_cross_section(self, section: CrossSection) -> None:
        """Set the cross-section for all subsequent beams.

        Args:
            section: CrossSection object

        Returns:
            None
        """
        cross_section = section.shape
        dimensions = section.dimensions
        if cross_section == BeamXn.CIRCLE:
            self.mapdl.sectype(1, "BEAM", "CSOLID")
            # radius
            self.mapdl.secdata(dimensions[0])
        elif cross_section == BeamXn.CYLINDER:
            self.mapdl.sectype(1, "BEAM", "CTUBE")
            # inner radius, outer radius
            self.mapdl.secdata(dimensions[0], dimensions[1])
        elif cross_section == BeamXn.RECTANGLETUBE:
            self.mapdl.sectype(1, "BEAM", "HREC")
            # width, height, WEST thickness, EAST thickness,
            # SOUTH thickness, NORTH thickness
            self.mapdl.secdata(
                dimensions[0],
                dimensions[1],
                dimensions[2],
                dimensions[3],
                dimensions[4],
                dimensions[5],
            )
        elif cross_section == BeamXn.RECTANGLE:
            self.mapdl.sectype(1, "BEAM", "RECT")
            self.mapdl.secdata(dimensions[0], dimensions[1])

    def construct_nodes(self) -> None:
        """Construct the simulation's nodes as dictated by the blueprint

        Returns:
            None
        """
        nodes = deepcopy(self.blueprint.nodes)
        self.nodes = []
        for node in nodes:
            self.mapdl.n(node.number, node.position.x, node.position.y, 0)
            self.nodes.append(node)

    def construct_beams(self) -> None:
        """Construct the simulation's beams/elements as dictated
        by the blueprint

        Returns:
            None
        """
        beams = deepcopy(self.blueprint.beams)
        self.beams = []
        for beam in beams:
            self.set_cross_section(beam.section)
            self.mapdl.mat(beam.material.id)
            beam.number = self.mapdl.e(beam.start.number, beam.end.number)
            self.beams.append(beam)

    def apply_force(self, gravity: bool = True) -> None:
        """Apply forces to nodes as dictated by the blueprint

        Returns:
            None
        """
        self.mapdl.antype("STATIC")
        additional_load = Vector.zero()
        if gravity:
            self.mapdl.acel(acel_y=9.81)
        for node in self.nodes:
            force = node.boundary_condition.force
            self.mapdl.f(node.number, "Fx", force.x + additional_load.x)
            self.mapdl.f(node.number, "Fy", force.y + additional_load.y)
            self.mapdl.f(node.number, "Fz", force.z + additional_load.z)

    def constrain_dof(self) -> None:
        """Constrain the simulation's nodes as dictated by the blueprint

        Returns:
            None
        """
        for node in self.nodes:
            bc = node.boundary_condition
            translation = bc.translational_freedoms
            rotation = bc.rotational_freedoms
            # If not all translation factors are free then ask which are not
            # free and constrain them in turn
            if not translation.true:
                if not translation.x:
                    self.mapdl.d(node.number, "UX")
                if not translation.y:
                    self.mapdl.d(node.number, "UY")
                if not translation.z:
                    self.mapdl.d(node.number, "UZ")
            if not rotation.true:
                if not rotation.x:
                    self.mapdl.d(node.number, "ROTX")
                if not rotation.y:
                    self.mapdl.d(node.number, "ROTY")
                if not rotation.z:
                    self.mapdl.d(node.number, "ROTZ")

    def solve(self) -> None:
        """Run the simulation

        Executes the APDL simulation.

        Returns:
            None
        """
        self.mapdl.run("/SOLU")
        self.mapdl.solve()
        self.mapdl.finish()

    def execute(self) -> None:
        """Run the entire Simulation script in order.

        Returns:
            None
        """
        self.setup()
        self.set_materials()
        self.construct_nodes()
        self.construct_beams()
        self.apply_force()
        self.constrain_dof()
        self.solve()
        self.post_process()

    def post_process(self) -> None:
        """Process the results of the simulation.

        Extract and store the max equivalent stress on each beam.

        Returns:
            None
        """
        self.mapdl.post1()
        self.mapdl.set("LAST")
        for beam in self.beams:
            equiv = self.mapdl.get_value("secr", beam.number, "s", "eqv", "max")
            beam.stress = equiv
        self.mapdl.exit()

    def assess_for_breaks(self) -> tuple[bool, str]:
        """Assess which beams have broken, if any, and return a report.

        The result will be printed to screen, but, the success and the
        description of what happened will be returned together as a tuple of
        a bool and a string.

        Returns:
            tuple[bool, str]
        """
        num_failures = len([i for i in self.beams if i.has_been_broken()])
        string_result = [f"Beam Failures: {num_failures} out of {len(self.beams)}"]
        for beam in self.beams:
            if beam.has_been_broken():
                addendum = "- BREAK"
            else:
                addendum = ""
            percentage_diff = 100.0 * beam.stress / beam.material.yield_strength
            string_result.append(
                f"Beam {beam.number}: {beam.start.number: ^5} - "
                f"{beam.end.number: ^5} -> {percentage_diff:g} % "
                f"of yield {addendum}"
            )
        breakage = False
        if num_failures > 0:
            string_result.append(f'{"BRIDGE BREAKS":*^30}')
            breakage = True
        else:
            string_result.append(f'{"SUCCESS!":*^30}')
        return breakage, "\n".join(string_result)

    def fetch_beam_stresses(self) -> list[tuple[int, float]]:
        """Fetch the stresses on each beam, and include the beam id_.

        Returns a list of tuples containing the beam id_ and the stress that
        beam experienced.

        Returns:
            list of all beams, their numbers and their stresses

        """
        return [(b.number, b.stress) for b in self.beams]

    def plot_result(self) -> tuple[plt.Figure, plt.Axes, Colorbar]:
        """Plot the simulation's stresses and return the fig, ax, cb objects

        Returns:
            plotting material
        """
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        ax.set_aspect(1)
        cmap = cm.viridis.copy()
        cmap.set_over("pink")
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("top", size="5%", pad=0.5)
        for beam in self.beams:
            frac = beam.stress / beam.material.yield_strength
            color = cmap(frac)
            ax.plot(
                [beam.start.position.x, beam.end.position.x],
                [beam.start.position.y, beam.end.position.y],
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
        for node in self.nodes:
            if node.type == TypeNode.CONSTRUCTED:
                x_bridge_nodes.append(node.position.x)
                y_bridge_nodes.append(node.position.y)
            elif node.type == TypeNode.ROCK:
                x_rocks.append(node.position.x)
                y_rocks.append(node.position.y)
            elif node.type == TypeNode.START:
                x_start_node.append(node.position.x)
                y_start_node.append(node.position.y)
            elif node.type == TypeNode.END:
                x_end_node.append(node.position.x)
                y_end_node.append(node.position.y)
            if node.boundary_condition.force.is_non_zero():
                x_load_path.append(node.position.x)
                y_load_path.append(node.position.y)
        ax.plot(
            x_bridge_nodes,
            y_bridge_nodes,
            linestyle=" ",
            marker="D",
            color="gray",
            label="Construction",
            ms=2,
            mfc="None",
            mew=2,
        )
        ax.plot(
            x_start_node,
            y_start_node,
            linestyle=" ",
            marker=5,
            color="crimson",
            label="START",
            ms=8,
        )
        ax.plot(
            x_end_node,
            y_end_node,
            linestyle=" ",
            marker=4,
            color="crimson",
            label="END",
            ms=8,
        )
        ax.plot(
            x_rocks,
            y_rocks,
            linestyle=" ",
            marker="h",
            color="brown",
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
            color="crimson",
            label="loaded nodes",
        )
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.legend(loc="best")
        norm = mpl.colors.Normalize(vmin=0.0, vmax=100.0)
        cb = fig.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            cax=cax,
            orientation="horizontal",
            label="Percentage of Yield (%)",
            extend="max",
        )
        return fig, ax, cb


def calc_distance_between_vectors(v1: Vector, v2: Vector) -> float:
    """Calculate the distance between 2 cartesian vectors.

    Args:
        v1: Vector 1
        v2: Vector 2

    Returns:
        float
    """
    diff_x = (v1.x - v2.x) ** 2
    diff_y = (v1.y - v2.y) ** 2
    diff_z = (v1.z - v2.z) ** 2
    return sqrt(diff_x + diff_y + diff_z)
