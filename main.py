from sympy.physics.continuum_mechanics.beam import Beam
from sympy import *
from sympy.plotting import plot, PlotGrid
import matplotlib.pyplot as plt

# https://docs.sympy.org/latest/modules/physics/continuum_mechanics/beam_problems.html#example-7

def beam_me_up(rxn, __L, __E, __I, __F, color):

    ## sign convention
    # upward forces and clockwise moment are positive

    # symbols
    L = symbols('L', positive=True)
    E, I, F = symbols('E I F')

    ## definition

    # beam
    b = Beam(L, E, I)

    if rxn == 'fixed-fixed':

        # beam reactions
        R1, R2 = symbols('R1  R2')
        M1, M2 = symbols('M1, M2')
        b.apply_load(R1, 0, -1)
        b.apply_load(M1, 0, -2)
        b.apply_load(R2, L, -1)
        b.apply_load(M2, L, -2)

        # beam load
        b.apply_load(-F, L / 2, -1)

        # beam boundary conditions
        b.bc_deflection = [(0, 0), (L, 0)]
        b.bc_slope = [(0, 0), (L, 0)]

        # solve
        b.solve_for_reaction_loads(R1, R2, M1, M2)

    elif rxn == 'simple-simple':

        # beam reactions
        R1, R2 = symbols('R1  R2')
        b.apply_load(R1, 0, -1)
        b.apply_load(R2, L, -1)

        # beam load
        b.apply_load(-F, L / 2, -1)

        # beam boundary conditions
        b.bc_deflection = [(0, 0), (L, 0)]

        # solve
        b.solve_for_reaction_loads(R1, R2)

    else :
        print("No command defined!")

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
    #ax0 = b.plot_loading_results(subs={L: __L, E: __E, I: __I, F: __F})
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

    # extracting sympy plot data from beam.py for plotting outside of this function
    ax1 = plot(b.shear_force().subs({L: __L, E: __E, I: __I, F: __F}), (b.variable, 0, __L),
               title="Shear Force", line_color=color, xlabel=r'$\mathrm{x}$', ylabel=r'$\mathrm{V\quad(lb)}$', show=False)
    ax2 = plot(b.bending_moment().subs({L: __L, E: __E, I: __I, F: __F}), (b.variable, 0, __L),
               title="Bending Moment", line_color=color, xlabel=r'$\mathrm{x}$', ylabel=r'$\mathrm{M\quad(lb \cdot in)}$', show=False)
    ax3 = plot(b.slope().subs({L: __L, E: __E, I: __I, F: __F}), (b.variable, 0, __L),
               title="Slope", line_color=color, xlabel=r'$\mathrm{x}$', ylabel=r'$\theta$', show=False)
    ax4 = plot(b.deflection().subs({L: __L, E: __E, I: __I, F: __F}), (b.variable, 0, __L),
               title="Deflection", line_color=color, xlabel=r'$\mathrm{x}$', ylabel=r'$\delta\quad(in)$', show=False)

    return ax1, ax2, ax3, ax4

# https://stackoverflow.com/q/63483960
def move_sympyplot_to_axes(p, ax):
    # move axes
    backend = p.backend(p)
    backend.ax = ax
    backend._process_series(backend.parent._series, ax, backend.parent)
    # remove top and right spines
    backend.ax.spines['top'].set_color('none')
    backend.ax.spines['right'].set_color('none')
    # move left and bottom spine to left and bottom of axis extents, previously 'bottom' was set to 'zero'
    backend.ax.spines['left'].set_position(('axes', 0))
    backend.ax.spines['bottom'].set_position(('axes', 0))
    # correct ylabel position, align vertically to center
    ax.yaxis.set_label_coords(-0.1, 0.5)
    plt.close(backend.fig)

## MAIN

beam = {
        "L": {
            "Name": "Length",
            "Value": 120,
            "Unit": "in"
        },
        "Ix": {
            "Name": "Moment of Inertia",
            "Value": [6.04, 8.6, 12.83],
            "Unit": "in4"
        },
        "E": {
            "Name": "Modulus of Elasticity",
            "Material": ["Aluminum", "Steel"],
            "Value": [9900E3, 2.901E7],
            "Unit": "lb/in2"
        },
        "F": {
            "Name": "Point Loads",
            "Value": [2120, 2200],
            "Unit": "lb"
        },
        "RXN": {
            "Name": "Reaction",
            "Value": ["fixed-fixed", "simple-simple"]
        }
}

for i, E in enumerate(beam['E']['Value']):

    MATERIAL = beam['E']['Material'][i]
    L = beam['L']['Value']
    F = beam['F']['Value'][i]

    for j, RXN in enumerate(beam['RXN']['Value']):

        Ix = beam['Ix']['Value']
        colors = ['red', 'blue', 'green']
        p = []

        title = f'Material = {MATERIAL}, Constraints = {RXN}'
        print(title)
        for k, I in enumerate(Ix):

            obj = beam_me_up(RXN, L, E, I, F, colors[k])
            p.append(obj)

            # https://www.spanco.com/blog/understanding-overhead-crane-deflection-and-criteria/
            # I think I could've used the b.max_deflection() formula with subs, but screw it!
            if RXN == 'fixed-fixed':
                delta = (F * L**3) / (192 * E * I)
            elif RXN == 'simple-simple':
                delta = (F * L ** 3) / (48 * E * I)
            allowable = L/450
            passed = False
            if delta < allowable:
                passed = True

            if k == 0:
                print(f'| Ix | &delta;<sub>max</sub> | &delta;<sub>allowable</sub> | Pass |')
                print(f'|----|-----------------------|-----------------------------|------|')

            print(f'| {I:10.2f} | {delta:10.2f} | {allowable:10.2f} | {passed} |')

        # matplotlib overlplotting
        fig, axes = plt.subplots(nrows=4)
        dpi = fig.get_dpi()
        fig.set_size_inches(800.0 / float(dpi), 600.0 / float(dpi))

        for P in p:
            move_sympyplot_to_axes(P[0], axes[0])
            move_sympyplot_to_axes(P[1], axes[1])
            move_sympyplot_to_axes(P[2], axes[2])
            move_sympyplot_to_axes(P[3], axes[3])

        # requirement
        axes[3].axhline(-allowable, linestyle='-', linewidth='1.0', color='magenta', zorder=0)

        # grid/limits/labels
        for ax in axes:
            ax.set_axisbelow(True)
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
            ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
            ax.set_xlim([0, L])
            #ylabel = ax.yaxis.get_label()
            #ylabel.set_verticalalignment('center')

        # legend
        handles = axes[0].get_legend_handles_labels()[0]  # return first value of function with [0]
        labels = [str(Ix) for Ix in Ix]  # convert list of floats to list of strings
        axes[0].legend(handles, labels, loc='right', title='Moment of Inertia (Ix)', ncol=3)

        # voila
        fig.tight_layout()
        fig.suptitle(title, fontsize=10, x=0.5, y=0.05, color='gray')
        filename = f'./img/result_{MATERIAL.lower()}_{RXN}.png'
        fig.savefig(filename, dpi=100)
        plt.show()
