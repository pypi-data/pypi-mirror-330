import enum
import os
from functools import wraps
from typing import Union
import torch
import triton
import triton.language as tl
import nexfort_codegen_extension
from ..utils.env_var import parse_boolean_from_env
from .activations import _ActivationType2TorchMethod, _nexfort_triton_activation_implementation, ActivationType
MAX_FP8_E4M3 = torch.finfo(torch.float8_e4m3fn).max
MIN_FP8_E4M3 = torch.finfo(torch.float8_e4m3fn).min
E5M2_MAX_POS = torch.finfo(torch.float8_e5m2).max
E5M2_MIN_POS = torch.finfo(torch.float8_e5m2).min
STR2DTYPE = {'float8_e4m3fn': torch.float8_e4m3fn, 'float8_e5m2': torch.float8_e5m2, 'int8': torch.int8}
DTYPE_INFO = {torch.float8_e4m3fn: (torch.finfo(torch.float8_e4m3fn).min, torch.finfo(torch.float8_e4m3fn).max), torch.float8_e5m2: (torch.finfo(torch.float8_e5m2).min, torch.finfo(torch.float8_e5m2).max), torch.int8: (torch.iinfo(torch.int8).min, torch.iinfo(torch.int8).max)}
EPS = {torch.bfloat16: 1e-12, torch.float16: torch.finfo(torch.float16).tiny}
_TORCH_DTYPE_TO_TRITON_DTYPE = {torch.float64: tl.float64, torch.float: tl.float32, torch.float16: tl.float16, torch.float8_e4m3fn: tl.float8e4nv, torch.float8_e5m2: tl.float8e5, torch.int32: tl.int32, torch.int8: tl.int8}

class QuantType(enum.Enum):
    PER_TOKEN = 'per_token'
    PER_TENSOR = 'per_tensor'
    PER_BLOCK = 'per_block'
    CAST = 'cast'
TRITON_GE_V3: tl.constexpr = triton.__version__ >= '3.0.0'

def with_cuda_ctx(fn):

    @wraps(fn)
    def decorated(*args, **kwargs):
        assert isinstance(args[0], (torch.Tensor, torch.nn.Parameter))
        with torch.cuda.device(args[0].device):
            return fn(*args, **kwargs)
    return decorated

@triton.jit
def _nexfort_clamp_min_2_0(x, min_val):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _nexfort_clamp_max_2_0(x, max_val):
    tl.static_assert(False, 'placeholder')

@triton.jit
def _nexfort_clamp_2_0(x, min_val, max_val):
    tl.static_assert(False, 'placeholder')
if TRITON_GE_V3:

    @triton.jit
    def _nexfort_clamp_min_3_0(x, min_val):
        tl.static_assert(False, 'placeholder')

    @triton.jit
    def _nexfort_clamp_max_3_0(x, max_val):
        tl.static_assert(False, 'placeholder')

    @triton.jit
    def _nexfort_clamp_3_0(x, min_val, max_val):
        tl.static_assert(False, 'placeholder')

