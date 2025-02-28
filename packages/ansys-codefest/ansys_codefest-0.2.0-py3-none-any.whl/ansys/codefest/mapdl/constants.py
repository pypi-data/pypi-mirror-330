from dataclasses import dataclass
from enum import IntEnum
from math import sqrt
from typing import TypedDict
from typing import Union


@dataclass(frozen=True)
class PhysicalLimits:
    """Dataclass to store the physical limits that can be encountered.

    Instances are immutable.
    """

    smallest: float
    largest: float


@dataclass(frozen=True)
class Material:
    """Dataclass designed to hold material information.

    Instances are immutable"""

    name: str
    density: float
    elastic_modulus: float
    poissons_ratio: float
    yield_strength: float
    price_per_kg: float
    id: int

    def __str__(self):
        s = f"""
            Material {self.id}: {self.name}
            ----------------
            Density: {self.density} kg/m^3
            Elastic Modulus: {self.elastic_modulus} Pa
            Poissons ratio: {self.poissons_ratio}
            Yield Strength: {self.yield_strength} Pa
            Price/kg: ${self.price_per_kg} /kg 
            
            """
        return s


STEEL = Material("Steel", 7850.0, 210.0e9, 0.29, 330.0e6, 1.2, 1)
COPPER = Material("Copper", 8940.0, 125.0e9, 0.345, 30.0e6, 9.3, 2)
# Al 6061 T6
ALUMINUM = Material("Aluminum", 2800.0, 70.0e9, 0.33, 270.0e6, 3.5, 3)
EXPANDED_POLYSTYRENE = Material(
    "Expanded Polystyrene", 24.0, 0.007e9, 0.275, 0.175e6, 3.0, 4
)
TITANIUM = Material("Titanium", 4500.0, 110.0e9, 0.35, 500.0e6, 15.0, 5)
IRON = Material("Cast Iron", 7000.0, 90.0e9, 0.26, 80.0e6, 0.5, 6)
DIAMOND = Material("Diamond", 3500.0, 1100.0e9, 0.2, 2850.0e6, 400000.0, 7)
CONCRETE = Material("Concrete", 2200.0, 15.0e9, 0.185, 1.0e6, 0.04, 8)
GRANITE = Material("Granite", 3000.0, 60.0e9, 0.2, 17.0e6, 3.5, 9)
MARBLE = Material("Marble", 2800.0, 60.0e9, 0.18, 8.0e6, 0.71, 10)
SANDSTONE = Material("Sandstone", 2400.0, 19.5e9, 0.255, 13.0e6, 0.5, 11)
ICE = Material("Ice", 925.0, 9.15e9, 0.365, 6.5e6, 0.25, 12)
OAK = Material("Oak", 800.0, 15.0e9, 0.375, 70.0e6, 2.3, 13)
PINE = Material("Pine", 400.0, 9.0e9, 0.375, 32.0e6, 1.0, 14)
BEECH = Material("Beech", 750.0, 15.0e9, 0.375, 58.0e6, 2.4, 15)
CORK = Material("Cork", 150.0, 0.02e9, 0.1, 0.5e6, 5.0, 16)

MATERIALS = {
    m.id: m
    for m in [
        STEEL,
        COPPER,
        ALUMINUM,
        EXPANDED_POLYSTYRENE,
        TITANIUM,
        IRON,
        DIAMOND,
        CONCRETE,
        GRANITE,
        MARBLE,
        SANDSTONE,
        ICE,
        OAK,
        PINE,
        BEECH,
        CORK,
    ]
}
MATERIAL_IDS = list(MATERIALS.keys())
MAX_EDGE_LENGTH = sqrt(2.0)
INT_OR_FLOAT = Union[int, float]
COORD_2D = list[INT_OR_FLOAT]

PHYSICAL_LIMITS = PhysicalLimits(1.0e-6, 10.0)


class BeamXn(IntEnum):
    """Beam cross-section enum.

    In PyMAPDL the beam cross-sections correspond to the following sectypes.

        * RECT = RECTANGLE = 1

        * HREC = RECTANGLETUBE = 4

        * CSOLID = CIRCLE = 2

        * CTUBE = CYLINDER = 3

    Dimensions structure for each cross-section shown below:

    RECTANGLE - [width, height]

    RECTANGLETUBE - [total_width, total_height,
                     left_wall_thickness, right_wall_thickness,
                     bottom_wall_thickness, top_wall_thickness]

    CIRCLE - [radius]

    CYLINDER - [inner_radius, outer_radius]

    Examples:
    ```python-repl
        >>> import ansys.codefest.mapdl as acf
        >>> acf.BeamXn.RECTANGLE
        <BeamXn.RECTANGLE: 1>
    ```
    """

    RECTANGLE = 1
    CIRCLE = 2
    CYLINDER = 3
    RECTANGLETUBE = 4


class StoryType(IntEnum):
    """The three types of story presentation ranging from least to most
    verbose. Integer Enum.

    - MINIMAL = 0
    - CONCISE = 1
    - VERBOSE = 2
    """

    MINIMAL = 0
    CONCISE = 1
    VERBOSE = 2


class Submission(TypedDict):
    """Challenge submission dictionary schema type.

    This class is a `typing.TypedDict` class that specifies
    the schema all dictionary submissions should follow to
    be valid when submitted. All entries can be any order,
    except where explicitly stated.

    Notes:
        The submission should contain details of all the material
        *to be built* in the challenge. It should not contain any material
        that has already been constructed by the challenge,
        unless it is required in order to specify a new object. For example,
        the start and end nodes (numbered 1 and 2) should NOT be redefined in
        a submission, however they *can* be used to create beam elements in
        the `beams` property. All rocks follow similar logic.

    Args:
        nodes: list of node numbers
        beams: list of beams represented by pairs of node numbers
        load_path: list of continuous connected nodes, in order,
                   leading from 1 through to 2.
        cross_section: list of BeamXn enum objects. This order corresponds
                       to the order of values in the `beams`.
        dimensions: list of dimensions for each cross-section.
                    Corresponds to the order of values in the `beams`.
        materials: list of materials for each beam, represented as integers.
                   Corresponds to the order of values in the `beams`.

    Examples:

    The suggested design for example 1a is shown below.

    ```
        {"nodes": [[3, -2, 1],
                   [4, -1, 1],
                   [5, 0, 1],
                   [6, 1, 1],
                   [7, 2, 1],
                   [8, 0, 0],
                   [9, 0, -1]],
                  "beams": [[1, 3],
                   [3, 4],
                   [4, 5],
                   [5, 6],
                   [6, 7],
                   [7, 2],
                   [5, 8],
                   [8, 9],
                   [9, 59]],
                  "load_path": [1, 3, 4, 5, 6, 7, 2],
                  "cross_section": [2, 2, 2, 2, 2, 2, 2, 2, 2],
                  "dimensions": [[0.025], [0.025], [0.025], [0.025],
                                 [0.025], [0.025], [0.025], [0.025],
                                 [0.025]],
                  "materials": [1, 1, 1, 1, 1, 1, 3, 3, 3]}
    ```

    """

    nodes: list[int]
    beams: list[list[int]]
    load_path: list[int]
    cross_section: list[BeamXn]
    dimensions: list[list[float]]
    materials: list[int]
