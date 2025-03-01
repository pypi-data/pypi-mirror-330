# -- import packages: ----------------------------------------------------------
import torch


# -- import local dependencies: ------------------------------------------------
from . import core


# -- import standard libraries and define types: -------------------------------
from typing import Union, List


# -- Main operational class: ---------------------------------------------------
class LatentPotentialSDE(core.BaseLatentSDE):
    """
    Latent Potential Stochastic Differential Equation (SDE) model.
    
    This class implements a stochastic differential equation with a potential function
    in the latent space. The SDE is defined by:
    
    dY_t = f(Y_t)dt + g(Y_t)dW_t
    
    where:
    - f(Y_t) is the drift function (deterministic part)
    - g(Y_t) is the diffusion function (stochastic part)
    - W_t is a Brownian motion
    
    The model also includes a prior drift function based on a potential gradient.
    
    Attributes:
        DIFFEQ_TYPE (str): Type of differential equation ("SDE").
        potential (core.Potential): Potential function used for prior drift.
    """
    DIFFEQ_TYPE = "SDE"

    def __init__(
        self,
        state_size: int,
        mu_hidden: Union[List[int], int] = [2000, 2000],
        sigma_hidden: Union[List[int], int] = [400, 400],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        sigma_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.2,
        sigma_dropout: Union[float, List[float]] = 0.2,
        mu_bias: Union[bool, List[bool]] = True,
        sigma_bias: Union[bool, List[bool]] = True,
        mu_output_bias: bool = False,
        sigma_output_bias: bool = True,
        mu_n_augment: int = 0,
        sigma_n_augment: int = 0,
        sde_type: str = "ito",
        noise_type: str = "general",
        brownian_dim: int = 1,
        coef_drift: float = 1.,
        coef_diffusion: float = 1.,
        coef_prior_drift: float = 1.,
    ):
        """
        Initialize the LatentPotentialSDE model.
        
        Parameters:
            state_size (int): Dimension of the state space.
            mu_hidden (Union[List[int], int]): Hidden layer sizes for the drift network.
            sigma_hidden (Union[List[int], int]): Hidden layer sizes for the diffusion network.
            mu_activation (Union[str, List[str]]): Activation function(s) for the drift network.
            sigma_activation (Union[str, List[str]]): Activation function(s) for the diffusion network.
            mu_dropout (Union[float, List[float]]): Dropout rate(s) for the drift network.
            sigma_dropout (Union[float, List[float]]): Dropout rate(s) for the diffusion network.
            mu_bias (Union[bool, List[bool]]): Whether to use bias in the drift network layers.
            sigma_bias (Union[bool, List[bool]]): Whether to use bias in the diffusion network layers.
            mu_output_bias (bool): Whether to use bias in the output layer of the drift network.
            sigma_output_bias (bool): Whether to use bias in the output layer of the diffusion network.
            mu_n_augment (int): Number of augmented dimensions for the drift network.
            sigma_n_augment (int): Number of augmented dimensions for the diffusion network.
            sde_type (str): Type of SDE ("ito" or "stratonovich").
            noise_type (str): Type of noise ("diagonal" or "general").
            brownian_dim (int): Dimension of the Brownian motion.
            coef_drift (float): Coefficient for the drift term.
            coef_diffusion (float): Coefficient for the diffusion term.
            coef_prior_drift (float): Coefficient for the prior drift term.
        """
        super().__init__()

        # explicitly state that we are not learning a potential function by default
        mu_potential = False
        self.__config__(locals())
        self.potential = core.Potential(state_size=self._state_size)

    def drift(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the drift function of the SDE.
        
        The drift function represents the deterministic part of the SDE and is 
        implemented as a neural network (self.mu) scaled by a coefficient.
        
        Parameters:
            y (torch.Tensor): Current state tensor of shape [batch_size, state_size].
            
        Returns:
            torch.Tensor: Drift term of shape [batch_size, state_size].
        """
        return self.mu(y) * self._coef_drift

    def prior_drift(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the prior drift function based on a potential gradient.
        
        This function calculates the gradient of the potential function with respect
        to the state and scales it by a coefficient. It's used to incorporate prior
        knowledge into the SDE.
        
        Parameters:
            y (torch.Tensor): Current state tensor of shape [batch_size, state_size].
            
        Returns:
            torch.Tensor: Prior drift term of shape [batch_size, state_size].
        """
        return self.potential.potential_gradient(y) * self._coef_prior_drift

    def diffusion(self, y: torch.Tensor) -> torch.Tensor:
        """
        Compute the diffusion function of the SDE.
        
        The diffusion function represents the stochastic part of the SDE and is
        implemented as a neural network (self.sigma) scaled by a coefficient.
        
        Parameters:
            y (torch.Tensor): Current state tensor of shape [batch_size, state_size].
            
        Returns:
            torch.Tensor: Diffusion term of shape [batch_size, state_size, brownian_dim].
        """
        return self.sigma(y).view(y.shape[0], y.shape[1], self._brownian_dim) * self._coef_diffusion
