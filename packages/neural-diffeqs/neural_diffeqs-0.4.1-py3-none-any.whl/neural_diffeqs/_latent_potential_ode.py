# -- import packages: ---------------------------------------------------------
import torch

# -- import local dependencies: -----------------------------------------------
from . import core

# -- set type hints: ----------------------------------------------------------
from typing import Union, List

# -- Main operational class: --------------------------------------------------
class LatentPotentialODE(core.BaseLatentODE):
    """A latent ordinary differential equation (ODE) model with a potential function.
    
    This class implements a neural ODE that combines a learned drift function with a 
    potential-based prior drift. The model uses a neural network to learn the drift 
    function and a potential function to define the prior drift through its gradient.
    
    The LatentPotentialODE inherits from BaseLatentODE and implements the required
    drift and prior_drift methods. It uses a Potential object to compute the gradient
    of the potential function for the prior drift.
    
    Attributes:
        DIFFEQ_TYPE (str): Type of differential equation, set to "ODE".
        potential (core.Potential): The potential function used for prior drift.
        mu (torch.nn.Module): Neural network for the drift function.
    """
    DIFFEQ_TYPE = "ODE"

    def __init__(
        self,
        state_size: int,
        coef_diff: float = 0,
        dt: float = 0.1,
        mu_hidden: Union[List[int], int] = [512, 512],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.,
        mu_bias: Union[bool, List[bool]] = True,
        mu_output_bias: bool = True,
        mu_n_augment: int = 0,
        sde_type: str = "ito",
        noise_type: str = "general",
        brownian_dim: int = 1,
    ) -> None:
        """Instantiate a LatentPotentialODE
        
        Args:
            state_size (int): Dimensionality of the state space.
            
            coef_diff (float): Diffusion coefficient scaling factor. Even though this is an ODE,
                               this parameter is kept for compatibility with SDE implementations.
                               ``**Default**: 0``
            
            dt (float): Time step size for numerical integration.
                        ``**Default**: 0.1``
            
            mu_hidden (Union[List[int], int]): Hidden layer sizes for the drift neural network.
                                              If an integer is provided, a single hidden layer with
                                              that many units is created.
                                              ``**Default**: [512, 512]``
            
            mu_activation (Union[str, List[str]]): Activation function(s) for the drift neural network.
                                                  If a string is provided, the same activation is used
                                                  for all layers.
                                                  ``**Default**: "LeakyReLU"``
            
            mu_dropout (Union[float, List[float]]): Dropout rate(s) for the drift neural network.
                                                   If a float is provided, the same dropout rate is used
                                                   for all layers.
                                                   ``**Default**: 0.``
            
            mu_bias (Union[bool, List[bool]]): Whether to include bias terms in the drift neural network.
                                              If a boolean is provided, the same setting is used for all layers.
                                              ``**Default**: True``
            
            mu_output_bias (bool): Whether to include a bias term in the output layer of the drift neural network.
                                  ``**Default**: True``
            
            mu_n_augment (int): Number of augmented dimensions for the drift neural network.
                               Used when the network is an AugmentedTorchNet.
                               ``**Default**: 0``
            
            sde_type (str): Type of stochastic differential equation interpretation.
                           Kept for compatibility with SDE implementations.
                           ``**Default**: "ito"``
            
            noise_type (str): Type of noise model to use.
                             Kept for compatibility with SDE implementations.
                             ``**Default**: "general"``
            
            brownian_dim (int): Dimensionality of the Brownian motion.
                               Kept for compatibility with SDE implementations.
                               ``**Default**: 1``
            
        Returns:
            None
            
        Notes:
            By declaring ``mu_potential = False``, we explicitly state that
            we are not learning a potential function by default.
        """
        
        super().__init__()

        mu_potential = False
        self.__config__(locals())
        self.potential = core.Potential(state_size = self._state_size)

    def drift(self, y: torch.Tensor) -> torch.Tensor:
        """Compute the drift function of the ODE.
        
        This method implements the drift function f(y) of the ODE dy/dt = f(y).
        It uses the neural network mu to compute the drift.
        
        Args:
            y (torch.Tensor): Input state tensor of shape [batch_size, state_size].
            
        Returns:
            y_hat_f (torch.Tensor): Drift function output of shape [batch_size, state_size].
        """
        return self.mu(y)

    def prior_drift(self, y: torch.Tensor) -> torch.Tensor:
        """Compute the prior drift function of the ODE.
        
        This method implements the prior drift function h(y) of the ODE.
        It computes the gradient of the potential function with respect to y.
        
        Args:
            y (torch.Tensor): Input state tensor of shape [batch_size, state_size].
            
        Returns:
            y_hat_h (torch.Tensor): Prior drift function output of shape [batch_size, state_size].
        """
        return self.potential.potential_gradient(y)
