from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("openmc_depletion_plotter")
except PackageNotFoundError:
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root="..", relative_to=__file__)
    except ImportError:
        __version__ = "unknown"

__all__ = ["__version__"]

from .utils import get_atoms_activity_from_material
from .utils import find_most_abundant_nuclides_in_material
from .utils import find_most_abundant_nuclides_in_materials
from .utils import get_nuclide_atoms_from_materials
from .utils import find_most_active_nuclides_in_material
from .utils import find_most_active_nuclides_in_materials
from .utils import get_nuclide_activities_from_materials
from .utils import get_decay_heat_from_materials
from .utils import get_atoms_from_material
from .utils import create_base_plot
from .utils import add_stables
from .utils import update_axis_range_partial_chart
from .utils import update_axis_range_full_chart
from .utils import add_scale_buttons

from .materials import plot_isotope_chart_of_atoms, plot_isotope_chart_of_activity
from .integrators import plot_pulse_schedule
from .results import plot_activity_vs_time, plot_atoms_vs_time, plot_decay_heat_vs_time
