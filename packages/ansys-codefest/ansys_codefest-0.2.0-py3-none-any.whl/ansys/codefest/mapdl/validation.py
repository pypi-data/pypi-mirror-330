from collections import namedtuple
from dataclasses import dataclass
from math import sqrt
from .constants import (
    MATERIALS,
    BeamXn,
    MAX_EDGE_LENGTH,
    INT_OR_FLOAT,
    PHYSICAL_LIMITS,
    Submission,
)

Coordinate = namedtuple("Coordinate", ["x", "y"])


def calc_graph_node_distance(n1: "GraphNode", n2: "GraphNode") -> float:
    return calc_distance_between_coords(
        (n1.coordinate.x, n1.coordinate.y), (n2.coordinate.x, n2.coordinate.y)
    )


def calc_distance_between_coords(
    xy1: tuple[INT_OR_FLOAT, INT_OR_FLOAT],
    xy2: tuple[INT_OR_FLOAT, INT_OR_FLOAT],
) -> float:
    diff_x = (xy1[0] - xy2[0]) ** 2
    diff_y = (xy1[1] - xy2[1]) ** 2
    return sqrt(diff_x + diff_y)


def is_valid_attempt(submission: Submission) -> tuple[bool, list[str]]:
    reasons = []
    valid = True
    valid = check_submission_dict(reasons, submission, valid)

    if not valid:
        return valid, reasons

    beams, node_dict, node_number_superset, nodes, valid = check_nodes_beams(
        reasons, submission, valid
    )

    loads, valid = check_xns_dims_mats(reasons, submission, valid)

    if not valid:
        return valid, reasons

    start_end, valid = check_nodes_beams_load_sets(
        beams, loads, node_number_superset, reasons, valid
    )

    valid = check_load_path_slopes(loads, node_dict, reasons, valid)

    for num in start_end:
        if num in node_number_superset:
            valid = False
            reasons.append(f"You can not have nodes numbered " f"{num} in your nodes")
    for node in nodes:
        if not isinstance(node.coordinate.x, int):
            valid = False
            reasons.append(
                f"node {node.number} has a non-integer " f"x-coord {node.coordinate.x}"
            )
        if not isinstance(node.coordinate.y, int):
            valid = False
            reasons.append(
                f"node {node.number} has a non-integer " f"y-coord {node.coordinate.y}"
            )
    return valid, reasons


def check_load_path_slopes(
    loads: list[int],
    node_dict: dict[int, "GraphNode"],
    reasons: list[str],
    valid: bool,
) -> bool:
    load_path_without_start_end = [i for i in loads if i not in [1, 2]]
    for i in range(len(load_path_without_start_end) - 1):
        node_a = node_dict[load_path_without_start_end[i]]
        node_b = node_dict[load_path_without_start_end[i + 1]]
        xdiff = node_b.coordinate.x - node_a.coordinate.x
        ydiff = node_b.coordinate.y - node_a.coordinate.y
        node_distance = sqrt(xdiff**2 + ydiff**2)
        if xdiff == 0 and ydiff != 0:
            valid = False
            reasons.append(
                f"The step between node {node_a.number} and "
                f"node {node_b.number} is vertical and not allowed"
            )
        if node_distance > MAX_EDGE_LENGTH:
            valid = False
            reasons.append(
                f"node {node_a.number} and node {node_b.number} "
                f"are too far apart ({node_distance:1.2f})"
            )
    return valid


def check_nodes_beams_load_sets(
    beams: list[list[int]],
    loads: list[int],
    node_number_superset: set[int],
    reasons: list[str],
    valid: bool,
) -> tuple[set[int], bool]:
    beam_node_set = {n for b in beams for n in b}
    load_node_set = set(loads)
    start_end = {1, 2}
    if not start_end.issubset(beam_node_set):
        valid = False
        reasons.append("Your beams do not connect to the start and/or end nodes.")
    if not start_end.issubset(load_node_set):
        valid = False
        reasons.append("Your load path must include the start/end nodes")
    if not load_node_set.issubset(beam_node_set):
        valid = False
        diff = load_node_set - beam_node_set
        reasons.append(
            f"Your load path includes nodes " f"unconnected to any other nodes {diff}"
        )
    if not (load_node_set - {1, 2}).issubset(node_number_superset):
        valid = False
        diff = load_node_set - node_number_superset - {1, 2}
        reasons.append(
            f"Your load path includes nodes "
            f"that are not amongst your node list {diff}"
        )
    return start_end, valid


