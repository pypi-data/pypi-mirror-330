from ansys.mapdl.core import launch_mapdl
import ansys.codefest.mapdl as acf


# start mapdl and clear it
mapdl = launch_mapdl()
mapdl.clear()  # optional as MAPDL just started
mapdl.units("SI")  # SI - International system (m, kg, s, K).
mapdl.prep7()
mapdl.antype("STATIC")
mapdl.et(1, "BEAM188")
mapdl.sectype(1, "BEAM", "CSOLID")
mapdl.secdata(0.01)

mapdl.n(1, 0, 0, 0)
mapdl.n(2, 1, 0, 0)
mapdl.n(3, 2, 0, 0)
beams = [mapdl.e(1, 2), mapdl.e(2, 3)]

mapdl.mp("EX", 1, acf.STEEL.elastic_modulus)
mapdl.mp("PRXY", 1, acf.STEEL.poissons_ratio)
mapdl.mp("DENS", 1, acf.STEEL.density)

# nplot, eplot, etc are all ways of visualising your setup
# mapdl.nplot(True,cpos='xy')

# constrain fixed nodes by removing their degrees of freedom
mapdl.nsel("ALL")
mapdl.d(1, "ALL")
mapdl.d(3, "ALL")


# Or you can constrain individual degrees of freedom
# mapdl.d(1, 'UX', 0)
# mapdl.d(1, 'UY', 0)
# mapdl.d(1, 'UZ', 0)
# mapdl.d(1, 'ROTX', 0)
# mapdl.d(1, 'ROTY', 0)
# mapdl.d(1, 'ROTZ', 0)
#
# mapdl.d(3, 'UX', 0)
# mapdl.d(3, 'UY', 0)
# mapdl.d(3, 'UZ', 0)
# mapdl.d(3, 'ROTX', 0)
# mapdl.d(3, 'ROTY', 0)
# mapdl.d(3, 'ROTZ', 0)


# Apply the 1 ton of force to node 2
mapdl.f(2, "FY", -9.81 * 1000.0)

# Turn on gravity
mapdl.acel(acel_y=9.81)
mapdl.finish()

# run solution
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
