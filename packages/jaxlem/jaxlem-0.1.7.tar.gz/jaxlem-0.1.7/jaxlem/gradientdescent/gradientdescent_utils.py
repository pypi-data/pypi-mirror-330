import numpy as np
import jax
import jax.numpy as jnp
from jax import lax
from flax import struct
from jax_tqdm import scan_tqdm, loop_tqdm
from flax.training.train_state import TrainState
from dataclasses import dataclass
from functools import partial


class TrainState(TrainState):
    obj_keeper: jnp.float32
    grads_keeper: jnp.array
    converged: jnp.bool_
    convergence_epoch: jnp.int32


@dataclass
class FitResults:
    theta: np.array
    converged: bool
    convergence_epoch: int
    objective_value: float
    grads: np.array


@struct.dataclass
class GDHyperparams:
    lr: float = 1e-1
    max_epochs: int = 100
    transition_steps: int = 10_000
    decay_rate: float = 0.99
    obj_threshold: float = 1e-3
    grad_threshold: float = 1e-3
    n_inits: int = 1
