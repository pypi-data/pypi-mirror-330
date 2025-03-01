
__module_name__ = "_decoder.py"
__doc__ = """Main user-facing API for torch.nn.Sequential Decoders."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])


# -- import packages: ---------------------------------------------------------
from typing import List, Union


# -- import local dependencies: -----------------------------------------------
from ._torch_net import TorchNet
from .core import power_space


# -- API-facing class: --------------------------------------------------------
class Decoder(TorchNet):
    """Class derived from TorchNet for constructing a decoder network."""
    def __init__(
        self,
        data_dim: int,
        latent_dim: int,
        n_hidden: int = 3,
        power: float = 2,
        activation: Union[str, List[str]] = "LeakyReLU",
        dropout: Union[float, List[float]] = 0.2,
        bias: bool = True,
        output_bias: bool = True,
    ) -> None:
        """
        Parameters:
        -----------
        data_dim
            Size of layer input.
            type: int

        latent_dim
            Size of layer output.
            type: int

        n_hidden
            Number of hidden layers
            type: int
            
        power
            exponent at which layer size changes.
            type: float

        activation
            If passed, defines appended activation function.
            type: 'torch.nn.modules.activation.<func>'
            default: None

        dropout
            If > 0, append dropout layer with probablity p, where p = dropout.
            type: float
            default: 0

        bias
            Indicate if the layer should/should not learn an additive bias.
            type: bool
            default: True

        output_bias
            Indicate if the output layer should/should not learn an
            additive bias.
            type: bool
            defualt: True


        Returns:
        --------
        TorchNet
            Neural network block. To be accepted into a torch.nn.Module object.
            type: torch.nn.Sequential

        Notes:
        ------
        (1) For params: 'activation', 'bias', and 'dropout': if more
            params than necessary are passed, they will go unused.
        """

        hidden = power_space(
            start=latent_dim, stop=data_dim, n=n_hidden + 2, power=power
        )[1:-1].tolist()

        super().__init__(
            in_features=latent_dim,
            out_features=data_dim,
            hidden=hidden,
            activation=activation,
            dropout=dropout,
            bias=bias,
            output_bias=output_bias,
        )
