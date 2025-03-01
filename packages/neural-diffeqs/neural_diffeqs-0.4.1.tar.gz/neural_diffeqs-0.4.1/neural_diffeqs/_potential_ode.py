# -- import packages: ---------------------------------------------------------
import torch


# -- import local dependencies: -----------------------------------------------
from .core import BaseODE


# -- import standard libraries and define types: ------------------------------
from typing import Union, List


# -- Main operational class: --------------------------------------------------
class PotentialODE(BaseODE):
    DIFFEQ_TYPE = "ODE"
    
    """
    PotentialODE implements an Ordinary Differential Equation (ODE) based on a potential function.
    
    This class defines an ODE where the drift term is derived from the gradient of a potential function.
    The potential function is represented by a neural network, and the drift is computed as the gradient
    of this potential with respect to the state.
    
    Inherits from BaseODE, which provides the basic structure for neural ODEs.
    """
    
    def __init__(
        self,
        state_size: int,
        dt: float = 0.1,
        coef_diff: float = 0,
        mu_hidden: Union[List[int], int] = [512, 512],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.,
        mu_bias: bool = True,
        mu_output_bias: bool = True,
        mu_n_augment: int = 0,
        sde_type: str = "ito",
        noise_type: str = "general",
        brownian_dim: int = 1,
    ) -> None:
        
        """
        Initialize a PotentialODE instance.
        
        Args:
            state_size: Dimensionality of the state space.
            dt: Time step size for numerical integration.
            coef_diff: Diffusion coefficient (typically 0 for ODEs).
            mu_hidden: Hidden layer sizes for the potential network. Can be a list of integers for multiple layers
                      or a single integer for a single hidden layer.
            mu_activation: Activation function(s) for the potential network. Can be a string or a list of strings.
            mu_dropout: Dropout rate(s) for the potential network. Can be a float or a list of floats.
            mu_bias: Whether to include bias terms in the hidden layers of the potential network.
            mu_output_bias: Whether to include a bias term in the output layer of the potential network.
            mu_n_augment: Number of augmented dimensions for the potential network.
            sde_type: Type of stochastic differential equation (e.g., "ito"). Used for compatibility with SDE models.
            noise_type: Type of noise (e.g., "general"). Used for compatibility with SDE models.
            brownian_dim: Dimensionality of the Brownian motion. Used for compatibility with SDE models.
            
        Returns:
            None
        """
        
        super().__init__()
        
        mu_potential = True

        self.__config__(locals())

    def _potential(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the potential function value for a given state.
        
        This method applies the potential neural network to the input state to compute
        the scalar potential value.
        
        Args:
            y: Input state tensor of shape [batch_size, state_size].
            
        Returns:
            Scalar potential value tensor of shape [batch_size, 1].
        """
        return self.mu(y)

    def _gradient(self, ψ: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the gradient of the potential with respect to the state.
        
        This method uses PyTorch's autograd to compute the gradient of the potential
        with respect to the state, which is used as the drift term in the ODE.
        
        Args:
            ψ: Potential value tensor of shape [batch_size, 1].
            y: State tensor of shape [batch_size, state_size] with requires_grad=True.
            
        Returns:
            Gradient tensor of shape [batch_size, state_size].
        """
        return torch.autograd.grad(ψ, y, torch.ones_like(ψ), create_graph=True)[0]

    def drift(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the drift term of the ODE.
        
        For a potential-based ODE, the drift is the negative gradient of the potential
        with respect to the state. This method computes the potential and then its gradient.
        
        Args:
            y: Input state tensor of shape [batch_size, state_size].
            
        Returns:
            Drift tensor of shape [batch_size, state_size].
        """
        y = y.requires_grad_()
        ψ = self._potential(y)
        return self._gradient(ψ, y)
