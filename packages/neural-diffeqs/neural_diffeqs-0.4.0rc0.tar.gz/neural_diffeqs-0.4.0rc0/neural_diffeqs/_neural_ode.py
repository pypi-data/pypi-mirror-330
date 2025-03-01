# -- import packages: ---------------------------------------------------------
import torch


# -- import local dependencies: -----------------------------------------------
from .core._base_neural_ode import BaseODE


# -- import standard libraries and define types: ------------------------------
from typing import Union, List


# -- Main operational class: --------------------------------------------------
class NeuralODE(BaseODE):
    """
    Neural Ordinary Differential Equation (Neural ODE) implementation.
    
    This class implements a neural network-based ODE solver where the dynamics
    are parameterized by a neural network. The drift function is learned from data,
    allowing for flexible modeling of continuous-time dynamical systems.
    
    Neural ODEs can be used for various tasks including time series modeling,
    continuous normalizing flows, and latent dynamics modeling in variational autoencoders.
    
    The implementation follows the approach described in "Neural Ordinary Differential
    Equations" (Chen et al., 2018).
    """
    
    DIFFEQ_TYPE = "ODE"
    
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
    ) -> None:
        """
        Initialize a Neural ODE model.
        
        Args:
            state_size: int
                Dimensionality of the state vector.
            
            dt: float = 0.1
                Time step size for numerical integration.
            
            coef_diff: float = 0
                Diffusion coefficient. For ODEs, this is typically set to 0.
            
            mu_hidden: Union[List[int], int] = [512, 512]
                Hidden layer sizes for the drift network. If an integer is provided,
                a single hidden layer with that many units will be used.
            
            mu_activation: Union[str, List[str]] = "LeakyReLU"
                Activation function(s) for the drift network. Can be a single string
                or a list of strings for different activations per layer.
            
            mu_dropout: Union[float, List[float]] = 0.
                Dropout rate(s) for the drift network. Can be a single float
                or a list of floats for different dropout rates per layer.
            
            mu_bias: bool = True
                Whether to include bias terms in the drift network layers.
            
            mu_output_bias: bool = True
                Whether to include a bias term in the output layer of the drift network.
            
            mu_n_augment: int = 0
                Number of augmented dimensions to add to the state for the drift network.
                Augmentation can help with expressivity of the model.
            
            sde_type: str = "ito"
                Type of stochastic differential equation. Options are "ito" or "stratonovich".
                For ODEs, this parameter has no effect but is included for API consistency.
            
            noise_type: str = "general"
                Type of noise model. For ODEs, this parameter has no effect but is
                included for API consistency with the SDE implementations.
            
        Returns:
            None
        """

        # -- auto: we are not using the diffusion: ----------------------------

        sigma_hidden = []
        sigma_output_bias = False
        brownian_dim = 1

        super().__init__()

        self.__config__(locals())

    def drift(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the drift term of the ODE.
        
        This method computes the time derivative of the state vector using
        the learned neural network.
        
        Args:
            y: torch.Tensor
                Current state tensor of shape [batch_size, state_size].
                
        Returns:
            torch.Tensor: The computed drift (time derivative) of the same shape as y.
        """
        return self.mu(y)

    def forward(self, t, y: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for the Neural ODE.
        
        This method is called by ODE solvers during integration. It returns the
        time derivative of the state at the current time point.
        
        Args:
            t: torch.Tensor or float
                Current time point. Not used in autonomous ODEs but required for
                compatibility with ODE solvers.
            y: torch.Tensor
                Current state tensor of shape [batch_size, state_size].
                
        Returns:
            torch.Tensor: The computed time derivative of the same shape as y.
        """
        return self.mu(y)
