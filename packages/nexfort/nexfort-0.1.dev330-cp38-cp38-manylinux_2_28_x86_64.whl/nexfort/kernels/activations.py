
import enum
from functools import partial
import torch
import triton
import triton.language as tl
from torch import nn
import nexfort_codegen_extension
if hasattr(tl.math, 'tanh'):
    libdevice = tl.math
elif (torch.version.cuda is not None):
    libdevice = tl.extra.cuda.libdevice
else:
    raise RuntimeError('No available math implementation')

class ActivationType(enum.Enum):
    GELU = enum.auto()
    GELU_TANH = enum.auto()
    SILU = enum.auto()
    RELU = enum.auto()
    TANH = enum.auto()
    SIGMOID = enum.auto()
    GELU_QUICK = enum.auto()
    IDENTITY = enum.auto()
ActivationType: tl.constexpr
_ActivationType2TorchMethod = {ActivationType.GELU: partial(nn.functional.gelu, approximate='none'), ActivationType.GELU_TANH: partial(nn.functional.gelu, approximate='tanh'), ActivationType.SILU: nn.functional.silu, ActivationType.RELU: nn.functional.relu, ActivationType.TANH: nn.functional.tanh, ActivationType.SIGMOID: nn.functional.sigmoid, ActivationType.IDENTITY: nn.Identity()}
_TorchMethod2ActivationType = {'SiLU()': ActivationType.SILU, 'ReLU()': ActivationType.RELU, "GELU(approximate='none')": ActivationType.GELU, "GELU(approximate='tanh')": ActivationType.GELU_TANH}

def torch_module2_act_type(obj):
    if isinstance(obj, nn.ReLU):
        return ActivationType.RELU
    elif isinstance(obj, nn.SiLU):
        return ActivationType.SILU
    elif isinstance(obj, nn.GELU):
        if (obj.approximate == 'gelu_tanh'):
            return ActivationType.GELU_TANH
        else:
            return ActivationType.GELU
    else:
        raise ValueError(f'Unknown activation type: {obj}')

@triton.jit
def _nexfort_triton_activation_implementation(method: tl.constexpr, x):
    tl.static_assert(False, 'placeholder')
