import jax.numpy as jnp
import numpy as np
from flax import struct
from typing import Union, Tuple, Optional, Type, NamedTuple, Sequence
from jaxtyping import Array, Int, Float, Bool
from dataclasses import dataclass, field
from jaxlem.stability.plotting_utils import viz_form
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


@dataclass
class FailureBox:
    x_lims: Tuple[Union[float, int], Union[float, int]]
    z_lims: Tuple[Union[float, int], Union[float, int]]
    radius_lims: Tuple[Union[float, int], Union[float, int]]
    n_x_points: int = 10
    n_z_points: int = 10
    n_radius: int = 10
    x_coords: Union[Int[Array, "n_x_points"], Float[Array, "n_x_points"]] = field(init=False)
    z_coords: Union[Int[Array, "n_z_points"], Float[Array, "n_z_points"]] = field(init=False)
    radius_grid: Union[Int[Array, "n_z_points"], Float[Array, "n_z_points"]] = field(init=False)
    mesh: Float[Array, "n_x_points*n_z_points*n_radius 3"] = field(init=False)

    def __post_init__(self) -> None:
        self.x_coords = jnp.linspace(self.x_lims[0], self.x_lims[1], self.n_x_points)
        self.z_coords = jnp.linspace(self.z_lims[0], self.z_lims[1], self.n_z_points)
        self.radius_grid = jnp.linspace(self.radius_lims[0], self.radius_lims[1], self.n_radius)
        mesh = jnp.meshgrid(self.x_coords, self.z_coords, self.radius_grid)
        self.mesh = jnp.stack((mesh[0].flatten(), mesh[1].flatten(), mesh[2].flatten()), axis=-1)


@dataclass
class RFCoords:
    x_coords: Union[
        np.ndarray[Union[float, int], "n_x_points"],
        Union[Int[Array, "n_x_points"], Float[Array, "n_x_points"]]
    ]
    z_coords: Union[
        np.ndarray[Union[float, int], "n_z_points"],
        Union[Int[Array, "n_z_points"], Float[Array, "n_z_points"]]
    ]
    mesh: Union[Int[Array, "n_x_points*n_z_points 2"], Float[Array, "n_x_points*n_z_points 2"]] = field(init=False)

    def __post_init__(self):
        mesh = jnp.meshgrid(self.x_coords, self.z_coords)
        self.mesh = jnp.stack((mesh[0].flatten(), mesh[1].flatten()), axis=-1)


@dataclass
class StabilityConfig:
    failure_box: FailureBox
    slope_height: Union[float, int] = 3
    slope_length: Union[float, int] = 10
    crest_length: Union[float, int] = 80
    toe_length: Union[float, int] = 60
    clay_thickness: Union[float, int] = 50
    embankment_gamma: Union[float, int] = 20
    clay_gamma: Union[float, int] = 20
    n_x_rf_coords: int = 30
    n_z_rf_coords: int = 10
    n_failure_circle_points: int = 101
    total_length: Union[float, int] = field(init=False)
    slope_rad: Union[float, int] = field(init=False)
    slope_deg: Union[float, int] = field(init=False)
    rf_coords: RFCoords = field(init=False)
    su_embankment: Union[float, int] = 40

    def __post_init__(self) -> None:
        self.total_length = self.crest_length + self.slope_length + self.toe_length
        self.slope_rad = self.slope_height / self.slope_length
        self.slope_deg = self.slope_rad * 180 / jnp.pi
        self.rf_coords = RFCoords(
            x_coords=jnp.linspace(0, self.total_length, self.n_x_rf_coords),
            z_coords=jnp.linspace(0, self.clay_thickness, self.n_z_rf_coords),
        )


@dataclass
class FORMResults:
    results: Tuple[
            Float[Array, "n_form_chains n_rf_cells"],
            Float[Array, "n_form_chains"],
            Float[Array, "n_form_chains"],
            Float[Array, "n_form_chains 3"],
            Float[Array, "n_form_chains"]
    ]
    rf_chains: Float[Array, "n_form_chains n_rf_cells"] = field(init=False)
    fos_chains: Float[Array, "n_form_chains"] = field(init=False)
    beta_chains: Float[Array, "n_form_chains"] = field(init=False)
    failure_circle_chains: Float[Array, "n_form_chains 3"] = field(init=False)
    converged_chains: Bool[Array, "n_form_chains"] = field(init=False)
    idx_critical: Int[Array, "1"] = field(init=False)
    beta: Float[Array, "1"] = field(init=False)
    fos: Float[Array, "1"] = field(init=False)
    rf:  Float[Array, "n_rf_cells"] = field(init=False)
    failure_circle: Float[Array, "3"] = field(init=False)

    def __post_init__(self) -> None:

        rf_chains, fos_chains, beta_chains, failure_circle_chains, converged_chains = self.results

        self.rf_chains = rf_chains
        self.fos_chains = fos_chains
        self.beta_chains = beta_chains
        self.failure_circle_chains = failure_circle_chains
        self.converged_chains = converged_chains

        beta_chains_converged = jnp.where(self.converged_chains, self.beta_chains, 9999)
        self.idx_critical = beta_chains_converged.argmin()
        self.beta = beta_chains_converged.min()
        self.fos = jnp.take(self.fos_chains, self.idx_critical, axis=0)
        self.rf = jnp.take(self.rf_chains, self.idx_critical, axis=0)
        self.failure_circle = jnp.take(self.failure_circle_chains, self.idx_critical, axis=0)

    def iter(self) -> zip:
        return zip(
            self.rf_chains,
            self.fos_chains,
            self.failure_circle_chains,
            self.beta_chains
        )

    def viz_critical(self, model, filename: Optional[str] = None):
        _ = viz_form(model, self.failure_circle, self.fos, self.rf, self.beta, filename)

    def viz_all(self, model, filename: Optional[str] = None):
        figs = []
        for i, (rf, fos, failure_circle, beta) in enumerate(self.iter()):
            fig = viz_form(model, failure_circle, fos, rf, beta, None)
            plt.close()
            figs.append(fig)

        pp = PdfPages(filename)
        [pp.savefig(fig) for fig in figs]
        pp.close()
