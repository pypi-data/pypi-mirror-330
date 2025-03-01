
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
class TorchNet(torch.nn.Sequential, ABCParse.ABCParse):
        
    """        
    Notes:
    ------
    (1) No need to define forward() method as it is already handled by nn.Sequential
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
    ):
        """
        in_features
        out_features
        hidden
        activation
        dropout
        bias
        output_bias
        """

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

        super().__init__(*layers)
        self._rename_nn_sequential_inplace(self, self._names)

    def _rename_nn_sequential_inplace(
        self, sequential: torch.nn.Sequential, names: List[str]
    ) -> None:
        
        new_modules = collections.OrderedDict()
        
        for i, (k, v) in enumerate(sequential._modules.items()):
            new_modules[names[i]] = v

        sequential._modules = new_modules

    @property
    def _building_list(self) -> List[str]:
        
        return ["hidden", "activation", "bias", "dropout"]
    
    @property
    def potential_net(self)->bool:
        
        output_shape = [p.shape for p in list(self.parameters())][-1][0]
        return (output_shape == 1)

    def stack(self) -> None:
        
        for key, val in self._PARAMS.items():
            if key in self._building_list:
                val = self.config.layerwise_attributes(self._PARAMS[key])
                setattr(self, key, val)

    def _build_hidden_layer(self, in_dim, out_dim, n):
        
        return LayerBuilder()(
            in_features=in_dim,
            out_features=out_dim,
            activation=self.activation[n],
            bias=self.bias[n],
            dropout=self.dropout[n],
        )

    def _build_output_layer(self, in_dim, out_dim):
        
        return LayerBuilder()(
            in_features=in_dim,
            out_features=out_dim,
            bias=self._output_bias,
        )

    def _build_net(self) -> Dict:
        
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
        """Convert to list, if not already"""
        if isinstance(input, list):
            return input
        return [input]
