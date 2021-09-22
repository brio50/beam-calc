from sympy.physics.continuum_mechanics.beam import Beam
from sympy import *

# https://docs.sympy.org/latest/modules/physics/continuum_mechanics/beam_problems.html#example-7

def beam_me_up(__L, __E, __I, __F):

    ## sign convention
    # upward forces and clockwise moment are positive

    # symbols
    L = symbols('L', positive=True)
    E, I, F = symbols('E I F')

    ## beam definition
    b = Beam(L, E, I)

    # reactions
    R1, R2 = symbols('R1  R2')
    M1, M2 = symbols('M1, M2')
    b.apply_load(R1, 0, -1)
    b.apply_load(M1, 0, -2)
    b.apply_load(R2, L, -1)
    b.apply_load(M2, L, -2)

    # beam load
    b.apply_load(-F, L/2, -1)

    # boundary conditions
    b.bc_deflection = [(0, 0), (L, 0)]
    b.bc_slope = [(0, 0), (L, 0)]

    ## solve
    b.solve_for_reaction_loads(R1, R2, M1, M2)

    # print results
    print('Reaction Loads:')
    pprint(b.reaction_loads)
    print('Load:')
    pprint(b.load)
    print('Max Deflection:')
    pprint(b.max_deflection())

    ## plotting

    # free body diagram
    # https: // docs.sympy.org / latest / modules / physics / continuum_mechanics / beam.html  # sympy.physics.continuum_mechanics.beam.Beam.draw
    # **Note:**: load F will not be rendered correctly if < -1, therefore use subs to make shear, bending, and moment diagrams
    #fbd = b.draw()
    #fbd.show()

    # shear, slope, moment, deflection
    b.plot_loading_results(subs={L: __L, E: __E, I: __I, F: __F})
    #ax1 = b.plot_shear_force()
    #ax2 = b.plot_slope()
    #ax3 = b.plot_bending_moment()
    #ax4 = b.plot_deflection()

    # how to access via backend
    # https://newbedev.com/display-two-sympy-plots-as-two-matplotlib-subplots
    #fig = ax0._backend.fig
    #ax0._backend = ax0.backend(ax0)
    #ax0._backend.process_series()
    #ax0._backend.ax[0].scatter([0, 60, 120], [0, 0, 0], marker='x', color='r')

    #ax.style.available
    #ax.backend
    #print(ax0.backend.__dict__)

    # doesnt work?
    #breakpoint()


L = 10*12 #in
E = 9900E3 #lb/in2
Ix = [6.04, 8.37] #in4
F = 2000 #lb
x = 3  # L/<value>

for i, I in enumerate(Ix):
    beam_me_up(L, E, I, F)