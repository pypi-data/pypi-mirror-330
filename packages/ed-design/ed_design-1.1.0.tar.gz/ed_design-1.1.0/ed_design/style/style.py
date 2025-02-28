# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
# import ed_design as edd
from ed_design.logo.logo import logo
from ed_design.colors import Colors
import os
import platform
import pkg_resources
import numpy as np
import pandas as pd

# %%


def style(style: str = 'envidan', prop_cycle_palette: str = 'normal', cycle_repeat: int = 10) -> None:
    """
    Sets matplotlib style with relevant stylesheet file (mpl)

    Parameters
    ----------
    style : str, optional
        Style name. The default is 'envidan'.
    prop_cycle_palette : str, optional
        Color palette to use as default prop_cycle. The default is 'normal'.
    cycle_repeat : int, optional
        N times to repeat the color palette in case plot has need for more colors
        Matplotlib will revert to another palette if not enough colors

    Returns
    -------
    None.

    """

    # module_dir = os.path.dirname(__file__)

    if style == 'envidan':
        try:
            file_path = pkg_resources.resource_filename(
                __name__, '/envidan.mplstyle')
            plt.style.use(file_path)
            prop_cycle(prop_cycle_palette, cycle_repeat)
        except FileNotFoundError:
            print(
                "The 'envidan.mplstyle' file was not found. Check your package structure.")

    if style == 'default':
        plt.style.use('default')

    # TODO Include Segoe UI font int his somehow
    return None


def prop_cycle(palette: str = 'normal', cycle_repeat: int = 10) -> None:
    """
    Sets the color prop_cycle in Matplotlib. The palette name must be a valid
    palette from ed_design.Colors().get_palette(palette)

    Parameters
    ----------
    palette : str, optional
        Color prop cycle name. The default is 'normal'.
    cycle_repeat : int, optional
        N times to repeat the color palette in case plot has need for more colors
        Matplotlib will revert to another palette if not enough colors

    Returns
    -------
    None.

    """
    colors = Colors()
    prop_cycle_palette = colors.get_palette(palette) * cycle_repeat
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=prop_cycle_palette)
    return None


def font_check(font_name: str = None) -> None:
    """
    Checks for system installed fonts Sathoshi and Segoe UI.
    Can also check for any other font name.

    Parameters
    ----------
    font_name : str, optional
        Font name to check for. The default is None.

    Returns
    -------
    None.

    """
    available_fonts = fm.findSystemFonts(fontpaths=None, fontext='otf')

    font_names_satoshi = [
        'Satoshi-Regular',
        'Satoshi-Black',
        'Satoshi-BlackItalic',
        'Satoshi-Bold',
        'Satoshi-BoldItalic',
        'Satoshi-Italic',
        'Satoshi-Light',
        'Satoshi-LightItalic',
        'Satoshi-Medium',
        'Satoshi-MediumItalic',
    ]

    font_names_segoe_ui = [
        'Segoe UI Bold Italic',
        'Segoe UI Bold',
        'Segoe UI Italic',
        'Segoe UI',
    ]

    if font_name is None:
        satoshi_lst = []
        for font in font_names_satoshi:
            if not any(font in font_path for font_path in available_fonts):
                satoshi_lst.append(font)
        if len(satoshi_lst) == 0:
            pass
        else:
            print(
                f'The fonts {satoshi_lst}" are not present on your system. Please install them from the path ed_design/style/_fonts/_satoshi')

        # The Segoe UI font messes up Maconomy so dont install this font !!
        # segoe_ui_lst = []
        # for font in font_names_segoe_ui:
        #     if not any(font in font_path for font_path in available_fonts):
        #         segoe_ui_lst.append(font)
        # if len(segoe_ui_lst) == 0:
        #     pass
        # else:
        #     print(f'The fonts {segoe_ui_lst}" are not present on your system. Please install them from the path ed_design/style/_fonts/_segoe_ui')

    if font_name is not None:
        if not any(font_name in font_path for font_path in available_fonts):
            print(f'The "{font_name}" font is not present on your system')
    return


