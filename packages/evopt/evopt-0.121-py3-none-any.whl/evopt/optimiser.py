import numpy as np
import os
from typing import Callable
from .cma_optimiser import CmaesOptimiser
from .directory_manager import DirectoryManager

def optimise(
    params: dict,
    evaluator: Callable,
    optimiser: str = 'cmaes',
    base_dir: str = None,
    dir_id: int = None,
    sigma_threshold: float = 0.1,
    batch_size: int = 16,
    start_epoch: int = None,
    verbose: bool = True,
    n_epochs: int = None,
):
    """
    Top-level function to run the optimization.

    Args:
        params (dict): A dictionary defining the parameters to optimise,
            where keys are parameter names and values are tuples of (min, max) bounds.
        evaluator (Callable): A callable that evaluates the parameters and returns an error value.
        batch_size (int): The number of solutions to evaluate in each epoch.
        optimiser (str, optional): The optimiser to use. Defaults to 'cmaes'.
        base_dir (str, optional): The base directory for all runs. Defaults to None.
        dir_id (int, optional): The specific directory ID for this run.
            If None, a new ID will be generated. Defaults to None.
        sigma_threshold (float, optional): Threshold for sigma values to terminate optimisation. 
        	Defaults to 0.1.
        start_epoch (int, optional): Epoch to start from (for resuming). Defaults to None.
        verbose (bool, optional): Whether to print detailed information during optimisation. Defaults to False.
        n_epochs (int, optional): The number of epochs to run the optimisation for. If None, the optimisation runs until the termination criteria is met. Defaults to None.
    """

    directory_manager = DirectoryManager(
        base_dir = os.getcwd() if base_dir is None else base_dir,
        dir_id = dir_id
    )
    if optimiser.lower() == 'cmaes':
        optimizer_class = CmaesOptimiser
    else:
        raise ValueError(f"Unsupported optimizer: {optimiser}")

    optimizer = optimizer_class(
        parameters=params,
        evaluator=evaluator,
        n_epochs=n_epochs,
        batch_size=batch_size,
        directory_manager=directory_manager,
        sigma_threshold=sigma_threshold,
        rand_seed=dir_id,
        start_epoch=start_epoch,
        verbose=verbose,
    )

    with directory_manager.logger:
        params = optimizer.optimise()
    return params