@triton.jit
def _nexfort_deprecated_nexfort_per_tensor_quantize_kernel(x_ptr, max_ptr, y_ptr, scale_ptr, n_elements, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@with_cuda_ctx
def deprecated_per_tensor_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    x = _ActivationType2TorchMethod[act_method](x)
    max_val = x.abs().amax()
    scale = torch.empty(1, dtype=torch.float32, device=x.device)
    y = torch.empty(x.size(), dtype=quant_dtype, device=x.device)
    N = x.shape[-1]
    n_elements = x.numel()
    BLOCK_SIZE = min(triton.next_power_of_2(N), 8192)
    grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']),)
    num_warps = 4 if BLOCK_SIZE < 2048 else 8 if BLOCK_SIZE < 4096 else 16
    _nexfort_deprecated_nexfort_per_tensor_quantize_kernel[grid](x, max_val, y, scale, n_elements, q_min, q_max, eps=eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, TRITON_V3=TRITON_GE_V3, num_warps=num_warps)
    return (y, scale)

@triton.jit
def _nexfort_per_tensor_quantize_kernel(x_ptr, max_ptr, y_ptr, scale_ptr, x_stride_b, x_stride_h, x_stride_m, x_stride_c, y_stride_b, y_stride_h, y_stride_m, y_stride_n, N, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@with_cuda_ctx
def per_tensor_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    x = _ActivationType2TorchMethod[act_method](x)
    max_val = x.abs().amax()
    scale = torch.empty(1, dtype=torch.float32, device=x.device)
    out_shape = x.shape
    y = torch.empty(out_shape, device=x.device, dtype=quant_dtype)
    dims = x.dim()
    if dims == 4:
        B, H, M, N = x.shape
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_xh = x.stride(1)
        stride_yh = y.stride(1)
    elif dims == 3:
        B = 1
        H, M, N = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_xh = x.stride(0)
        stride_yh = y.stride(0)
    elif dims == 2:
        B = 1
        H = 1
        M, N = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_xh = 0
        stride_yh = 0
    else:
        raise NotImplementedError('Only support 2-D or 3-D tensor for now!')
    BLOCK_SIZE = triton.next_power_of_2(N)
    _nexfort_per_tensor_quantize_kernel[M, H, B](x, max_val, y, scale, stride_xb, stride_xh, x.stride(-2), x.stride(-1), stride_yb, stride_yh, y.stride(-2), y.stride(-1), N, q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, TRITON_V3=TRITON_GE_V3)
    return (y, scale)

@triton.jit
def _nexfort_deprecated_per_token_quantize_kernel(x_ptr, y_ptr, scale_ptr, x_stride_m, x_stride_c, y_stride_m, y_stride_n, scale_stride, N, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@with_cuda_ctx
def deprecated_per_token_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    x = _ActivationType2TorchMethod[act_method](x)
    out_shape = x.shape
    scale_shape = x.shape[:-1] + (1,)
    x = x.reshape(-1, out_shape[-1])
    M, N = x.shape
    y = torch.empty((M, N), device=x.device, dtype=quant_dtype)
    scale = torch.empty((M,), device=x.device, dtype=torch.float32)
    BLOCK_SIZE = triton.next_power_of_2(N)
    _nexfort_deprecated_per_token_quantize_kernel[M,](x, y, scale, x.stride(0), x.stride(1), y.stride(0), y.stride(1), scale.stride(0), N, q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, ACTIVATION_METHOD=ActivationType.IDENTITY, TRITON_V3=TRITON_GE_V3)
    return (y.view(out_shape), scale.view(scale_shape))

@triton.jit
def _nexfort_per_token_quantize_kernel(x_ptr, y_ptr, scale_ptr, x_stride_b, x_stride_h, x_stride_m, x_stride_c, y_stride_b, y_stride_h, y_stride_m, y_stride_n, scale_stride_b, scale_stride_h, scale_stride, N, q_min, q_max, eps, out_dtype: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@with_cuda_ctx
def per_token_quantize(x, quant_dtype, q_min, q_max, eps, act_method=ActivationType.IDENTITY):
    out_shape = x.shape
    scale_shape = x.shape[:-1] + (1,)
    y = torch.empty(out_shape, device=x.device, dtype=quant_dtype)
    scale = torch.empty(scale_shape, device=x.device, dtype=torch.float32)
    dims = x.dim()
    if dims == 4:
        B, H, M, N = x.shape
        stride_xb = x.stride(0)
        stride_yb = y.stride(0)
        stride_sb = scale.stride(0)
        stride_xh = x.stride(1)
        stride_yh = y.stride(1)
        stride_sh = scale.stride(1)
    elif dims == 3:
        B = 1
        H, M, N = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_sb = 0
        stride_xh = x.stride(0)
        stride_yh = y.stride(0)
        stride_sh = scale.stride(0)
    elif dims == 2:
        B = 1
        H = 1
        M, N = x.shape
        stride_xb = 0
        stride_yb = 0
        stride_sb = 0
        stride_xh = 0
        stride_yh = 0
        stride_sh = 0
    else:
        raise NotImplementedError('Only support 2-D or 3-D tensor for now!')
    BLOCK_SIZE = triton.next_power_of_2(N)
    _nexfort_per_token_quantize_kernel[M, H, B](x, y, scale, stride_xb, stride_xh, x.stride(-2), x.stride(-1), stride_yb, stride_yh, y.stride(-2), y.stride(-1), stride_sb, stride_sh, scale.stride(-2), N, q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], BLOCK_SIZE=BLOCK_SIZE, ACTIVATION_METHOD=act_method, TRITON_V3=TRITON_GE_V3)
    return (y, scale)

@triton.jit
def _nexfort_per_block_quantize_kernel(x_ptr, y_ptr, scale_ptr, M, x_stride_b, x_stride_h, x_stride_m, x_stride_k, y_stride_b, y_stride_h, y_stride_m, y_stride_k, scale_stride_b, scale_stride_h, scale_stride_m, q_min, q_max, eps, out_dtype: tl.constexpr, HEAD_DIM: tl.constexpr, BLOCK_SIZE: tl.constexpr, ACTIVATION_METHOD: tl.constexpr, TRITON_V3: tl.constexpr):
    tl.static_assert(False, 'placeholder')

@with_cuda_ctx
def per_block_quantize(x, quant_dtype, q_min, q_max, eps, block_size, act_method=ActivationType.IDENTITY):
    dims = x.dim()
    assert dims == 4, 'Only support 4-D tensor for per_block quantization!'
    B, H, M, K = x.shape
    block_num = (M + block_size - 1) // block_size
    y = torch.empty((B, H, M, K), device=x.device, dtype=quant_dtype)
    scale = torch.empty((B, H, block_num), device=x.device, dtype=torch.float32)
    _nexfort_per_block_quantize_kernel[block_num, H, B](x, y, scale, M, x.stride(0), x.stride(1), x.stride(2), x.stride(3), y.stride(0), y.stride(1), y.stride(2), y.stride(3), scale.stride(0), scale.stride(1), scale.stride(2), q_min, q_max, eps, out_dtype=_TORCH_DTYPE_TO_TRITON_DTYPE[quant_dtype], HEAD_DIM=K, BLOCK_SIZE=block_size, ACTIVATION_METHOD=act_method, TRITON_V3=TRITON_GE_V3)
    return (y, scale)

def quantize(x: Union[torch.HalfTensor, torch.BFloat16Tensor], *, quant_dtype: torch.dtype=torch.float8_e4m3fn, quant_type: QuantType=QuantType.PER_TENSOR, block_size: int=1):
    q_min, q_max = DTYPE_INFO[quant_dtype]
    if quant_type == QuantType.PER_TENSOR:
        quantized_x, scale = per_tensor_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype])
    elif quant_type == QuantType.PER_TOKEN:
        quantized_x, scale = per_token_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype])
    elif quant_type == QuantType.PER_BLOCK:
        quantized_x, scale = per_block_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype], block_size=block_size)
    elif quant_type == QuantType.CAST:
        quantized_x = x.to(quant_dtype)
        scale = None
    else:
        raise ValueError(f'quant_type={quant_type!r} is invaild value!')
    return (quantized_x, scale)

