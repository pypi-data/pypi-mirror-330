from ansys.mapdl.core import launch_mapdl
import ansys.codefest.mapdl as acf


design = {
    "nodes": [],
    "beams": [],
    "load_path": [],
    "cross_section": [],
    "dimensions": [],
}
fixed_nodes = []


# start mapdl and clear it
mapdl = launch_mapdl()
mapdl.clear()  # optional as MAPDL just started
mapdl.units("SI")  # SI - International system (m, kg, s, K).
mapdl.prep7()

mapdl.antype("STATIC")
mapdl.et(1, "BEAM188")
mapdl.sectype(1, "BEAM", "CSOLID")
mapdl.secdata(design["dimensions"][0])


mapdl.mp("EX", 1, acf.STEEL.elastic_modulus)
mapdl.mp("PRXY", acf.STEEL.poissons_ratio)

for node in design["nodes"]:
    mapdl.n(node[0], node[1], node[2], 0)

# Note: We have to include 1, 2 and the rock nodes we want to use
for node in fixed_nodes:
    mapdl.n(node[0], node[1], node[2], 0)

beams = []
for beam in design["beams"]:
    beams.append(mapdl.e(beam[0], beam[1]))


mapdl.nplot(True, cpos="xy")
# constrain fixed nodes by removing their degrees of freedom
mapdl.nsel("ALL")
for n in fixed_nodes:
    mapdl.d(n[0], "ALL")

# Apply the 1 ton of force to each node
for node in design["load_path"]:
    mapdl.f(node, "FY", -9.81 * 1000.0)

mapdl.finish()
mapdl.run("/SOLU")
mapdl.solve()
mapdl.finish()
mapdl.post1()
mapdl.set("LAST")

for beam_num in beams:
    equiv = mapdl.get_value("secr", beam_num, "s", "eqv", "max")
    print(
        f"Beam Number: {beam_num} " f"experienced max equivalent stress of: {equiv} Pa"
    )

mapdl.finish()
# This command is arguably the most important!
# Make sure it gets called when you're done otherwise your
# MAPDL instances will hang forever!
mapdl.exit()
