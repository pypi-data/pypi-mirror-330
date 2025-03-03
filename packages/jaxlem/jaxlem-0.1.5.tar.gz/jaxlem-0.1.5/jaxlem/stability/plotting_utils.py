import numpy as np
from jaxtyping import Array, Int, Float, Bool
from typing import Union, Tuple, Optional, Type
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


FAILURE_PARAMS_TYPE = Union[
    Int[Array, "n_x_points*n_z_points*n_radius 3"],
    Float[Array, "n_x_points*n_z_points*n_radius 3"]
]


def viz(model, failure_circle: FAILURE_PARAMS_TYPE, fos_all: Float[Array, "n_circles"], filename: str) -> None:
    fos_all = np.asarray([fos_all]).squeeze()

    single_circle = np.equal(fos_all.size, 1)

    if single_circle: fos_all = np.asarray([fos_all])
    if single_circle: failure_circle = np.expand_dims(failure_circle, 0)

    if not single_circle:
        idx = np.where(fos_all < 5)[0]
        failure_circle = failure_circle[idx]
        fos_all = fos_all[idx]

        norm = matplotlib.colors.Normalize(vmin=float(fos_all.min()), vmax=float(fos_all.max()))
        cmap = matplotlib.cm.rainbow_r
        sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)

    fig = plt.figure(figsize=(12, 8))
    plt.plot([0, model.config.crest_length], [model.config.slope_height, model.config.slope_height],
             color='k', linewidth=2)
    plt.plot([model.config.crest_length, model.config.crest_length + model.config.slope_length],
             [model.config.slope_height, 0], color='k', linewidth=2)
    plt.axhline(0, color='k', linewidth=2)
    plt.axhline(-model.config.clay_thickness, color='k', linewidth=2)

    if not single_circle:
        for i, (circle, fos) in enumerate(zip(failure_circle, fos_all)):

            x_center, z_center, radius = model._unpack_failure_circle(circle)

            intersection_points, intersects = model._intersection_points(circle)
            if not intersects:
                continue

            x_circle = np.linspace(intersection_points[:, 0].min(), intersection_points[:, 0].max(), 100)
            z_circle = z_center - np.sqrt((radius ** 2 - (x_circle - x_center) ** 2))

            plt.scatter(circle[0], circle[1], marker='x', color=sm.to_rgba(fos), s=40)
            plt.plot(x_circle, z_circle, color=sm.to_rgba(fos), linewidth=0.5)
            plt.plot([x_circle.min(), x_center], [z_circle[0], z_center], color=sm.to_rgba(fos), linewidth=0.5)
            plt.plot([x_circle.max(), x_center], [z_circle[-1], z_center], color=sm.to_rgba(fos), linewidth=0.5)

    fos = fos_all.min()
    circle_min = failure_circle[fos_all.argmin()]
    x_center, z_center, radius = model._unpack_failure_circle(circle_min)
    intersection_points, intersects = model._intersection_points(circle_min)
    x_circle = np.linspace(intersection_points[:, 0].min(), intersection_points[:, 0].max(), 100)
    z_circle = z_center - np.sqrt((radius ** 2 - (x_circle - x_center) ** 2))

    plt.scatter(circle_min[0], circle_min[1], marker='x', color='r', s=40)
    plt.plot(x_circle, z_circle, color='r', linewidth=2, label='Critical plane\nFoS={fos:.3f}'.format(fos=fos))
    plt.plot([x_circle.min(), x_center], [z_circle[0], z_center], color='r', linewidth=2)
    plt.plot([x_circle.max(), x_center], [z_circle[-1], z_center], color='r', linewidth=2)

    rect = patches.Rectangle((min(model.config.failure_box.x_lims), min(model.config.failure_box.z_lims)),
                             max(model.config.failure_box.x_lims) - min(model.config.failure_box.x_lims),
                             max(model.config.failure_box.z_lims) - min(model.config.failure_box.z_lims),
                             linewidth=1, edgecolor='b', facecolor='b', alpha=0.3)
    plt.gca().add_patch(rect)

    plt.xlim(0, model.config.total_length)
    plt.ylim(-model.config.clay_thickness, model.config.failure_box.z_coords.max() + 5)
    plt.xlabel('X coordinate [m]', fontsize=16)
    plt.ylabel('Y coordinate [m]', fontsize=16)
    plt.legend(fontsize=14)

    if not single_circle:
        sub_ax = plt.axes([0.92, 0.2, 0.01, 0.6])
        cbar = plt.colorbar(sm, cax=sub_ax)
        cbar.ax.get_yaxis().labelpad = 15
        cbar.ax.set_ylabel('FoS [-]', fontsize=16)

    fig.savefig(filename)