def act_and_quantize(x: Union[torch.HalfTensor, torch.BFloat16Tensor], *, quant_dtype: torch.dtype=torch.float8_e4m3fn, quant_type: QuantType=QuantType.PER_TENSOR, act_method: ActivationType=ActivationType.IDENTITY, block_size: int=1):
    q_min, q_max = DTYPE_INFO[quant_dtype]
    if quant_type == QuantType.PER_TENSOR:
        quantized_x, scale = per_tensor_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype], act_method=act_method)
    elif quant_type == QuantType.PER_TOKEN:
        quantized_x, scale = per_token_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype], act_method=act_method)
    elif quant_type == QuantType.PER_BLOCK:
        quantized_x, scale = per_block_quantize(x, quant_dtype, q_min, q_max, EPS[x.dtype], block_size=block_size, act_method=act_method)
    elif quant_type == QuantType.CAST:
        quantized_x = _ActivationType2TorchMethod[act_method](x).to(quant_dtype)
        scale = None
    else:
        raise ValueError(f'quant_type={quant_type!r} is invaild value!')
    return (quantized_x, scale)

def acc_type(dtype, allow_low_precision=True):
    if dtype == torch.float16:
        if allow_low_precision and torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction and (torch.version.hip is None):
            return tl.float16
        else:
            return tl.float32
    elif dtype == torch.bfloat16:
        return tl.float32
    elif dtype == torch.float8_e4m3fn or dtype == torch.float8_e5m2:
        return tl.float32
    elif dtype == torch.int8:
        return tl.int32
    else:
        return getattr(tl, f'{dtype}'.replace('torch.', ''))

