"""Base class for neural differential equation models.

This module provides the foundation for implementing neural differential equation models.
It defines an abstract base class that all specific differential equation types
(ODEs, SDEs, etc.) should inherit from.
"""

# -- import packages: ----------------------------------------------------------
import torch
import ABCParse


# -- import standard libraries: ------------------------------------------------
from abc import abstractmethod


# -- Main operational class: ---------------------------------------------------
class BaseDiffEq(torch.nn.Module, ABCParse.ABCParse):
    """Abstract base class for all neural differential equation models.
    
    This class serves as the foundation for implementing various types of neural
    differential equations, including ODEs and SDEs. It combines PyTorch's Module
    system with ABCParse's parameter handling capabilities.
    
    All specific differential equation types should inherit from this class and
    implement the required abstract methods.
    
    Attributes:
        DIFFEQ_TYPE (str): Identifier for the differential equation type.
            Should be overridden by subclasses (e.g., "ODE", "SDE").
    """
    DIFFEQ_TYPE = ""
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the base differential equation model.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Note:
            Inheriting classes must call self.__config__(locals()) in their __init__ method
            to properly configure the model parameters.
        """
        super().__init__()
        
        """
        Must call self.__config__(locals()) in the __init__ of the inheriting
        class.        
        """

    # -- required methods in child classes: ------------------------------------
    @abstractmethod
    def drift(self):
        """Define the drift function of the differential equation.
        
        This abstract method must be implemented by all subclasses to define
        the deterministic part of the differential equation (often denoted as 'f').
        
        For ODEs, this represents the entire vector field.
        For SDEs, this represents the drift term.
        """
        ...

    @abstractmethod
    def diffusion(self):
        """Define the diffusion function of the differential equation.
        
        This abstract method must be implemented by all subclasses to define
        the stochastic part of the differential equation (often denoted as 'g').
        
        For ODEs, this is typically zero or used for compatibility with SDE interfaces.
        For SDEs, this represents the diffusion term that scales the noise.
        """
        ...

    def f(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Compute the drift term of the differential equation.
        
        This method provides a standardized interface for the drift term,
        compatible with numerical solvers like those in torchdiffeq and torchsde.
        
        Args:
            t (torch.Tensor): The current time point.
            y (torch.Tensor): The current state of the system.
            
        Returns:
            torch.Tensor: The drift term evaluated at the current state.
        """
        return self.drift(y)

    def g(self, t: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Compute the diffusion term of the differential equation.
        
        This method provides a standardized interface for the diffusion term,
        compatible with numerical solvers like those in torchsde.
        
        Args:
            t (torch.Tensor): The current time point.
            y (torch.Tensor): The current state of the system.
            
        Returns:
            torch.Tensor: The diffusion term evaluated at the current state.
        """
        return self.diffusion(y)
