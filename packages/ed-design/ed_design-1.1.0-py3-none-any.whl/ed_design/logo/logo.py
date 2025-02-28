# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import matplotlib.figure
import matplotlib.axes
import numpy as np

# %%


def logo(kind: str = 'print') -> np.ndarray:
    """
    Load Envidan logo for use in for example a Matplotlib figure

    Use:
        Put logon in Matplotlib figures by adding an axes.

        logo = logo()
        ax_logo = fig.add_axes([0.80,0.94,0.16,0.20], anchor='NE', zorder=-1)
        ax_logo.imshow(logo)
        ax_logo.axis('off')

    Parameters
    ----------
    kind : str, optional
        Kind of logo to load. Options are "print" and "web". The default is 'print'.

    Returns
    -------
    logo : Array of uint8
        Array of uint8 number representing the image.

    """

    module_dir = os.path.dirname(__file__)

    if kind == 'print':
        file_path = os.path.join(module_dir, 'ed_logo_blue_print.jpg')
        logo = plt.imread(file_path)
    elif kind == 'web':
        file_path = os.path.join(module_dir, 'ed_logo_blue_web.png')
        logo = plt.imread(file_path)
    else:
        raise ValueError(f'{kind} is unknown for logo type. Use "print" or "web"')
    return logo


def logo2fig(fig_or_ax: matplotlib.figure.Figure | matplotlib.axes.Axes,  # Type hint for figure or axes
             logo_kind: str = 'print',
             x_position: float = 0.87,
             y_position: float = 0.87,
             width: float = 0.13,
             height: float = 0.10,
             zorder: int = 100) -> matplotlib.figure.Figure:  # Return type is a Figure
    """
    Add the Envidan logo to a Matplotlib figure or axes.

    This function places the Envidan logo on an existing Matplotlib figure or axes by
    adding an additional axes in a specified position. The logo can be loaded in different formats
    (print or web), and its position and size within the figure can be adjusted.

    Parameters
    ----------
    fig_or_ax : matplotlib.figure.Figure or matplotlib.axes.Axes
        The Matplotlib figure or axes to which the logo will be added.
    logo_kind : str, optional
        The type of logo to load. Options are:
        - 'print' : High-quality logo for printing.
        - 'web'   : Optimized logo for web use.
        The default is 'print'.
    x_position : float, optional
        The x-coordinate of the bottom-left corner of the logo in figure-relative
        coordinates (0 to 1). Higher values move the logo further to the right.
        Default is 0.92.
    y_position : float, optional
        The y-coordinate of the bottom-left corner of the logo in figure-relative
        coordinates (0 to 1). Higher values move the logo further up.
        Default is 0.87.
    width : float, optional
        The width of the logo as a fraction of the figure width.
        Default is 0.08 (8% of the figure width).
    height : float, optional
        The height of the logo as a fraction of the figure height.
        Default is 0.10 (10% of the figure height).
    zorder : integer, optional
        Controls the stacking order of the logo within the figure. Elements with higher
        `zorder` values are drawn on top of elements with lower values. This parameter
        determines which layer the logo appears on relative to other elements in the plot.
        Default is 0, meaning the logo will be drawn behind most plot elements.
        Default is 100 (on the top).

    Returns
    -------
    fig_or_ax : matplotlib.figure.Figure or matplotlib.axes.Axes
        The modified Matplotlib figure or axes with the Envidan logo added.

    Raises
    ------
    ValueError
        If an invalid Matplotlin figure or axes object is provided.

    Example
    -------
    ```python
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    fig = logo2fig(fig, logo_kind='web', x_position=0.85, y_position=0.90, width=0.10, height=0.12)
    plt.show()
    ```

    """
    # Load the Envidan logo
    ed_logo = logo(kind=logo_kind)

    if isinstance(fig_or_ax, plt.Axes):  # If an axes object is passed
        ax = fig_or_ax
        ax_logo = ax.figure.add_axes([x_position, y_position, width, height], zorder=zorder)
        ax_logo.imshow(ed_logo)
        ax_logo.axis('off')
    elif isinstance(fig_or_ax, plt.Figure):  # If a figure object is passed
        fig = fig_or_ax
        ax_logo = fig.add_axes([x_position, y_position, width, height], zorder=zorder)
        ax_logo.imshow(ed_logo)
        ax_logo.axis('off')
    else:
        raise ValueError("The input must be a Matplotlib figure or axes object.")

    return fig_or_ax
