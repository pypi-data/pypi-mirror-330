__all__ = (
    "helloworld",
    "add",
    "linspace_2d",
    "reverse_vector",
    # 以下才是通用方法：line直线,curve曲线,plane平面,surface曲面
    "plot_2d_curve_parametric",
    "plot_3d_curve_parametric",
    "plot_3d_surface_z",
    "plot_3d_plane_dot2normal",
    "plot_3d_surface_z_with_curve",
    "plot_3d_curve_parametric_with_tangent",
    "example_plot_3d_curve_parametric_with_tangent",
    "example_plot_2d_curve_parametric",
    "example_plot_3d_curve_parametric",
    "example_plot_3d_plane_dot2normal",
    "example_plot_3d_surface_z",
    "example_plot_3d_surface_z_with_curve",
    "scatter_2d",
    "example_scatter_2d",
    # 线性回归相关
    "linreg_single_bgd",
    "linreg_single_normal_equation",
    "plot_linreg_single_bgd",
    "example_linreg_single_bgd",
    "example_plot_linreg_single_bgd",
    "example_linreg_single_normal_equation"
)

from rbutils.hello import helloworld
from rbutils.calc import add
from rbutils.plot import (
    plot_2d_curve_parametric,
    plot_3d_curve_parametric,
    plot_3d_surface_z,
    plot_3d_plane_dot2normal,
    plot_3d_surface_z_with_curve,
    plot_3d_curve_parametric_with_tangent,
    scatter_2d,
    example_scatter_2d,
    example_plot_3d_curve_parametric_with_tangent,
    example_plot_2d_curve_parametric,
    example_plot_3d_curve_parametric,
    example_plot_3d_plane_dot2normal,
    example_plot_3d_surface_z,
    example_plot_3d_surface_z_with_curve,
    plot_3d_curve_parametric_with_tangent_with_plane,
    example_plot_3d_curve_parametric_with_tangent_with_plane
)
from rbutils.rbnp import linspace_2d, reverse_vector
from rbutils.linreg import (
    linreg_single_bgd,
    linreg_single_normal_equation,
    plot_linreg_single_bgd,
    example_linreg_single_bgd,
    example_plot_linreg_single_bgd,
    example_linreg_single_normal_equation
)
