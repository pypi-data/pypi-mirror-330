# -- import packages: ----------------------------------------------------------
import torch


# -- import local dependencies: ------------------------------------------------
from . import core


# -- import standard libraries and define types: -------------------------------
from typing import Union, List


# -- Main operational class: ---------------------------------------------------
class PotentialSDE(core.BaseSDE):
    """PotentialSDE, subclass of core.BaseSDE
    
    A stochastic differential equation (SDE) model that uses a potential-based approach for the drift term.
    The drift is computed as the gradient of a scalar potential function, which is modeled by a neural network.
    This approach ensures that the drift field is conservative (curl-free).
    """
    DIFFEQ_TYPE = "SDE"
    def __init__(
        self,
        state_size: int,
        mu_hidden: Union[List[int], int] = [512, 512],
        sigma_hidden: Union[List[int], int] = [32, 32],
        mu_activation: Union[str, List[str]] = "LeakyReLU",
        sigma_activation: Union[str, List[str]] = "LeakyReLU",
        mu_dropout: Union[float, List[float]] = 0.,
        sigma_dropout: Union[float, List[float]] = 0.,
        mu_bias: Union[bool, List[bool]] = True,
        sigma_bias: Union[bool, List[bool]] = True,
        sigma_output_bias: bool = True,
        mu_n_augment: int = 0,
        sigma_n_augment: int = 0,
        sde_type: str = "ito",
        noise_type: str = "general",
        brownian_dim: int = 1,
        coef_drift: float = 1.,
        coef_diffusion: float = 1.,
    ):
        
        """PotentialSDE instantiation from parameters are parsed and passed to the base class config function.
        
        Args:
            state_size (int): Input and output state size of the differential equation.
        
            mu_hidden (Union[List[int], int]): Architecture of the hidden layers of the drift neural network. **Default**: ``[512, 512]``.
        
            sigma_hidden (Union[List[int], int]): Architecture of the hidden layers of the diffusion neural network. **Default**: ``[32, 32]``.
            
            mu_activation (Union[str, List[str]]): Activation function(s) used in each layer of the drift neural network. If ``len(mu_hidden) > len(mu_activation)``, the remaining activation functions are autofilled using the last value passed. **Default**: ``"LeakyReLU"``.
            
            sigma_activation (Union[str, List[str]]): Activation function(s) used in each layer of the diffusion neural network. If ``len(sigma_hidden) > len(sigma_activation)``, the remaining activation functions are autofilled using the last value passed. **Default**: ``"LeakyReLU"``.
            
            mu_dropout (Union[float, List[float]]): Dropout rate(s) for each layer of the drift neural network. If ``len(mu_hidden) > len(mu_dropout)``, the remaining dropout rates are autofilled using the last value passed. **Default**: ``0.``.
            
            sigma_dropout (Union[float, List[float]]): Dropout rate(s) for each layer of the diffusion neural network. If ``len(sigma_hidden) > len(sigma_dropout)``, the remaining dropout rates are autofilled using the last value passed. **Default**: ``0.``.
            
            mu_bias (Union[bool, List[bool]]): Whether to include bias terms in each layer of the drift neural network. If ``len(mu_hidden) > len(mu_bias)``, the remaining bias flags are autofilled using the last value passed. **Default**: ``True``.
            
            sigma_bias (Union[bool, List[bool]]): Whether to include bias terms in each layer of the diffusion neural network. If ``len(sigma_hidden) > len(sigma_bias)``, the remaining bias flags are autofilled using the last value passed. **Default**: ``True``.
            
            sigma_output_bias (bool): Whether to include a bias term in the output layer of the diffusion neural network. **Default**: ``True``.
            
            mu_n_augment (int): Number of augmented dimensions for the drift neural network. If greater than 0, uses an AugmentedTorchNet instead of a standard TorchNet. **Default**: ``0``.
            
            sigma_n_augment (int): Number of augmented dimensions for the diffusion neural network. If greater than 0, uses an AugmentedTorchNet instead of a standard TorchNet. **Default**: ``0``.
            
            sde_type (str): Type of SDE formulation to use. Options are "ito" or "stratonovich". **Default**: ``"ito"``.
            
            noise_type (str): Type of noise to use in the SDE. Options are "general", "diagonal", or "scalar". **Default**: ``"general"``.
            
            brownian_dim (int): Number of diffusion dimensions. **Default**: ``1``.
            
            coef_drift (float): Multiplier of drift network output. **Default**: ``1.``.
            
            coef_diffusion (float): Multiplier of diffusion network output. **Default**: ``1.``.
        
        Returns:
            None
        
        Notes:
            NeuralSDE: torch.nn.Module
            
        Example:
        
            .. code-block:: python

                import neural_diffeqs
                SDE = neural_diffeqs.PotentialSDE(state_size = 50)
        """
        
        super().__init__()

        mu_potential = True
        self.__config__(locals())
        
    def _potential(self, y: torch.Tensor) -> torch.Tensor:
        
        """Compute the scalar potential function.
        
        This method computes the scalar potential function using the mu neural network.
        The potential is a scalar field whose gradient gives the drift of the SDE.
        
        Args:
            y (torch.Tensor): Input tensor representing the state. Shape: [batch_size, state_size].
            
        Returns:
            torch.Tensor: Scalar potential values. Shape: [batch_size, 1].
        """
        
        y = y.requires_grad_()
        return self.mu(y)

    def _gradient(self, ψ: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        
        """Compute the gradient of the potential with respect to the input.
        
        This method computes the gradient of the potential function ψ with respect to the input y
        using PyTorch's autograd functionality. The gradient represents the conservative vector field
        that determines the drift of the SDE.
        
        Args:
            ψ (torch.Tensor): Scalar potential values. Shape: [batch_size, 1].
            y (torch.Tensor): Input tensor representing the state. Shape: [batch_size, state_size].
            
        Returns:
            torch.Tensor: Gradient of the potential with respect to the input. Shape: [batch_size, state_size].
        """
        
        return torch.autograd.grad(ψ, y, torch.ones_like(ψ), create_graph=True)[0]

    def drift(self, y: torch.Tensor) -> torch.Tensor:
        
        """Compute the drift term of the SDE.
        
        This method computes the drift term of the SDE as the gradient of the potential function
        multiplied by the drift coefficient. The drift represents the deterministic part of the SDE.
        
        Args:
            y (torch.Tensor): Input tensor representing the state. Shape: [batch_size, state_size].
            
        Returns:
            torch.Tensor: Drift term of the SDE. Shape: [batch_size, state_size].
        """
        
        y = y.requires_grad_()
        ψ = self._potential(y)
        return self._gradient(ψ, y) * self._coef_drift

    def diffusion(self, y: torch.Tensor) -> torch.Tensor:
        
        """Compute the diffusion term of the SDE.
        
        This method computes the diffusion term of the SDE using the sigma neural network.
        The diffusion represents the stochastic part of the SDE.
        
        Args:
            y (torch.Tensor): Input tensor representing the state. Shape: [batch_size, state_size].
            
        Returns:
            torch.Tensor: Diffusion term of the SDE. Shape: [batch_size, state_size, brownian_dim].
        """
        
        return self.sigma(y).view(y.shape[0], y.shape[1], self._brownian_dim) * self._coef_diffusion
