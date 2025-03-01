# -- import packages: ---------------------------------------------------------
import collections
import numpy as np

# -- import local modules: ----------------------------------------------------
from .._torch_net import TorchNet

# -- set type hints: ----------------------------------------------------------
from typing import List


# -- operational cls: ---------------------------------------------------------
class InferredNetworkArchitecture:
    """
    Notes:
    ------
    (1) Assumes structure to always be: [input, [wa, b, wb], ..., [wa, b, wb], [out_w, (out_b)]
    (2) assumes bias is True for all hidden (i.e., forming triplets.) Can expand / refactor if
        necessary. Currently an edge case if False.
    """

    def __init__(self, state_dict: collections.OrderedDict) -> None:
        self.state_dict = state_dict

    def _get_network_param_sizes(self) -> list:
        param_sizes = []
        for key, val in self.state_dict.items():
            param_sizes += list(val.shape)[::-1]
        return param_sizes

    @property
    def param_sizes(self) -> List:
        return self._get_network_param_sizes()

    @property
    def output_bias(self):
        return (len(self.param_sizes[1:]) - 2) % 3 == 0

    @property
    def in_features(self):
        return self.param_sizes[0]

    @property
    def out_features(self):
        if self.output_bias:
            return np.unique(self.param_sizes[-2:])[0]
        return np.unique(self.param_sizes[-1:])[0]

    @property
    def n_hidden(self):
        _n_hidden = len(self.hidden_param_sizes) / 3
        if (int(_n_hidden) - _n_hidden) == 0:
            return int(_n_hidden)
        raise ValueError("Invalid architecture")

    @property
    def hidden_param_sizes(self):
        if self.output_bias:
            return self.param_sizes[1:-2]
        return self.param_sizes[1:-1]

    @property
    def hidden(self):
        return np.unique(
            np.stack(
                [self.hidden_param_sizes[(n * 3) : (n * 3) + 3] for n in range(self.n_hidden)]
            ),
            axis=1,
        ).flatten().tolist()

    @property
    def bias(self):
        return [True] * self.n_hidden

    def __call__(self):

        """
        param_sizes = _get_network_param_sizes(state_dict)

        output_bias = _has_output_bias(param_sizes)
        n_hidden, hidden_param_sizes, out_features = _extract_hidden_layers(
            param_sizes, output_bias
        )
        """

        return {
            "in_features": self.in_features,
            "out_features": self.out_features,
            "hidden": self.hidden,
            "bias": self.bias,
            "output_bias": self.output_bias,
        }


def infer_network_architecture_from_state(
    state_dict: collections.OrderedDict,
    dropout: List[float] = [0],
    activation: List[str] = ["LeakyReLU"],
) -> TorchNet:
    """You still need to provide dropout and activation structures."""
    arch = InferredNetworkArchitecture(state_dict)
    return TorchNet(dropout=dropout, activation=activation, **arch())
