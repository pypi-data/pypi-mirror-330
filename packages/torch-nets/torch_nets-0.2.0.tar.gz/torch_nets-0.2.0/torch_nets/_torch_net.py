# -- import packages: ---------------------------------------------------------
import ABCParse
import collections
import torch


# -- import local dependencies: -----------------------------------------------
from .core.config import Config
from .core import LayerBuilder


# -- set typing: --------------------------------------------------------------
from typing import Union, List, Any, Dict


# -- API-facing class: --------------------------------------------------------
class TorchNet(ABCParse.ABCParse, torch.nn.Sequential):
        
    """
    A flexible PyTorch neural network implementation that extends torch.nn.Sequential.
    
    TorchNet provides a high-level API for creating customizable neural networks
    with configurable hidden layers, activation functions, and dropout rates.
    The implementation automatically handles the construction of the network
    architecture based on the provided parameters.
    
    This class inherits from both ABCParse.ABCParse for parameter parsing and
    torch.nn.Sequential for the neural network functionality.
        
    Notes:
    ------
    No need to define forward() method as it is already handled by nn.Sequential.
    """
    def __init__(
        self,
        in_features: int,
        out_features: int,
        hidden: Union[List[int], int] = [],
        activation: Union[str, List[str]] = "LeakyReLU",
        dropout: Union[float, List[float]] = 0.2,
        bias: bool = True,
        output_bias: bool = True,
    ) -> None:
        """
        Initialize a TorchNet neural network.
        
        Parameters
        ----------
        in_features : int
            Number of input features/dimensions for the network.
        
        out_features : int
            Number of output features/dimensions for the network.
        
        hidden : Union[List[int], int], optional
            Hidden layer dimensions. Can be a single integer or a list of integers.
            Each integer specifies the number of neurons in a hidden layer.
            Default is an empty list (no hidden layers).
        
        activation : Union[str, List[str]], optional
            Activation function(s) to use in the hidden layers.
            Can be a single string or a list of strings for layer-specific activations.
            Default is "LeakyReLU".
        
        dropout : Union[float, List[float]], optional
            Dropout rate(s) to apply after hidden layers.
            Can be a single float or a list of floats for layer-specific dropout rates.
            Default is 0.2.
        
        bias : bool, optional
            Whether to include bias terms in the hidden layers.
            Default is True.
        
        output_bias : bool, optional
            Whether to include a bias term in the output layer.
            Default is True.
        """
        
        # Initialize torch.nn.Sequential first with empty layers
        torch.nn.Sequential.__init__(self)
        
        # Then parse the arguments
        self.__parse__(locals())

        self.config = Config(
            in_features = self._in_features,
            out_features = self._out_features,
            hidden = self._hidden,
        )

        self._names, layers = [], []
        _net = self._build_net()

        for i, (_name, _layer) in enumerate(_net.items()):
            layers.append(_layer)
            self._names.append(_name)
        
        # Add the layers to the Sequential
        for layer in layers:
            self.add_module(str(len(self)), layer)
            
        # Rename the modules
        self._rename_nn_sequential_inplace(self, self._names)

    def _rename_nn_sequential_inplace(
        self, sequential: torch.nn.Sequential, names: List[str]
    ) -> None:
        """
        Rename the modules in a Sequential container in-place.
        
        Parameters
        ----------
        sequential : torch.nn.Sequential
            The Sequential container whose modules will be renamed.
        
        names : List[str]
            List of names to assign to the modules.
        """
        
        new_modules = collections.OrderedDict()
        
        for i, (k, v) in enumerate(sequential._modules.items()):
            new_modules[names[i]] = v

        sequential._modules = new_modules

    @property
    def _building_list(self) -> List[str]:
        """
        List of parameter names that are used for building the network layers.
        
        Returns
        -------
        List[str]
            List of parameter names.
        """
        
        return ["hidden", "activation", "bias", "dropout"]
    
    @property
    def potential_net(self) -> bool:
        """
        Check if the network has a single output neuron, which might indicate
        a potential network (e.g., for binary classification).
        
        Returns
        -------
        bool
            True if the output layer has a single neuron, False otherwise.
        """
        
        output_shape = [p.shape for p in list(self.parameters())][-1][0]
        return (output_shape == 1)

    def stack(self) -> None:
        """
        Process and stack layer-wise attributes.
        
        This method ensures that parameters like activation, bias, and dropout
        are properly formatted for each layer in the network.
        """
        
        for key, val in self._PARAMS.items():
            if key in self._building_list:
                val = self.config.layerwise_attributes(self._PARAMS[key])
                setattr(self, key, val)

    def _build_hidden_layer(self, in_dim, out_dim, n):
        """
        Build a hidden layer with the specified dimensions and attributes.
        
        Parameters
        ----------
        in_dim : int
            Input dimension for the layer.
        
        out_dim : int
            Output dimension for the layer.
        
        n : int
            Index of the layer, used to select the appropriate activation,
            bias, and dropout values.
        
        Returns
        -------
        torch.nn.Sequential
            A Sequential container with the constructed layer.
        """
        
        return LayerBuilder()(
            in_features=in_dim,
            out_features=out_dim,
            activation=self.activation[n],
            bias=self.bias[n],
            dropout=self.dropout[n],
        )

    def _build_output_layer(self, in_dim, out_dim):
        """
        Build the output layer with the specified dimensions.
        
        Parameters
        ----------
        in_dim : int
            Input dimension for the layer.
        
        out_dim : int
            Output dimension for the layer.
        
        Returns
        -------
        torch.nn.Sequential
            A Sequential container with the constructed output layer.
        """
        
        return LayerBuilder()(
            in_features=in_dim,
            out_features=out_dim,
            bias=self._output_bias,
        )

    def _build_net(self) -> Dict:
        """
        Build the complete neural network architecture.
        
        This method constructs all layers of the network based on the
        configuration and returns them as a dictionary.
        
        Returns
        -------
        Dict
            Dictionary mapping layer names to layer objects.
        """
        
        self.stack()

        TorchNetDict = {}

        for n, (layer_name, (in_dim, out_dim)) in enumerate(
            self.config.network_structure.items()
        ):
                  
            if layer_name == "output":
                TorchNetDict[layer_name] = self._build_output_layer(in_dim, out_dim)
            else:
                TorchNetDict[layer_name] = self._build_hidden_layer(in_dim, out_dim, n)

        return TorchNetDict
    
    def _as_list(self, input: Union[list, Any]):
        """
        Convert input to a list if it's not already a list.
        
        Parameters
        ----------
        input : Union[list, Any]
            The input to convert.
        
        Returns
        -------
        list
            The input as a list.
        """
        if isinstance(input, list):
            return input
        return [input]
