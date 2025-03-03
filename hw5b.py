# region imports
import hw5a as pta
import random as rnd
from matplotlib import pyplot as plt


# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2000 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """
    if Re >= 4000:
        return pta.ff_colebrook(Re, rr, f_init=0.02)
    if Re <= 2000:
        return pta.ff_laminar(Re)

    # Prediction of Colebrook Equation in Transition region
    CBff = pta.ff_colebrook(Re, rr, f_init=0.02)
    # Prediction of Laminar Equation in Transition region
    Lamff = pta.ff_laminar(Re)

    mean = (CBff + Lamff) / 2
    sig = 0.2 * mean
    return rnd.normalvariate(mean, sig)  # Use normalvariate to select a number randomly from a normal distribution


def PlotPoint(Re, f):
    """
        Plots the user-specified point (Re, f) on the existing Moody chart.

        If the flow is transitional (2000 < Re < 4000), the point is plotted
        with a triangular marker ('^'). Otherwise (laminar or turbulent),
        the point is plotted with a circular marker ('o').

        :param Re: the Reynolds number at which to plot the point (float)
        :param f: the friction factor value to plot (float)
        :return: None
        """
    # Determine marker style based on Reynolds number
    if 2000 < Re < 4000:
        marker = '^'  # Upwards-pointing triangle for transition flow
    else:
        marker = 'o'  # Circle for laminar or turbulent flow

    # Plot Moody chart and highlight the point with the appropriate marker
    pta.plotMoody(plotPoint=True, pt=(Re, f), marker=marker)


def main():
    """
        Main driver function that repeatedly prompts the user for:
          - Reynolds number (Re),
          - Relative roughness (rr),
          - Pipe diameter in inches (di).

        It then computes the friction factor via ffPoint(Re, rr) and calls PlotPoint
        to display the result on the Moody chart. The user can repeat this process
        multiple times until they choose to stop.

        :return: None
        """
    while True:
        Re = float(input("Enter the Reynolds number: "))
        rr = float(input("Enter the relative roughness: "))
        di = float(input("Enter the pipe diameter in inches: "))
        f = ffPoint(Re, rr)
        print(f"Friction factor = {f:.5f}")
        PlotPoint(Re, f)

        # Ask the user if they want to re-specify the parameters
        repeat = input("Do you want to re-specify the parameters? (yes/no): ").strip().lower()
        if repeat != 'yes':
            break


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
