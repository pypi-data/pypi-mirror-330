# -- import packages: ---------------------------------------------------------
import torch
import ABCParse
import abc

# -- import local dependencies: -----------------------------------------------
from ._base_neural_diffeq import BaseDiffEq
from ._diffeq_config import DiffEqConfig


class BaseLatentSDE(BaseDiffEq):
    DIFFEQ_TYPE = "SDE"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        """
        Must call self.__config__(locals()) in the __init__ of theinheriting
        class.
        
        
        """

    def __config__(self, kwargs: dict) -> None:
        """Sets up mu and sigma given params"""

        self.__parse__(kwargs=kwargs, public = ['noise_type', 'sde_type'])

        self._config_kwargs = ABCParse.function_kwargs(func=DiffEqConfig, kwargs=kwargs)
        configs = DiffEqConfig(**self._config_kwargs)

        self.mu = configs.mu
        self.sigma = configs.sigma

    # -- required methods in child classes: ------------------------------------
    @abc.abstractmethod
    def drift(self):
        """Called by self.f"""
        ...

    @abc.abstractmethod
    def diffusion(self):
        """Called by self.g"""
        ...

    @abc.abstractmethod
    def prior_drift(self):
        """Called by self.h"""
        ...

    def h(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Should return the output of self.diffusion"""
        return self.prior_drift(y)