def check_xns_dims_mats(
    reasons: list[str], submission: Submission, valid: bool
) -> tuple[list[int], bool]:
    cross_sections = submission["cross_section"]
    dimensions = submission["dimensions"]
    xn_valid, reasons_xn = are_all_cross_section_details_valid(
        cross_sections, dimensions, submission["beams"]
    )
    if not xn_valid:
        valid = xn_valid
        reasons.extend(reasons_xn)
    if "materials" in submission:
        materials_valid, reasons_materials = are_materials_valid(
            submission["materials"], submission["beams"]
        )
        if not materials_valid:
            valid = materials_valid
            reasons.extend(reasons_materials)
    loads = submission["load_path"]
    for n in loads:
        if not isinstance(n, int):
            valid = False
            reasons.append(f"node {n} in the load path is not an integer")
    return loads, valid


def check_nodes_beams(
    reasons: list[str], submission: Submission, valid: bool
) -> tuple[list[list[int]], dict[int, "GraphNode"], set[int], list["GraphNode"], bool]:
    nodes = [GraphNode.from_list(n) for n in submission["nodes"]]
    node_dict = {n.number: n for n in nodes}
    valid_nodes, reasons_nodes = are_nodes_valid(nodes)
    if not valid_nodes:
        valid = valid_nodes
        reasons.extend(reasons_nodes)
    node_number_list = [n.number for n in nodes]
    node_number_superset = set(node_number_list)
    beams = submission["beams"]
    beams_valid, reasons_beams = are_beams_valid(beams)
    if not beams_valid:
        valid = beams_valid
        reasons.extend(reasons_beams)
    return beams, node_dict, node_number_superset, nodes, valid


def check_submission_dict(
    reasons: list[str], submission: Submission, valid: bool
) -> bool:
    for key in ["nodes", "beams", "load_path", "cross_section", "dimensions"]:
        if key not in submission:
            valid = False
            reasons.append(f'"{key}" not present in submission')
        elif key != "cross_section" and not isinstance(submission[key], list):  # type: ignore
            valid = False
            reasons.append(f'"{key}" values are not a list')
    return valid


def are_nodes_valid(nodes: list["GraphNode"]) -> tuple[bool, list[str]]:
    reasons = []
    valid = True
    node_number_list = [n.number for n in nodes]
    node_number_superset = set(node_number_list)
    if len(node_number_superset) != len(nodes):
        for n in node_number_superset:
            count = node_number_list.count(n)
            if count > 1:
                valid = False
                reasons.append(f"node {n} appears {count} times in " f"the node list")
    return valid, reasons


def are_materials_valid(materials, beams):
    valid = True
    reasons = []
    if not isinstance(materials, list):
        reasons.append("Optional 'materials' key present but is not a list of ints")
        valid = False
    elif len(materials) != len(beams):
        reasons.append(
            "materials list must be the same length as the "
            "beam list, or not present at all."
        )
        valid = False
    for i, item in enumerate(materials):
        if not isinstance(item, int):
            valid = False
            reasons.append(
                f"Element {i} - {item} in the materials list " f"is not an integer"
            )
        elif item not in MATERIALS:
            valid = False
            allowed_ids = [(id_, m.name) for id_, m in MATERIALS.items()]
            reasons.append(
                f"Materials ID {item} at index {i} is not one of "
                f"the allowed material IDs "
                f"({allowed_ids})"
            )
    return valid, reasons


def are_all_cross_section_details_valid(
    xns: list[BeamXn], dims: list[list[float]], beam_list: list[list[int]]
):
    reasons = []
    valid = True
    if not isinstance(xns, list):
        valid = False
        reasons.append("The object supplied as list of cross-sections is not a list.")
    if not isinstance(dims, list):
        valid = False
        reasons.append("The object supplied as list of dimensions is not a list.")
    if not valid:
        return valid, reasons
    if len(xns) > len(beam_list):
        valid = False
        reasons.append(
            "More cross-section " "types have been provided than equivalent beams."
        )
    elif len(xns) < len(beam_list):
        valid = False
        reasons.append(
            "Fewer cross-section " "types have been provided than equivalent beams."
        )
    if len(dims) > len(beam_list):
        valid = False
        reasons.append("More dimension sets have been provided than equivalent beams.")
    elif len(dims) < len(beam_list):
        valid = False
        reasons.append("Fewer dimension sets have been provided than equivalent beams.")
    if len(xns) > len(dims):
        valid = False
        reasons.append(
            "More cross-section " "types have been provided than equivalent dimensions."
        )
    elif len(xns) < len(dims):
        valid = False
        reasons.append(
            "Fewer cross-section "
            "types have been provided than equivalent dimensions."
        )
    if valid:
        for xn, dims_ in zip(xns, dims):
            valid, new_reasons = are_cross_section_details_valid(xn, dims_)
            reasons.extend(new_reasons)
    return valid, reasons


