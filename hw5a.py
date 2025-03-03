# hw5a.py

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def ff_colebrook(Re, rr, f_init=0.02):
    """
    Solve the Colebrook equation for friction factor f given:
       Re  : Reynolds number
       rr  : relative roughness (epsilon/d)
       f_init : initial guess for the solver (default=0.02)

    Returns
    -------
    float
        The friction factor (f) that solves the Colebrook equation:
          1 / sqrt(f) = -2.0 * log10( (rr/3.7) + 2.51/(Re * sqrt(f)) )
    Notes
    -----
    Uses scipy.optimize.fsolve for numerical root-finding.
    """

    def colebrook_eqn(f):
        return 1.0 / np.sqrt(f) + 2.0 * np.log10((rr / 3.7) + 2.51 / (Re * np.sqrt(f)))

    sol = fsolve(colebrook_eqn, f_init)
    return sol[0]


def ff_laminar(Re):
    """
    For laminar flow, friction factor f = 64 / Re

    Parameters
    ----------
    Re : float
        Reynolds number

    Returns
    -------
    float
        The laminar friction factor (64 / Re)
    """
    return 64.0 / Re


def ff(Re, rr, CBEQN=False):
    """
    Universal friction-factor function:
      if CBEQN=False => laminar formula => f = 64/Re
      if CBEQN=True  => Colebrook equation

    Parameters
    ----------
    Re : float
        Reynolds number
    rr : float
        Relative roughness (epsilon/d)
    CBEQN : bool
        If True, use Colebrook eqn; if False, use laminar eqn.

    Returns
    -------
    float
        The computed friction factor under the chosen flow model
    """
    if CBEQN:
        return ff_colebrook(Re, rr, f_init=0.02)
    else:
        return ff_laminar(Re)


def plotMoody(plotPoint=False, pt=(0, 0), marker='o'):
    """
    Produces a Moody diagram from Re ~ 600 to 1e8, covering:
      - laminar region (f=64/Re),
      - transition region (2000<Re<4000) -> also f=64/Re for a rough placeholder,
      - turbulent region (Colebrook eqn).
    Also loops over a set of relative roughness (rrVals) from 0 to ~0.05.
    Plots all these curves on a log-log plot of friction factor (f) vs. Re.

    Parameters
    ----------
    plotPoint : bool
        If True, highlight a specific point on the diagram.
    pt : tuple of floats, default=(0, 0)
        The (Re, f) coordinate for the point to plot, if plotPoint=True.
    marker : str, default='o'
        Matplotlib marker style for the highlighted point.

    Returns
    -------
    None
        Displays the generated plot via plt.show().
    """
    ReValsL = np.logspace(np.log10(600.0), np.log10(2000.0), 20)
    ReValsTrans = np.logspace(np.log10(2000.0), np.log10(4000.0), 20)
    ReValsCB = np.logspace(np.log10(4000.0), 8.0, 50)  # up to 1e8

    rrVals = np.array([
        0, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 2e-4, 4e-4, 6e-4, 8e-4,
        1e-3, 2e-3, 4e-3, 6e-3, 8e-3, 1.5e-2, 2e-2, 3e-2, 4e-2, 5e-2
    ])

    ffLam = np.array([ff_laminar(Re) for Re in ReValsL])
    ffTrans = np.array([ff_laminar(Re) for Re in ReValsTrans])

    ffCB = np.zeros((len(rrVals), len(ReValsCB)))
    for i, relR in enumerate(rrVals):
        f_guess = 0.02
        for j, Re in enumerate(ReValsCB):
            f_guess = ff_colebrook(Re, relR, f_init=f_guess)
            ffCB[i, j] = f_guess

    plt.figure(figsize=(8, 6))
    plt.loglog(ReValsL, ffLam, 'k-', label='Laminar (f=64/Re)')
    plt.loglog(ReValsTrans, ffTrans, 'k--', label='Transition')

    for i, relR in enumerate(rrVals):
        plt.loglog(ReValsCB, ffCB[i, :], color='k')
        x_annot = ReValsCB[-1]
        y_annot = ffCB[i, -1]
        plt.annotate(
            f"{relR:g}",
            xy=(x_annot, y_annot),
            xytext=(x_annot * 1.05, y_annot),
            fontsize=8,
            ha='left'
        )

    plt.xlim(600, 1e8)
    plt.ylim(0.008, 0.10)
    plt.xlabel(r"Reynolds number $Re = \rho\,V\,d / \mu$", fontsize=14)
    plt.ylabel(r"Friction factor $f$", fontsize=14)
    plt.text(2.5e8, 0.02, r"Relative roughness $\epsilon/d$", rotation=90, fontsize=12)

    ax = plt.gca()
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)
    ax.grid(which='both', linestyle='-', alpha=0.5)
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.3f"))

    if plotPoint:
        plt.plot(pt[0], pt[1], marker=marker, color='red', markersize=12, markeredgecolor='red', markerfacecolor='none')

    plt.legend(loc='best')
    plt.show()


def main():
    """
    Main driver function that, by default, calls plotMoody() with no point
    to generate and display the Moody diagram.
    """
    plotMoody()


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