def viz_form(model, failure_circle: FAILURE_PARAMS_TYPE, fos: Float[Array, "n_circles"],
           rf: Float[Array, "n_cells_rf"], beta: Bool[Array, "n_cells_rf"], filename: Optional[str] = None)\
        -> plt.Figure:

    fig = plt.figure(figsize=(12, 8))
    plt.plot([0, model.config.crest_length], [model.config.slope_height, model.config.slope_height],
             color='k', linewidth=2)
    plt.plot([model.config.crest_length, model.config.crest_length + model.config.slope_length],
             [model.config.slope_height, 0], color='k', linewidth=2)
    plt.axhline(0, color='k', linewidth=2)
    plt.axhline(-model.config.clay_thickness, color='k', linewidth=2)

    x_center, z_center, radius = model._unpack_failure_circle(failure_circle)
    intersection_points, intersects = model._intersection_points(failure_circle)
    x_circle = np.linspace(intersection_points[:, 0].min(), intersection_points[:, 0].max(), 100)
    z_circle = z_center - np.sqrt((radius ** 2 - (x_circle - x_center) ** 2))

    plt.scatter(failure_circle[0], failure_circle[1], marker='x', color='r', s=40)
    plt.plot(x_circle, z_circle, color='r', linewidth=2, label='Critical plane\nFoS={fos:.3f}'.format(fos=fos))
    plt.plot([x_circle.min(), x_center], [z_circle[0], z_center], color='r', linewidth=2)
    plt.plot([x_circle.max(), x_center], [z_circle[-1], z_center], color='r', linewidth=2)

    rect = patches.Rectangle((min(model.config.failure_box.x_lims), min(model.config.failure_box.z_lims)),
                             max(model.config.failure_box.x_lims) - min(model.config.failure_box.x_lims),
                             max(model.config.failure_box.z_lims) - min(model.config.failure_box.z_lims),
                             linewidth=1, edgecolor='b', facecolor='b', alpha=0.3)
    plt.gca().add_patch(rect)

    plt.xlim(0, model.config.total_length)
    plt.ylim(-model.config.clay_thickness, model.config.failure_box.z_coords.max() + 5)
    plt.xlabel('X coordinate [m]', fontsize=16)
    plt.ylabel('Y coordinate [m]', fontsize=16)
    plt.legend(fontsize=14)

    X = np.asarray(model.config.rf_coords.mesh)[:, 0].reshape(model.config.rf_coords.x_coords.size, -1,
                                                                  order='F')
    Z = -np.asarray(model.config.rf_coords.mesh)[:, 1].reshape(model.config.rf_coords.x_coords.size, -1,
                                                                   order='F')
    rf_reshaped = rf.reshape(X.shape, order='F')
    norm = matplotlib.colors.Normalize(vmin=float(rf.min()), vmax=float(rf.max()))
    cmap = matplotlib.cm.rainbow_r
    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    plt.contourf(X, Z, rf_reshaped, cmap=cmap)
    sub_ax = plt.axes([0.92, 0.2, 0.01, 0.6])
    cbar = plt.colorbar(sm, cax=sub_ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('${S}_{u}$ design points [kPa] [-]', fontsize=16)

    fig.suptitle('β={beta:.2f}'.format(beta=beta), fontsize=16)

    if filename is not None:
        fig.savefig(filename)

    return fig