def are_cross_section_details_valid(xn: BeamXn, dims: list[float]):
    valid = True
    reasons = []
    if not isinstance(xn, BeamXn):
        valid = False
        reasons.append(
            f"{xn} is not a valid cross-section. " f"Use a value of the BeamXn enum."
        )
    for dim in dims:
        if not isinstance(dim, float):
            valid = False
            reasons.append(f"dimensions must be floats. {dim} is not a float.")
        elif dim <= 0.0:
            valid = False
            reasons.append(f"All dimensions must be greater than 0., " f"not {dim}")

    if not valid:
        return valid, reasons
    if xn == BeamXn.CIRCLE:
        if len(dims) != 1:
            valid = False
            reasons.append(
                f"One dimension needs to be supplied for the "
                f"BeamXn.CIRCLE cross-section, not {dims}"
            )
    elif xn == BeamXn.CYLINDER:
        if len(dims) != 2:
            valid = False
            reasons.append(
                f"two dimensions are needed for the "
                f"BeamXn.CYLINDER cross-section, not {dims}"
            )
        elif dims[1] <= dims[0]:
            valid = False
            reasons.append(
                f"The BeamXn.CYLINDER dimensions must be supplied "
                f"in the "
                f"order of inner radius then outer radius. The "
                f"supplied inner radius is bigger than (or equal "
                f"to) the outer radius {dims}."
            )
    elif xn == BeamXn.RECTANGLE:
        if len(dims) != 2:
            valid = False
            reasons.append(
                f"two dimensions are needed for the "
                f"BeamXn.RECTANGLE cross-section, not {dims}"
            )
    elif xn == BeamXn.RECTANGLETUBE:
        if len(dims) != 6:
            valid = False
            reasons.append(
                f"six dimensions are needed for the "
                f"BeamXn.RECTANGLETUBE cross-section "
                f"(length width and 4 thicknesses), not {dims}"
            )
        else:
            if (dims[2] + dims[3]) >= dims[0]:
                valid = False
                reasons.append(
                    f"The width thicknesses of the BeamXn.RECTANGLETUBE"
                    f" cross-section combined are greater "
                    f"than the combined width of the cross-section."
                    f"{dims[2]} + {dims[3]} >= {dims[0]}"
                )
            if (dims[4] + dims[5]) >= dims[1]:
                valid = False
                reasons.append(
                    f"The width thicknesses of the BeamXn.RECTANGLETUBE"
                    f" cross-section combined are greater "
                    f"than the combined width of the cross-section."
                    f"{dims[4]} + {dims[5]} >= {dims[1]}"
                )

    if valid:
        physical, physicality_reasons = are_cross_section_dims_physical(xn, dims)
    else:
        physical = False
        physicality_reasons = []
    if not physical:
        valid = False
        reasons.extend(physicality_reasons)
    return valid, reasons


def are_cross_section_dims_physical(xn: BeamXn, dims: list[float]):
    reasons = []
    valid = True
    if xn in [BeamXn.CIRCLE, BeamXn.CYLINDER]:
        for dim in dims:
            if not (
                PHYSICAL_LIMITS.smallest * 0.5 <= dim <= PHYSICAL_LIMITS.largest * 0.5
            ):
                valid = False
                reasons.append(
                    f"Diameter {dim * 2} is not physical and is outside "
                    f"the bounds of the physical limits "
                    f"BuildyMcBuildFace can create: {PHYSICAL_LIMITS}"
                )
    else:
        for dim in dims:
            if not (PHYSICAL_LIMITS.smallest <= dim <= PHYSICAL_LIMITS.largest):
                valid = False
                reasons.append(
                    f"Dimension {dim} is not physical and is outside "
                    f"the bounds of the physical limits "
                    f"BuildyMcBuildFace can create: {PHYSICAL_LIMITS}"
                )
    if xn == BeamXn.CYLINDER:
        thickness = dims[1] - dims[0]
        if not (PHYSICAL_LIMITS.smallest <= thickness <= PHYSICAL_LIMITS.largest):
            valid = False
            reasons.append(
                f"Thickness {thickness} is not physical and is outside "
                f"the bounds of the physical limits "
                f"BuildyMcBuildFace can create: {PHYSICAL_LIMITS}"
            )

    return valid, reasons


