
# -- import packages: ----------------------------------------------------------
import torch


# -- main module class: --------------------------------------------------------
class ActivationFunctionConfig:
    def __init__(self):
        self._msg = "Must pass torch.nn.<function> or a string that fetches a torch.nn.<function>"

    def check_str(self, func):
        return isinstance(func, str)

    def from_str(self, func_str):
        return getattr(torch.nn, func_str)()

    def check_torch_module_callable(self, func):
        return isinstance(func, torch.nn.Module)

    def from_torch_module_callable(self, func):
        return func

    def check_torch_module(self, func):
        return isinstance(func(), torch.nn.Module)

    def from_torch_module(self, func):
        return func()

    def __call__(self, func):
        if self.check_str(func):
            return self.from_str(func)
        if self.check_torch_module_callable(func):
            return self.from_torch_module_callable(func)
        if self.check_torch_module(func):
            return self.from_torch_module(func)

        print(self._msg)
