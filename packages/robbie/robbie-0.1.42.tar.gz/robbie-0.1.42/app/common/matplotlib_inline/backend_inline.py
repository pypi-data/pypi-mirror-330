"""A matplotlib backend for publishing figures via display_data"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the BSD 3-Clause License.
## Adapted fromt the matplotlib inline backend
## https://github.com/ipython/matplotlib-inline/blob/main/matplotlib_inline/backend_inline.py

import sys
import matplotlib
from matplotlib.backends import backend_agg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib._pylab_helpers import Gcf
from matplotlib.figure import Figure

import datetime
import time

def get_filestring(extension='png'):
    # Get current time with nanoseconds
    now = datetime.datetime.now()
    nanoseconds = time.time_ns() % 1000000000

    # Format the datetime string
    datetime_str = now.strftime('%Y-%m-%d_%H:%M:%S.%f')
    datetime_str_with_ns = f"{datetime_str}{nanoseconds:09d}"

    return datetime_str_with_ns + '.' + extension


def new_figure_manager(num, *args, FigureClass=Figure, **kwargs):
    """
    Return a new figure manager for a new figure instance.

    This function is part of the API expected by Matplotlib backends.
    """
    return new_figure_manager_given_figure(num, FigureClass(*args, **kwargs))


def new_figure_manager_given_figure(num, figure):
    """
    Return a new figure manager for a given figure instance.

    This function is part of the API expected by Matplotlib backends.
    """
    manager = backend_agg.new_figure_manager_given_figure(num, figure)

    # Hack: matplotlib FigureManager objects in interacive backends (at least
    # in some of them) monkeypatch the figure object and add a .show() method
    # to it.  This applies the same monkeypatch in order to support user code
    # that might expect `.show()` to be part of the official API of figure
    # objects.  For further reference:
    # https://github.com/ipython/ipython/issues/1612
    # https://github.com/matplotlib/matplotlib/issues/835

    # Override show to save the figure as a file
    figure.show = lambda *a: figure.savefig(get_filestring())

    # ensure current figure will be drawn, and each subsequent call
    # of draw_if_interactive() moves the active figure to ensure it is
    # drawn last
    try:
        show._to_draw.remove(figure)
    except ValueError:
        # ensure it only appears in the draw list once
        pass
    # Queue up the figure for drawing in next show() call
    show._to_draw.append(figure)
    show._draw_called = True

    return manager


def show(close=None, block=None):
    """Show all figures as SVG/PNG payloads.

    Parameters
    ----------
    close : bool, optional
        If true, a ``plt.close('all')`` call is automatically issued after
        sending all the figures. If this is set, the figures will entirely
        removed from the internal list of figures.
    block : Not used.
        The `block` parameter is a Matplotlib experimental parameter.
        We accept it in the function signature for compatibility with other
        backends.
    """
    try:
        for figure_manager in Gcf.get_all_fig_managers():
            if figure_manager.canvas.figure:
                figure_manager.canvas.figure.savefig(get_filestring())

    finally:
        show._to_draw = []
        # only call close('all') if any to close
        # close triggers gc.collect, which can be slow
        if close and Gcf.get_all_fig_managers():
            matplotlib.pyplot.close('all')


# This flag will be reset by draw_if_interactive when called
show._draw_called = False
# list of figures to draw when flush_figures is called
show._to_draw = []


def flush_figures():
    """Send all figures that changed

    This is meant to be called automatically and will call show() if, during
    prior code execution, there had been any calls to draw_if_interactive.

    This function is meant to be used as a post_execute callback in IPython,
    so user-caused errors are handled with showtraceback() instead of being
    allowed to raise.  If this function is not called from within IPython,
    then these exceptions will raise.
    """
    if not show._draw_called:
        return

    try:
        # exclude any figures that were closed:
        active = set([fm.canvas.figure for fm in Gcf.get_all_fig_managers()])
        for fig in [fig for fig in show._to_draw if fig in active]:
            try:
                fig.savefig(get_filestring())
            except Exception as e:
                print("Exception in callback %r: %s" % (fig, e), file=sys.stderr)
    finally:
        # clear flags for next round
        show._to_draw = []
        show._draw_called = False


# Changes to matplotlib in version 1.2 requires a mpl backend to supply a default
# figurecanvas. This is set here to a Agg canvas
# See https://github.com/matplotlib/matplotlib/pull/1125
FigureCanvas = FigureCanvasAgg