def generate_example_data(seed=42, num_points=100, num_clusters=5):
    """
    Generate 5 types of datasets, each containing 5 variations within a single DataFrame.
    The 'x' column is set as the index for easier plotting.

    Parameters
    ----------
    seed : int, optional
        Random seed for reproducibility. Default is 42.
    num_points : int, optional
        Number of data points per dataset. Default is 100.
    num_clusters : int, optional
        Number of clusters per dataset type (for cluster datasets). Default is 5.

    Returns
    -------
    dict
        A dictionary containing the datasets: "linear", "quadratic", "sinusoidal", "clusters", and "time_series".
    """
    np.random.seed(seed)
    datasets = {"linear": None, "quadratic": None, "sinusoidal": None, "clusters": None, "time_series": None}

    # 1. Linear dataset with different slopes and noise levels
    linear_data = []
    x = np.linspace(0, 10, num_points)  # Common x for all linear datasets
    for i in range(5):
        y = (i + 1) * x + np.random.normal(scale=2 + i, size=num_points)  # Increasing slope & noise
        linear_data.append(pd.DataFrame({f'y_{i+1}': y}))
    datasets["linear"] = pd.DataFrame({'x': x}).join(pd.concat(linear_data, axis=1)).set_index('x')

    # 2. Quadratic dataset with different coefficients and noise levels
    quadratic_data = []
    x = np.linspace(-5, 5, num_points)  # Common x for all quadratic datasets
    for i in range(5):
        y = (i + 1) * x**2 + np.random.normal(scale=2 + i, size=num_points)  # Increasing coefficient & noise
        quadratic_data.append(pd.DataFrame({f'y_{i+1}': y}))
    datasets["quadratic"] = pd.DataFrame({'x': x}).join(pd.concat(quadratic_data, axis=1)).set_index('x')

    # 3. Sinusoidal dataset with different amplitudes, frequencies, and phase shifts (same x)
    sinusoidal_data = []
    x_sin = np.linspace(0, 4 * np.pi, num_points)  # Same x for all sinusoidal waves
    for i in range(5):
        y = (i + 1) * np.sin((i + 1) * x_sin + (i * np.pi / 6)) + np.random.normal(scale=0.2, size=num_points)
        sinusoidal_data.append(pd.DataFrame({f'y_{i+1}': y}))
    datasets["sinusoidal"] = pd.DataFrame({'x': x_sin}).join(pd.concat(sinusoidal_data, axis=1)).set_index('x')

    # 4. Cluster dataset with 5 distinct clusters (A, B, C, D, E)
    cluster_data = []
    cluster_labels = ['A', 'B', 'C', 'D', 'E']
    x_all, y_all, labels_all = [], [], []
    for i in range(num_clusters):
        for j, label in enumerate(cluster_labels):
            cluster = np.random.normal(loc=[(i + 1) * 2 + j, (i + 1) * 2 + j], scale=0.8 + i * 0.2, size=(20, 2))
            x, y = cluster.T
            x_all.extend(x)
            y_all.extend(y)
            labels_all.extend([label] * 20)

    datasets["clusters"] = pd.DataFrame({'x': x_all, 'y': y_all, 'cluster': labels_all}).set_index('x')

    # 5. Time series dataset with different trends and noise levels
    time_series_data = []
    x_time = np.arange(num_points)
    for i in range(5):
        values = np.cumsum(np.random.normal(scale=1 + i * 0.5, size=num_points)) + (0.5 + i * 0.2) * x_time
        time_series_data.append(pd.DataFrame({f'value_{i+1}': values}))
    datasets["time_series"] = pd.DataFrame({'time': x_time}).join(pd.concat(time_series_data, axis=1)).set_index('time')

    # 6. bar plot datta
    datasets["barplot"] = pd.DataFrame(np.random.randint(0, 100, size=(100, 8)), columns=list('ABCDEFGH'))

    return datasets


def color_showcase():
    """
    Opens a specific PDF file located in the code base using the default PDF viewer.

    The PDF file is located in a fixed, predefined relative path in the codebase.

    Returns
    -------
    None

    Example
    -------
    ```python
    open_pdf_from_codebase()
    ```
    """
    # Define the relative path to the PDF file from the root of the package
    # You can change this path as per your actual file location in the codebase
    file_name = 'ed_design/style/Envidan_Color_showcase_010722.pdf'  # Example path to the PDF file

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'Envidan_Color_showcase_010722.pdf')

    # Ensure the file exists before trying to open it
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_name}' does not exist in the codebase.")
        return

    # Check the platform to determine the appropriate command
    system = platform.system()

    if system == 'Darwin':  # macOS
        os.system(f'open "{file_path}"')
    elif system == 'Windows':  # Windows
        os.system(f'start "" "{file_path}"')
    elif system == 'Linux':  # Linux
        os.system(f'xdg-open "{file_path}"')
    else:
        print(f"Unsupported OS: {system}. Could not open the file.")