def enabled_triton_autotune_cache():
    return parse_boolean_from_env('NEXFORT_ENABLE_TRITON_AUTOTUNE_CACHE', default_value=True)

def force_torch_flash_attention():
    return parse_boolean_from_env('NEXFORT_FORCE_TORCH_FLASH_ATTENTION', default_value=False)

def force_cast_value_to_fp16_in_attention():
    return parse_boolean_from_env('NEXFORT_FORCE_CAST_VALUE_TO_FP16_IN_ATTENTION', default_value=False)

def enabled_quantize_attention():
    return parse_boolean_from_env('NEXFORT_ENABLE_QUANTIZE_ATTENTION', default_value=True)

def enabled_fuse_attention_fp16_reduction():
    return parse_boolean_from_env('NEXFORT_ENABLE_FUSE_ATTENTION_FP16_REDUCTION', default_value=True)

def enabled_autotune_triton_attention():
    return parse_boolean_from_env('NEXFORT_ENABLE_AUTOTUNE_TRITON_ATTENTION', default_value=True)

def enabled_matmul_fp16_reduction():
    return parse_boolean_from_env('NEXFORT_ENABLE_MATMUL_FP16_REDUCTION', default_value=True)

def attention_quantize_dtype():
    quant_dtype = os.getenv('NEXFORT_ATTENTION_QUANTIZE_DTYPE', default='float8_e4m3fn')
    assert quant_dtype in ('float8_e4m3fn', 'float8_e5m2', 'int8'), f'Valid values of NEXFORT_ATTENTION_QUANTIZE_DTYPE are [float8_e4m3fn, float8_e5m2, int8], but got {quant_dtype}'
    return STR2DTYPE[quant_dtype]

def attention_quantize_type():
    quant_type = os.getenv('NEXFORT_ATTENTION_FP8_QUANTIZE_TYPE', default='cast')
    assert quant_type in ('per_token', 'per_tensor', 'per_block', 'cast', 'direct_quant'), f'Valid values of NEXFORT_ATTENTION_FP8_QUANTIZE_TYPE are [per_token, per_tensor, per_block, cast, direct_quant], but got {quant_type}'
    if quant_type == 'direct_quant':
        return QuantType('cast')
    else:
        return QuantType(quant_type)

def force_torch_scaled_mm():
    return parse_boolean_from_env('NEXFORT_FORCE_TORCH_SCALED_MM', default_value=False)

def matmul_allow_tf32():
    return parse_boolean_from_env('NEXFORT_FX_MATMUL_ALLOW_TF32', default_value=False)