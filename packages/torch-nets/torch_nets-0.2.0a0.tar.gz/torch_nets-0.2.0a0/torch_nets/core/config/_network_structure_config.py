
# -- import packages: -------------------------------------------------
import ABCParse
from typing import Union, Any, Dict


class NetworkStructureConfig(ABCParse.ABCParse):
    def __init__(self):
        
        self._TorchNetDict = {}

    def _as_list(self, input: Union[list, Any]):
        """Convert to list, if not already"""
        if isinstance(input, list):
            return input
        return [input]

    @property
    def layer_names(self):
        return ["hidden_{}".format(i + 1) for i in range(self._n_hidden)] + ["output"]

    @property
    def structure(self):
        return [self._in_features] + self._hidden + [self._out_features]

    def __call__(self, in_features, out_features, hidden) -> Dict:
        
        """Build layered neural network structure"""
        
        self.__parse__(kwargs=locals(), public=[None])

        self._hidden = self._as_list(self._hidden)
        self._n_hidden = len(self._hidden)

        for n, (i, j) in enumerate(zip(self.structure[:-1], self.structure[1:])):
            self._TorchNetDict[self.layer_names[n]] = (i, j)

        return self._TorchNetDict