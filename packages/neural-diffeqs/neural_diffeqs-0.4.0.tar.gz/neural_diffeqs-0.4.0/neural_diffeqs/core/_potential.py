# -- import packages: ----------------------------------------------------------
import torch


# -- operational class: --------------------------------------------------------
class Potential(torch.nn.Sequential):

    """Linear transform state of arbitrary dimension to a 1-D potential value"""

    def __init__(self, state_size: int):
        """
        Parameters:
        -----------
        state_size
            type: int

        Returns:
        --------
        None, instantiates class.
        """
        super().__init__()
        self.add_module("psi", torch.nn.Linear(state_size, 1, bias=False))

    def gradient(self, ψ, y):
        """
        Compute the gradient of ψ with respect to y.
        
        Parameters:
        -----------
        ψ : torch.Tensor
            The potential value, typically output from a potential network.
        y : torch.Tensor
            The input tensor with respect to which the gradient is computed.
            
        Returns:
        --------
        torch.Tensor
            The gradient of ψ with respect to y.
        """
        return torch.autograd.grad(ψ, y, torch.ones_like(ψ), create_graph=True)[0]

    def potential_gradient(self, y):
        """
        Compute the gradient of the potential with respect to the input.
        
        Parameters:
        -----------
        y : torch.Tensor
            Input tensor, typically the output of a neural network.
            
        Returns:
        --------
        torch.Tensor
            The gradient of the potential with respect to y.
        """
        y = y.requires_grad_()
        return self.gradient(self.psi(y), y)
    
    def __call__(self, y: torch.Tensor) -> torch.Tensor:
        """
        Apply the potential transformation to the input tensor.
        
        Parameters:
        -----------
        y : torch.Tensor
            Input tensor to transform into a potential value.
            
        Returns:
        --------
        torch.Tensor
            A 1-dimensional potential value.
        """
        return self.psi(y.requires_grad_())