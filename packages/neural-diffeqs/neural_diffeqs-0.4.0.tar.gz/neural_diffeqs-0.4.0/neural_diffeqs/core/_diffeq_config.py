"""Configuration class for neural differential equations.

This module provides a configuration class for setting up neural networks
that parameterize drift and diffusion terms in neural differential equations.
"""

import ABCParse
from typing import List, Union, Tuple, Type, Dict, Any, Optional
import torch_nets


class DiffEqConfig(ABCParse.ABCParse):
    """Configuration for neural differential equation models.
    
    This class configures the neural networks that parameterize the drift (mu) 
    and diffusion (sigma) terms in neural differential equations. It provides
    a flexible interface for specifying network architectures and properties.
    
    Attributes:
        state_size (int): Dimension of the state space.
        mu_hidden (List[int]): Hidden layer sizes for the drift network.
        sigma_hidden (List[int]): Hidden layer sizes for the diffusion network.
        brownian_dim (int): Dimension of the Brownian motion.
        mu_activation (List[str]): Activation functions for the drift network.
        sigma_activation (List[str]): Activation functions for the diffusion network.
        mu_dropout (List[float]): Dropout rates for the drift network.
        sigma_dropout (List[float]): Dropout rates for the diffusion network.
        mu_n_augment (int): Number of augmented dimensions for the drift network.
        sigma_n_augment (int): Number of augmented dimensions for the diffusion network.
        mu_bias (List[bool]): Whether to use bias in the drift network layers.
        sigma_bias (List[bool]): Whether to use bias in the diffusion network layers.
        mu_potential (bool): Whether the drift is derived from a potential function.
        sigma_potential (bool): Whether the diffusion is derived from a potential function.
        mu_output_bias (bool): Whether to use bias in the drift network output layer.
        sigma_output_bias (bool): Whether to use bias in the diffusion network output layer.
    """
    
    def __init__(
        self,
        state_size: int,
        mu_hidden: List[int] = [2000, 2000],
        sigma_hidden: List[int] = [400, 400],
        brownian_dim: int = 1,
        mu_activation: List[str] = ["LeakyReLU"],
        sigma_activation: List[str] = ["LeakyReLU"],
        mu_dropout: List[float] = [0.2],
        sigma_dropout: List[float] = [0.2],
        mu_n_augment: int = 0,
        sigma_n_augment: int = 0,
        mu_bias: List[bool] = [True],
        sigma_bias: List[bool] = [True],
        mu_potential: bool = False,
        sigma_potential: bool = False,
        mu_output_bias: bool = False,
        sigma_output_bias: bool = False,
    ) -> None:
        """Initialize the differential equation configuration.
        
        Args:
            state_size: Dimension of the state space.
            mu_hidden: Hidden layer sizes for the drift network.
            sigma_hidden: Hidden layer sizes for the diffusion network.
            brownian_dim: Dimension of the Brownian motion.
            mu_activation: Activation functions for the drift network.
            sigma_activation: Activation functions for the diffusion network.
            mu_dropout: Dropout rates for the drift network.
            sigma_dropout: Dropout rates for the diffusion network.
            mu_n_augment: Number of augmented dimensions for the drift network.
            sigma_n_augment: Number of augmented dimensions for the diffusion network.
            mu_bias: Whether to use bias in the drift network layers.
            sigma_bias: Whether to use bias in the diffusion network layers.
            mu_potential: Whether the drift is derived from a potential function.
            sigma_potential: Whether the diffusion is derived from a potential function.
            mu_output_bias: Whether to use bias in the drift network output layer.
            sigma_output_bias: Whether to use bias in the diffusion network output layer.
        """
        self.__parse__(locals(), public = [None])

    @property
    def mu_in_features(self) -> int:
        """Get the input dimension for the drift network.
        
        Returns:
            The number of input features for the drift network.
        """
        return self._state_size

    @property
    def sigma_in_features(self) -> int:
        """Get the input dimension for the diffusion network.
        
        Returns:
            The number of input features for the diffusion network.
        """
        return self._state_size

    @property
    def mu_out_features(self) -> int:
        """Get the output dimension for the drift network.
        
        If mu_potential is True, the output is a scalar potential function.
        Otherwise, the output has the same dimension as the state.
        
        Returns:
            The number of output features for the drift network.
        """
        if self._mu_potential:
            return 1
        return self._state_size

    @property
    def sigma_out_features(self) -> int:
        """Get the output dimension for the diffusion network.
        
        If sigma_potential is True, the output is a scalar potential function.
        Otherwise, the output has dimension state_size * brownian_dim.
        
        Returns:
            The number of output features for the diffusion network.
        """
        if self._sigma_potential:
            return 1
        return self._state_size * self._brownian_dim

    @property
    def mu_output_bias(self) -> bool:
        """Determine whether to use bias in the drift network output layer.
        
        If mu_potential is True, no bias is used regardless of the setting.
        
        Returns:
            Boolean indicating whether to use bias in the output layer.
        """
        if self._mu_potential:
            return False
        return self._mu_output_bias

    @property
    def sigma_output_bias(self) -> bool:
        """Determine whether to use bias in the diffusion network output layer.
        
        If sigma_potential is True, no bias is used regardless of the setting.
        
        Returns:
            Boolean indicating whether to use bias in the output layer.
        """
        if self._sigma_potential:
            return False
        return self._sigma_output_bias

    @property
    def mu_net_cls(self) -> Type[Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet]]:
        """Get the appropriate network class for the drift term.
        
        Returns:
            The network class to use for the drift term.
        """
        if self._mu_n_augment:
            self._mu_kwargs = {"n_augment": self._mu_n_augment}
            return torch_nets.AugmentedTorchNet
        self._mu_kwargs = {}
        return torch_nets.TorchNet

    @property
    def sigma_net_cls(self) -> Type[Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet]]:
        """Get the appropriate network class for the diffusion term.
        
        Returns:
            The network class to use for the diffusion term.
        """
        if self._sigma_n_augment:
            self._sigma_kwargs = {"n_augment": self._sigma_n_augment}
            return torch_nets.AugmentedTorchNet
        self._sigma_kwargs = {}
        return torch_nets.TorchNet

    @property
    def mu(self) -> Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet]:
        """Create and configure the drift network.
        
        Returns:
            The configured neural network for the drift term.
        """
        return self.mu_net_cls(
            in_features=self.mu_in_features,
            out_features=self.mu_out_features,
            hidden=self._mu_hidden,
            activation=self._mu_activation,
            dropout=self._mu_dropout,
            bias=self._mu_bias,
            output_bias=self.mu_output_bias,
            **self._mu_kwargs,
        )

    @property
    def sigma(self) -> Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet]:
        """Create and configure the diffusion network.
        
        Returns:
            The configured neural network for the diffusion term.
        """
        return self.sigma_net_cls(
            in_features=self.sigma_in_features,
            out_features=self.sigma_out_features,
            hidden=self._sigma_hidden,
            activation=self._sigma_activation,
            dropout=self._sigma_dropout,
            bias=self._sigma_bias,
            output_bias=self.sigma_output_bias,
            **self._sigma_kwargs
        )
        
    def __call__(self) -> Tuple[Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet], 
                               Union[torch_nets.TorchNet, torch_nets.AugmentedTorchNet]]:
        """Return the configured drift and diffusion networks.
        
        Returns:
            A tuple containing the drift (mu) and diffusion (sigma) networks.
        """
        return self.mu, self.sigma
