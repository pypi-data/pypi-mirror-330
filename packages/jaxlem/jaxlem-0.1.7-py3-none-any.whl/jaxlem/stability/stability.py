import jax
import jax.numpy as jnp
from jax import lax
from jaxopt import GradientDescent
from jax_tqdm import scan_tqdm, loop_tqdm
import optax
from functools import partial
from abc import ABC, abstractmethod
from typing import Union, Tuple, Optional, Type
from jaxtyping import Array, Int, Float, Bool
from jaxlem.stability.stability_utils import StabilityConfig, FORMResults, FailureBox
from jaxlem.gradientdescent.gradientdescent_utils import GDHyperparams


FAILURE_PARAMS_TYPE = Union[
    Int[Array, "n_x_points*n_z_points*n_radius 3"],
    Float[Array, "n_x_points*n_z_points*n_radius 3"]
]


class SlopeStability(ABC):

    def __init__(self, config: StabilityConfig) -> None:
        self.config = config

    @staticmethod
    def _quadratic_roots(p: Float[Array, "3"]):

        delta = jnp.take(p, 1) ** 2 - 4 * jnp.take(p, 0) * jnp.take(p, 2)
        x = jnp.where(
            jnp.greater_equal(delta, 0),
            (-jnp.take(p, 1) + jnp.array([-1, 1]) * jnp.sqrt(jnp.abs(delta))) / (2 * jnp.take(p, 0)),
            jnp.array([1+1j, 1-1j])
        )
        return x

    @partial(jax.jit, static_argnums=(0,))
    def _p_quadratic(self, a: Float[Array, "1"], b: Float[Array, "1"], x_center: Float[Array, "1"],
                     z_center: Float[Array, "1"], radius: Float[Array, "1"]) -> Float[Array, "3"]:
        p_quadratic = jnp.asarray([
            jnp.array(1) + a ** 2,
            -2 * x_center + 2 * a * (b-z_center),
            x_center ** 2 + b ** 2 + z_center ** 2 - 2 * b * z_center - radius ** 2
        ])
        return p_quadratic

    @partial(jax.jit, static_argnums=(0,))
    def _crest_intersection(self, x_center: Float[Array, "1"], z_center: Float[Array, "1"], radius: Float[Array, "1"])\
            -> Tuple[Float[Array, "1"], Bool[Array, "1"]]:
        p_quadratic = self._p_quadratic(0, self.config.slope_height, x_center, z_center, radius)
        x_crest = self._quadratic_roots(p_quadratic)
        intersects_crest = jnp.any(jnp.equal(jnp.imag(x_crest), 0))
        # x_crest = jnp.real(x_crest).min()
        x_crest = jnp.real(x_crest)
        return x_crest, intersects_crest

    @partial(jax.jit, static_argnums=(0,))
    def _clay_intersection(self, x_center: Float[Array, "1"], z_center: Float[Array, "1"], radius: Float[Array, "1"]) \
            -> Tuple[Float[Array, "1"], Bool[Array, "1"]]:
        p_quadratic = self._p_quadratic(0, 0, x_center, z_center, radius)
        x_clay = self._quadratic_roots(p_quadratic)
        intersects_clay = jnp.any(jnp.equal(jnp.imag(x_clay), 0))
        x_clay = jnp.real(x_clay)
        return x_clay, intersects_clay

    @partial(jax.jit, static_argnums=(0,))
    def _slope_intersection(self, x_center: Float[Array, "1"], z_center: Float[Array, "1"], radius: Float[Array, "1"]) \
            -> Tuple[Float[Array, "1"], Bool[Array, "1"]]:
        a = -self.config.slope_rad
        b = self.config.slope_height - a * self.config.crest_length
        p_quadratic = self._p_quadratic(a, b, x_center, z_center, radius)
        x_slope = self._quadratic_roots(p_quadratic)
        intersects_slope = jnp.any(jnp.equal(jnp.imag(x_slope), 0))
        x_slope = jnp.sort(jnp.real(x_slope))
        in_slope = jnp.logical_and(
            jnp.greater(x_slope, self.config.crest_length),
            jnp.less(x_slope, self.config.crest_length+self.config.slope_length)
        )
        x_slope = jnp.where(in_slope, x_slope, -9999)
        intersects_slope = jnp.logical_and(intersects_slope, jnp.any(in_slope))

        return x_slope, intersects_slope

    @partial(jax.jit, static_argnums=(0,))
    def _check_intersections(self, intersects_crest: Bool[Array, "1"], intersects_clay: Bool[Array, "1"],
                             intersects_slope: Bool[Array, "1"]) \
            -> Tuple[
                Bool[Array, "1"],
                Bool[Array, "1"],
                Bool[Array, "1"],
                Bool[Array, "1"],
                Bool[Array, "1"],
                Bool[Array, "1"]
            ]:

        crest_clay = jnp.logical_and(
            jnp.logical_and(intersects_crest, intersects_clay),
            jnp.logical_not(intersects_slope)
        )
        crest_slope = jnp.logical_and(
            jnp.logical_and(intersects_crest, intersects_slope),
            jnp.logical_not(intersects_clay)
        )
        only_slope = jnp.logical_and(
                intersects_slope,
                jnp.logical_and(jnp.logical_not(intersects_crest), jnp.logical_not(intersects_clay))
            )
        crest_clay_slope = jnp.logical_and(
            intersects_slope,
            jnp.logical_and(intersects_crest, intersects_clay)
        )
        slope_clay = jnp.logical_and(
            intersects_slope,
            jnp.logical_and(intersects_clay, jnp.logical_not(intersects_crest))
        )
        only_crest = jnp.logical_and(
            intersects_crest,
            jnp.logical_and(jnp.logical_not(intersects_clay), jnp.logical_not(intersects_slope))
        )

        return crest_clay, crest_slope, only_slope, crest_clay_slope, slope_clay, only_crest

    @partial(jax.jit, static_argnums=(0,))
    def _unpack_failure_circle(self, failure_params: Float[Array, "3"])\
            -> Tuple[Float[Array, "1"], Float[Array, "1"], Float[Array, "1"]]:
        x_center = jnp.take(failure_params, 0)
        z_center = jnp.take(failure_params, 1)
        radius = jnp.take(failure_params, -1)
        return x_center, z_center, radius

    @partial(jax.jit, static_argnums=(0,))
    def _intersection_x(self, x_crest: Float[Array, "1"], x_clay: Float[Array, "1"], x_slope: Float[Array, "1"],
                        crest_clay: Bool[Array, "1"], crest_slope: Bool[Array, "1"], only_slope: Bool[Array, "1"],
                        only_crest: Bool[Array, "1"], crest_clay_slope: Bool[Array, "1"], slope_clay: Bool[Array, "1"])\
            -> Float[Array, "3"]:

        x_intersection = jnp.where(crest_clay, jnp.append(x_crest.min(), x_clay), 0)
        x_intersection = jnp.where(
            crest_slope,
            jnp.append(x_crest.min(), jnp.append(x_slope.max(), x_slope.max())),
            x_intersection
        )
        x_intersection = jnp.where(only_slope, jnp.append(x_slope, x_slope.max()), x_intersection)
        x_intersection = jnp.where(
            crest_clay_slope,
            jnp.append(x_crest.min(), jnp.append(x_clay.min(), x_slope.max())),
            x_intersection
        )
        x_intersection = jnp.where(slope_clay, jnp.append(x_slope.min(), x_clay), x_intersection)
        x_intersection = jnp.where(only_crest, jnp.append(x_crest.min(), x_crest), x_intersection)

        return x_intersection

    @partial(jax.jit, static_argnums=(0,))
    def _intersection(self, failure_params: Float[Array, "3"]) -> Tuple[Float[Array, "3"], Bool[Array, "1"]]:

        x_center, z_center, radius = self._unpack_failure_circle(failure_params)

        x_crest, intersects_crest = self._crest_intersection(x_center, z_center, radius)
        x_clay, intersects_clay = self._clay_intersection(x_center, z_center, radius)
        x_slope, intersects_slope = self._slope_intersection(x_center, z_center, radius)

        crest_clay, crest_slope, only_slope, crest_clay_slope, slope_clay, only_crest = \
            self._check_intersections(intersects_crest, intersects_clay, intersects_slope)

        x_intersection = self._intersection_x(x_crest, x_clay, x_slope, crest_clay, crest_slope, only_slope, only_crest,
                                              crest_clay_slope, slope_clay)

        intersects = jnp.append(intersects_crest, jnp.append(intersects_clay, intersects_slope))
        intersects = jnp.greater(intersects.sum(), 1)

        return x_intersection, intersects

    @partial(jax.jit, static_argnums=(0,))
    def _intersection_points(self, failure_params: Float[Array, "3"]) -> Tuple[Float[Array, "3 2"], Bool[Array, "1"]]:

        x_center, z_center, radius = self._unpack_failure_circle(failure_params)
        x_intersection, intersects = self._intersection(failure_params)

        z_intersection = z_center - jnp.sqrt(radius**2-(x_intersection-x_center)**2)
        intersection_points = jnp.stack((x_intersection, z_intersection), axis=-1)

        return intersection_points, intersects

    @partial(jax.jit, static_argnums=(0,))
    def _slice_coords(self, failure_params: Float[Array, "3"], intersection_points: Float[Array, "3 2"])\
            -> Float[Array, "n_slices 4 2"]:

        x_center = jnp.take(failure_params, 0)
        z_center = jnp.take(failure_params, 1)
        radius = jnp.take(failure_params, -1)

        x_intersection = jnp.take(intersection_points, 0, axis=1)

        x_slice = jnp.linspace(x_intersection.min(), x_intersection.max(), self.config.n_failure_circle_points)
        z_slice_top = jnp.where(
            jnp.less_equal(x_slice, self.config.crest_length+self.config.slope_length),
            self.config.slope_height,
            0
        )
        z_slice_top = jnp.where(
            jnp.logical_and(
                jnp.greater_equal(x_slice, self.config.crest_length),
                jnp.less(x_slice, self.config.crest_length+self.config.slope_length)
            ),
            self.config.slope_height-self.config.slope_rad*(x_slice-self.config.crest_length),
            z_slice_top
        )

        z_slice_bottom = z_center - jnp.sqrt(radius**2-(x_slice-x_center)**2)

        coords = self._make_coords(x_slice, z_slice_bottom, z_slice_top)

        return coords

    @partial(jax.jit, static_argnums=(0,))
    def _make_coords(self, x_slice: Float[Array, "n_failure_points"], z_slice_bottom: Float[Array, "n_failure_points"],
                     z_slice_top: Float[Array, "n_failure_points"]) -> Float[Array, "n_slices 4 2"]:

        x_coord = jnp.stack((
            jnp.take(x_slice, jnp.arange(x_slice.size-1)),
            jnp.take(x_slice, jnp.arange(1, x_slice.size))
        ), axis=-1)
        x_coord = jnp.repeat(x_coord, 2, axis=1)

        z_coord_bottom = jnp.stack((
            jnp.take(z_slice_bottom, jnp.arange(z_slice_bottom.size-1)),
            jnp.take(z_slice_bottom, jnp.arange(1, z_slice_bottom.size))
        ), axis=-1)
        z_coord_top = jnp.stack((
            jnp.take(z_slice_top, jnp.arange(z_slice_top.size-1)),
            jnp.take(z_slice_top, jnp.arange(1, z_slice_top.size))
        ), axis=-1)
        z_coord = jnp.stack((
            jnp.take(z_coord_top, 0, axis=1),
            jnp.take(z_coord_bottom, 0, axis=1),
            jnp.take(z_coord_bottom, 1, axis=1),
            jnp.take(z_coord_top, 1, axis=1)
        ), axis=-1)

        coords = jnp.stack((x_coord, z_coord), axis=-1)

        return coords

    @partial(jax.jit, static_argnums=(0,))
    def _slice_area(self, coords: Float[Array, "4 2"]) -> Float[Array, "1"]:
        x = jnp.take(coords, 0, axis=1)
        z = jnp.take(coords, 1, axis=1)
        area = 0.5 * jnp.abs(jnp.dot(x, jnp.roll(z, 1)) - jnp.dot(z, jnp.roll(x, 1)))
        return area

    @partial(jax.jit, static_argnums=(0,))
    def _slice_mass_center(self, coords: Float[Array, "n_slices 4 2"]) -> Float[Array, "n_slices 2"]:
        return jnp.mean(coords, axis=1)

    @partial(jax.jit, static_argnums=(0,))
    def _slice_lever(self, failure_params: Float[Array, "3"], mass_centers: Float[Array, "n_slices 2"])\
            -> Float[Array, "n_slices 2"]:
        x_center = jnp.take(failure_params, 0)
        return -(jnp.take(mass_centers, 0, axis=1) - x_center)  # Minus sign so that the moment takes the correct influence

    @partial(jax.jit, static_argnums=(0,))
    def _slice_weight(self, area: Float[Array, "n_slices"], mass_centers: Float[Array, "n_slices 2"])\
            -> Float[Array, "n_slices"]:
        soil_type = jnp.greater(jnp.take(mass_centers, 1, axis=1), 0)
        gamma = jnp.where(soil_type, self.config.embankment_gamma, self.config.clay_gamma)
        weight = gamma * area
        return weight

    @partial(jax.jit, static_argnums=(0,))
    def _slice_bottom_coords(self, coords: Float[Array, "n_slices 4 2"]) -> Float[Array, "2"]:
        return jnp.take(coords, jnp.arange(1, 3), axis=0)

    @partial(jax.jit, static_argnums=(0,))
    def _slice_bottom_center(self, coords: Float[Array, "n_slices 2 2"]) -> Float[Array, "n_slices 2"]:
        return jnp.mean(coords, axis=1)

    @partial(jax.jit, static_argnums=(0,))
    def _slice_bottom_length(self, coords: Float[Array, "n_slices 2 2"]) -> Float[Array, "n_slices"]:
        diff_coords = jnp.diff(coords, axis=1).squeeze()
        return jnp.sqrt(jnp.take(diff_coords, 0, axis=1)**2+jnp.take(diff_coords, 1, axis=1)**2)

    @partial(jax.jit, static_argnums=(0,))
    def _slice_bottom_lever(self, failure_params: Float[Array, "3"], coords: Float[Array, "2 2"]) -> Float[Array, "1"]:
        center = jnp.take(failure_params, jnp.arange(2))
        lever = jnp.linalg.norm(jnp.cross(jnp.diff(coords, axis=0), jnp.take(coords, 0, axis=0)-center)) /\
                jnp.linalg.norm(jnp.diff(coords, axis=0))
        return jnp.abs(lever)

    @partial(jax.jit, static_argnums=(0,))
    def _idx_rf(self, coords: Float[Array, "n_slices 2"]) -> Int[Array, "n_slices"]:

        x_points = jnp.take(coords, 0, axis=1)
        z_points = jnp.take(coords, 1, axis=1)

        x_distance = x_points - jnp.take(self.config.rf_coords.mesh, 0, axis=1)[:, jnp.newaxis]
        #  z_points > 0, config.rf_coords.y_grid < 0, use minus to fix their distances
        z_distance = -z_points - jnp.take(self.config.rf_coords.mesh, 1, axis=1)[:, jnp.newaxis]
        distance = jnp.sqrt(x_distance ** 2 + z_distance ** 2)
        idx_rf = distance.argmin(axis=0)

        return idx_rf

    @partial(jax.jit, static_argnums=(0,))
    def _strength(self, rf_points: Float[Array, "n_slices"], slice_bottom_centers: Float[Array, "n_slices 2"])\
            -> Float[Array, "n_slices"]:
        z_slice_centers = jnp.take(slice_bottom_centers, 1, axis=1)
        su = jnp.where(jnp.greater(z_slice_centers, 0), self.config.su_embankment,rf_points)
        return su

    @partial(jax.jit, static_argnums=(0,))
    def _resistance(self, rf: Float[Array, "n_rf_mesh"], slice_bottom_centers: Float[Array, "n_slices 2"],
                    slice_bottom_lengths: Float[Array, "n_slices"], slice_bottom_levers: Float[Array, "n_slices"])\
            -> Float[Array, "n_slices"]:
        idx_rf = self._idx_rf(slice_bottom_centers)
        rf_points = jnp.take(rf, idx_rf)
        su_points = self._strength(rf_points, slice_bottom_centers)
        slice_resistances = slice_bottom_levers * slice_bottom_lengths * su_points
        return slice_resistances

    @partial(jax.jit, static_argnums=(0,))
    def _check_bounds(self, failure_params: Float[Array, "3"]) -> Bool[Array, "1"]:
        x_center, z_center, radius = self._unpack_failure_circle(failure_params)
        out_of_vertical_bounds = jnp.less(z_center - radius, -self.config.clay_thickness)
        out_of_horizontal_bounds = jnp.logical_or(
            jnp.less(x_center - radius, 0),
            jnp.greater(x_center + radius, self.config.total_length)
        )
        out_of_bounds = jnp.logical_or(out_of_vertical_bounds, out_of_horizontal_bounds)
        return out_of_bounds

    @partial(jax.jit, static_argnums=(0,))
    def safety_factor_point(self, rf: Float[Array, "n_rf_mesh"], failure_params: Float[Array, "3"]) \
            -> Float[Array, "1"]:

        intersection_points, intersects = self._intersection_points(failure_params)

        slice_coords = self._slice_coords(failure_params, intersection_points)

        slice_areas = jax.vmap(self._slice_area)(slice_coords)
        slice_mass_centers = self._slice_mass_center(slice_coords)
        slice_levers = self._slice_lever(failure_params, slice_mass_centers)
        slice_weights = self._slice_weight(slice_areas, slice_mass_centers)
        slice_drives = slice_levers * slice_weights
        driving_moment = slice_drives.sum()

        slice_bottom_coords = jax.vmap(self._slice_bottom_coords)(slice_coords)
        slice_bottom_centers = self._slice_bottom_center(slice_bottom_coords)
        slice_bottom_lengths = self._slice_bottom_length(slice_bottom_coords)
        slice_bottom_levers = jax.vmap(self._slice_bottom_lever, in_axes=(None, 0))(failure_params, slice_bottom_coords)
        slice_resistances = self._resistance(rf, slice_bottom_centers, slice_bottom_lengths, slice_bottom_levers)
        resisting_moment = slice_resistances.sum()

        fos = resisting_moment / driving_moment

        out_of_bounds = self._check_bounds(failure_params)

        fos = jnp.where(intersects, fos, 9999.0).astype(jnp.float32)
        fos = jnp.where(out_of_bounds, 9999.0, fos).astype(jnp.float32)

        return fos

    @partial(jax.jit, static_argnums=(0,))
    def safety_factor_vmap(self, rf: Float[Array, "n_rf_mesh"], failure_params: Float[Array, "n_circles 3"])\
            -> Tuple[Float[Array, "1"], Float[Array, "3"], Float[Array, "n_circles"]]:
        fos = jax.vmap(self.safety_factor_point, in_axes=(None, 0))(rf, failure_params)
        return jnp.nanmin(fos.min()), jnp.take(failure_params, jnp.nanargmin(fos), axis=0), fos

    # @partial(jax.jit, static_argnums=(0, 2,))
    def _loss_gd(self, failure_params: Float[Array, "n_circles 3"], rf: Float[Array, "n_rf_mesh"]) -> Float[Array, "1"]:
            return self.safety_factor_point(rf, failure_params)

    @partial(jax.jit, static_argnums=(0, 2,))
    def safety_factor_gd(self, rf: Float[Array, "n_rf_mesh"], gd_hyperparams: GDHyperparams)\
            -> Tuple[Float[Array, "1"], Float[Array, "3"]]:

        _initilizate = jax.jit(
            lambda rng: jnp.take(
                self.config.failure_box.mesh,
                jax.random.choice(rng, jnp.arange(self.config.failure_box.mesh.shape[0]), shape=(1,)),
                axis=0).astype(jnp.float32).squeeze()
        )

        rng = jax.random.PRNGKey(42)
        rngs = jax.random.split(rng, gd_hyperparams.n_inits)
        circle_init = jax.vmap(_initilizate)(rngs)
        gd = GradientDescent(
            self._loss_gd,
            stepsize=gd_hyperparams.lr,
            maxiter=gd_hyperparams.max_epochs,
            tol=min(gd_hyperparams.obj_threshold, gd_hyperparams.grad_threshold),
            implicit_diff=True
        )
        res = jax.vmap(gd.run, in_axes=(0, None))(circle_init, rf)

        circles = res.params
        fos_all = jax.vmap(self.safety_factor_point, in_axes=(None, 0))(rf, circles)
        fos = fos_all.min()
        failure_circle = jnp.take(circles, fos_all.argmin(), axis=0)

        return fos, failure_circle

    @partial(jax.jit, static_argnums=(0, 2,))
    def reliability_montecarlo(self, rf: Float[Array, "n_mc n_rf_mesh"], gd_hyperparams: GDHyperparams)\
            -> Tuple[Float[Array, "1"], Float[Array, "n_mc"], Float[Array, "n_mc 3"]]:

        # """ Monte Carlo using vmap """
        # fos, failure_circle = jax.vmap(self.safety_factor_gd, in_axes=(0, None))(rf, gd_hyperparams)

        """ Monte Carlo using lax.scan """
        def _body(rf, i):
            rf_point = jnp.take(rf, i, axis=0)
            fos, failure_circle = self.safety_factor_gd(rf_point, gd_hyperparams)
            return rf, (fos, failure_circle)

        _, output = lax.scan(scan_tqdm(rf.shape[0])(_body), init=rf, xs=jnp.arange(rf.shape[0]))
        fos, failure_circle = output
        pf = jnp.sum(jnp.less(fos, 1))

        return pf, fos, failure_circle

    # @partial(jax.jit, static_argnums=(0, 2, 3,))
    @partial(jax.jit, static_argnums=(0,))
    def _u_to_rf(self, u: Float[Array, "n_rf_mesh"], rf_mean: Float[Array, "n_rf_mesh"],
                 rf_std: Float[Array, "n_rf_mesh"]) -> Float[Array, "n_rf_mesh"]:
        return rf_mean + rf_std * u

    @partial(jax.jit, static_argnums=(0, 4))
    def _lsf(self, u: Float[Array, "n_rf_mesh"], rf_mean: Float[Array, "n_rf_mesh"],
             rf_std: Float[Array, "n_rf_mesh"], gd_hyperparams) -> Float[Array, "1"]:
        rf = self._u_to_rf(u, rf_mean, rf_std)
        fos, _ = self.safety_factor_gd(rf, gd_hyperparams)
        return fos - 1

    @partial(jax.jit, static_argnums=(0, 3))
    def _convergence(self, beta: Float[Array, "1"], beta_old: Float[Array, "1"], beta_tol: float):
        return jnp.less(jnp.abs(beta - beta_old), beta_tol)

    @partial(jax.jit, static_argnums=(0, 3, 4, 5, 6))
    def reliability_form(self, rf_mean: Float[Array, "n_rf_mesh"], rf_std: Float[Array, "n_rf_mesh"],
                         gd_hyperparams: GDHyperparams, form_chains: int = 100, form_iters: int = 30,
                         beta_tol: float = 1e-2, verbose: bool = True) \
        -> Tuple[
            Float[Array, "n_form_chains"],
            Float[Array, "n_form_chains"],
            Float[Array, "n_form_chains"],
            Float[Array, "n_form_chains 3"],
            Float[Array, "n_form_chains"]
        ]:

        _initilizate_u = jax.jit(lambda rng: jax.random.normal(rng, shape=(rf_mean.size,)))

        @jax.jit
        def _loop(iloop, runner):
            u, beta_old, converged = runner
            u = jnp.where(jnp.isnan(u), 0, u)
            lsf = self._lsf(u, rf_mean, rf_std, gd_hyperparams)
            grads = jax.grad(self._lsf, argnums=(0,))(u, rf_mean, rf_std, gd_hyperparams)[0]
            grads_clean = jnp.where(jnp.isnan(grads), 0, grads)
            norm = jnp.linalg.norm(grads_clean)
            alpha = grads_clean / norm
            beta = beta_old + lsf / norm
            u = - alpha * beta
            u_clean_cond = jnp.logical_or(jnp.isnan(grads), jnp.equal(grads_clean, 0))
            u = jnp.where(u_clean_cond, 0, u)
            converged = self._convergence(beta, beta_old, beta_tol)
            return (u, beta, converged)

        rng = jax.random.PRNGKey(42)
        rngs = jax.random.split(rng, form_chains)
        u_init = jax.vmap(_initilizate_u)(rngs)
        beta_init = jnp.sqrt(jnp.mean(jnp.power(u_init, 2), axis=1))

        _initialize_vmap = jax.vmap(lambda x, y, z: (x, y, z), in_axes=(0, 0, None))
        runner = _initialize_vmap(u_init, beta_init, jnp.array(False))

        if verbose:
            runner = jax.vmap(lambda x: lax.fori_loop(0, form_iters, loop_tqdm(form_iters)(_loop), x))(runner)
        else:
            runner = jax.vmap(lambda x: lax.fori_loop(0, form_iters, _loop, x))(runner)

        u_chains, beta_chains, converged_chains = runner
        rf_chains = jax.vmap(self._u_to_rf, in_axes=(0, None, None))(u_chains, rf_mean, rf_std)
        beta_chains = jnp.sqrt(jnp.mean(jnp.power(u_chains, 2), axis=1))
        safety_factor_vmap = jax.vmap(self.safety_factor_gd, in_axes=(0, None))
        fos_chains, failure_circle_chains = safety_factor_vmap(rf_chains, gd_hyperparams)

        results = (rf_chains, fos_chains, beta_chains, failure_circle_chains, converged_chains)

        return results


if __name__ == "__main__":

    pass
