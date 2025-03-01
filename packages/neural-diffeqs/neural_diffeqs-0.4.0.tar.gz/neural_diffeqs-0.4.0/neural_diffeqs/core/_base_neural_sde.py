import ABCParse
from abc import abstractmethod


from ._base_neural_diffeq import BaseDiffEq
from ._diffeq_config import DiffEqConfig


class BaseSDE(BaseDiffEq):
    """Base class for Stochastic Differential Equation (SDE) models.
    
    This abstract class provides the foundation for implementing neural SDE models.
    It extends the BaseDiffEq class and specializes in stochastic differential equations
    with both drift (mu) and diffusion (sigma) terms.
    
    Attributes:
        DIFFEQ_TYPE (str): Identifier for the differential equation type, set to "SDE".
        mu: Neural network that parameterizes the drift term.
        sigma: Neural network that parameterizes the diffusion term.
        noise_type (str): Type of noise used in the SDE (e.g., "diagonal", "scalar").
        sde_type (str): Type of SDE (e.g., "ito", "stratonovich").
    """
    DIFFEQ_TYPE = "SDE"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the SDE model.
        
        Note:
            Inheriting classes must call self.__config__(locals()) in their __init__ method
            to properly configure the drift and diffusion terms.
            
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. These should include parameters for
                      configuring the neural networks that parameterize the drift and
                      diffusion terms, as well as 'noise_type' and 'sde_type'.
        """
        super().__init__()

    def __config__(self, kwargs):
        """Configure the SDE model with the provided parameters.
        
        This method sets up the drift (mu) and diffusion (sigma) neural networks
        based on the configuration parameters.
        
        Args:
            kwargs (dict): Dictionary of parameters, typically from locals() in the
                          inheriting class's __init__ method. Should include parameters
                          for DiffEqConfig as well as 'noise_type' and 'sde_type'.
        """
        self.__parse__(kwargs=kwargs, public = ['noise_type', 'sde_type'])

        self._config_kwargs = ABCParse.function_kwargs(func=DiffEqConfig, kwargs=kwargs)
        configs = DiffEqConfig(**self._config_kwargs)

        self.mu = configs.mu
        self.sigma = configs.sigma

    # -- required methods in child classes: ------------------------------------
    @abstractmethod
    def drift(self):
        """Calculate the drift term of the SDE.
        
        This abstract method must be implemented by child classes to define
        the drift component of the SDE.
        
        Returns:
            torch.Tensor: The drift term evaluated at the current state.
        """
        ...

    @abstractmethod
    def diffusion(self):
        """Calculate the diffusion term of the SDE.
        
        This abstract method must be implemented by child classes to define
        the diffusion component of the SDE.
        
        Returns:
            torch.Tensor: The diffusion term evaluated at the current state.
        """
        ...
