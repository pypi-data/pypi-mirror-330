
# -- import packages: ---------------------------------------------------------
import ABCParse
import torch


# -- import local dependencies: -----------------------------------------------
from ._layer_wise_attributes_config import LayerWiseAttributesConfig
from ._activation_function_config import ActivationFunctionConfig
from ._network_structure_config import NetworkStructureConfig


# -- set typing: --------------------------------------------------------------
from typing import List, Dict, Tuple, Type, Callable
ActivationFunction = Type[Callable[torch.nn.modules.activation, torch.Tensor]]


# -- operator class: ----------------------------------------------------------
class Config(ABCParse.ABCParse):
    def __init__(self, in_features: int, out_features: int, hidden: List[int]):
        
        self.__parse__(locals())
        
        self._NETWORK_STRUCTURE = NetworkStructureConfig()
        self._ACTIVATION_FUNCTION = ActivationFunctionConfig()
        self._LAYERWISE_ATTRIBUTES = LayerWiseAttributesConfig(
            n_hidden=self.n_hidden
        )

    @property
    def n_hidden(self) -> int:
        return len(self._hidden)

    @property
    def activation_function(self) -> ActivationFunction:
        return self._ACTIVATION_FUNCTION

    @property
    def network_structure(self) -> Dict[str, Tuple[int]]:
        return self._NETWORK_STRUCTURE(
            self._in_features, self._out_features, self._hidden,
        )

    @property
    def layerwise_attributes(self):
        return self._LAYERWISE_ATTRIBUTES