@dataclass
class GraphNode:
    coordinate: Coordinate
    number: int
    edges: list[Coordinate]
    is_start: bool = False
    is_end: bool = False
    parent: Coordinate = None

    @classmethod
    def from_list(cls, node_list):
        number, x, y = node_list
        return cls(Coordinate(x, y), number, [], number == 1, number == 2)

    @property
    def horizontal_edges(self) -> list[Coordinate]:
        return [e for e in self.edges if e.y == self.coordinate.y]

    @property
    def vertical_edges(self) -> list[Coordinate]:
        return [e for e in self.edges if e.x == self.coordinate.x]


@dataclass
class Network:
    nodes: list[GraphNode]
    load_path: list[GraphNode]
    dimension: int = None

    @classmethod
    def from_attempt(
        cls,
        data: dict,
        start: list[int],
        end: list[int],
        rocks: list[list[int]],
        dimension: int,
    ):
        bridge_nodes = {n[0]: GraphNode.from_list(n) for n in data["nodes"]}
        rock_nodes = {n[0]: GraphNode.from_list(n) for n in rocks}
        nodes = {
            **bridge_nodes,
            **rock_nodes,
            1: GraphNode.from_list([1] + start),
            2: GraphNode.from_list([2] + end),
        }
        for beam in data["beams"]:
            n1_num, n2_num = beam
            node1 = nodes[n1_num]  # type: GraphNode
            node2 = nodes[n2_num]  # type: GraphNode
            if node2 not in node1.edges:
                node1.edges.append(node2.coordinate)
            if node1 not in node2.edges:
                node2.edges.append(node1.coordinate)
        load_path = [nodes[n] for n in data["load_path"]]
        return cls(list(nodes.values()), load_path, dimension=dimension)

    @property
    def start(self) -> GraphNode:
        return [n for n in self.nodes if n.is_start][0]

    @property
    def end(self) -> GraphNode:
        return [n for n in self.nodes if n.is_end][0]

    def are_nodes_on_grid(self) -> tuple[bool, list[GraphNode]]:
        limits = [-(self.dimension - 1) / 2, (self.dimension - 1) / 2]
        problem_nodes = []
        for node in self.nodes:
            if (
                not limits[0] <= node.coordinate.x <= limits[1]
                or not limits[0] <= node.coordinate.y <= limits[1]
            ):
                problem_nodes.append(node)
        return not bool(problem_nodes), problem_nodes

    def is_load_path_valid(
        self, rock_coords: list[Coordinate]
    ) -> tuple[bool, list[str]]:
        valid = True
        reasons = []
        nodes_on_path = {n.number for n in self.load_path}
        all_nodes = {n.number for n in self.nodes}
        if not nodes_on_path.issubset(all_nodes):
            valid = False
            reasons.append("load path contains nodes not in the network")
        if not self.load_path[0].is_start:
            valid = False
            reasons.append("first node is not the starting node")
        if not self.load_path[-1].is_end:
            valid = False
            reasons.append("last node is not the end node")
        for i in range(len(self.load_path) - 1):
            node_a = self.load_path[i]
            node_b = self.load_path[i + 1]
            if node_b.coordinate not in node_a.edges:
                valid = False
                reasons.append(
                    f"Node {node_a.number} is not connected " f"to {node_b.number}"
                )
            node_distance = calc_graph_node_distance(node_a, node_b)
            xdiff = node_b.coordinate.x - node_a.coordinate.x
            if xdiff == 0:
                valid = False
                reasons.append(
                    f"The step between node {node_a.number} and "
                    f"node {node_b.number} is vertical and "
                    f"not allowed"
                )
            if node_distance > MAX_EDGE_LENGTH:
                valid = False
                reasons.append(
                    f"node {node_a.number} and node {node_b.number} "
                    f"are too far apart ({node_distance:1.2f})"
                )
        for node in self.load_path:
            matched_rocks = [r for r in rock_coords if r == node.coordinate]
            if matched_rocks:
                valid = False
                reasons.append(
                    f"The load path must not touch any rocks. "
                    f"{node.coordinate} intersects with a rock"
                )
        return valid, reasons


def are_beams_valid(beams: list[list[int]]) -> tuple[bool, list[str]]:
    reasons = []
    valid = True
    for beam in beams:
        if not isinstance(beam, list):
            valid = False
            reasons.append(f"beam {beam} is not a list")
    if not valid:
        return valid, reasons
    for beam in beams:
        for val in beam:
            if not isinstance(val, int):
                valid = False
                reasons.append(f"beam {beam} contains a " f"non-int value {val}")
    return valid, reasons
