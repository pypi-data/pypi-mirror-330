
import torch
import ABCParse
from abc import abstractmethod


# from ._base_neural_diffeq import BaseDiffEq
from ._base_neural_ode import BaseODE


class BaseLatentODE(BaseODE):
    DIFFEQ_TYPE = "ODE"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        """
        Must call self.__config__(locals()) in the __init__ of theinheriting
        class.
        
        """

#     def __config__(self, kwargs):
#         """Sets up mu and sigma given params"""

#         self.__parse__(kwargs=kwargs)

#         self._config_kwargs = ABCParse.function_kwargs(func=DiffEqConfig, kwargs=kwargs)
#         configs = DiffEqConfig(**self._config_kwargs)
#         self.mu = configs.mu

    # -- required methods in child classes: ------------------------------------
    @abstractmethod
    def drift(self):
        """Called by self.f"""
        ...
    
#     def diffusion(self, y):
#         # keep for compatibility with torchsde.sdeint
#         """Called by self.g"""
#         return torch.zeros([y.shape[0], y.shape[1], self.brownian_dim])
    
    @abstractmethod
    def prior_drift(self):
        """Called by self.h"""
        ...

    def h(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Should return the output of self.diffusion"""
        return self.prior_drift(y)
