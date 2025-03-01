
__module_name__ = "_layer.py"
__doc__ = """Layer module."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])


# -- import packages: ----------------------------------------------------------
from typing import List, Union, Type, Callable
from collections import OrderedDict
import ABCParse
import torch


# -- import local dependencies: ------------------------------------------------
from .config._activation_function_config import ActivationFunctionConfig


# -- set typing: ---------------------------------------------------------------
ActivationFunction = Type[Callable[torch.nn.modules.activation, torch.Tensor]]


# -- Layer module: -------------------------------------------------------------
class LayerBuilder(ABCParse.ABCParse):
    def __init__(self, name: str = "") -> None:

        """
        Container for a single linear layer for a torch neural network,
        often an essential building block of torch.nn.Sequential or
        torch.nn.Module.
        
        Parameters:
        -----------
        in_features
            Size of layer input.
            type: int
        
        out_features
            Size of layer output.
            type: int
        
        activation
            If passed, defines appended activation function.
            type: 'torch.nn.modules.activation.<func>'
            default: None
        
        bias
            Indicate if the layer should not learn an additive bias.
            type: bool
            default: True
            
        dropout
            If > 0, append dropout layer with probablity p, where p = dropout.
            type: float
            default: 0
        
        name [Optional]
            Name of the layer. If defined, specified within torch.nn.Sequential.
            Layer name.
            type: str
                    
        Returns:
        --------
        None, instantiates Layer class.
        
        Notes:
        ------
        (1) General flow assumed is: Linear -> Dropout -> Activation
        """
        
        super(LayerBuilder, self).__init__()        
        setattr(self, "__name__", name)
                
    # -- core properties: ----------------------------------------------------------------
    @property
    def linear(self)->torch.nn.modules.linear.Linear:
        """torch.nn.Linear layer"""
        return torch.nn.Linear(
            in_features=self._in_features,
            out_features=self._out_features,
            bias=self._bias,
        )

    @property
    def dropout(self)->torch.nn.modules.dropout.Dropout:
        """torch.nn.Dropout layer."""
        if self._dropout:
            return torch.nn.Dropout(self._dropout)
        
    @property
    def activation(self) -> ActivationFunction:
        """torch.nn.<activation> layer"""
        if self._activation:
            return self._configure_activation(self._activation)
        
    @property
    def layer_attrs(self) -> List[str]:
        return ['linear', 'dropout', 'activation']
        
    # -- called: -------------------------------------------------------------------------
    def __collect_attributes__(self) -> None:
        """Collect passed layer and optionally dropout, activation."""
        
        for attr in self.layer_attrs:
            if not getattr(self, attr) is None:
                if self.__name__:
                    attr_name = "_".join([self.__name__, attr])
                else:
                    attr_name = attr
                yield (attr_name, getattr(self, attr))
    

    @property
    def layer(self)-> torch.nn.Sequential:
        """
        Generate layer from arguments passed to __init__() and processed with supporting
        functions.
        
        Returns:
        --------
        Layer
            Composed layer
            type: torch.nn.Sequential
        """
        
        if not hasattr(self, "_assembled"):
            self._assembled = torch.nn.Sequential(OrderedDict(self.__collect_attributes__()))
        return self._assembled
    
    def __call__(
        self,
        in_features: int,
        out_features: int,
        activation: Union[None, ActivationFunction] = None,
        bias: bool = True,
        dropout: Union[None, float] = 0,
    )->torch.nn.Sequential:
        
        """
        Return Layer.
        
        Parameters:
        -----------
        in_features
            Size of layer input.
            type: int
        
        out_features
            Size of layer output.
            type: int
        
        activation
            If passed, defines appended activation function.
            type: 'torch.nn.modules.activation.<func>'
            default: None
        
        bias
            Indicate if the layer should not learn an additive bias.
            type: bool
            default: True
            
        dropout
            If > 0, append dropout layer with probablity p, where p = dropout.
            type: float
            default: 0
            
        Returns:
        --------
        layer
            type: torch.nn.Sequential
        """
        
        self.__parse__(kwargs=locals(), public=[None]) # ignore=["name"],
        self._configure_activation = ActivationFunctionConfig()
        
        return self.layer
    
    def __repr__(self)->str:
        return "LayerBuilder"
