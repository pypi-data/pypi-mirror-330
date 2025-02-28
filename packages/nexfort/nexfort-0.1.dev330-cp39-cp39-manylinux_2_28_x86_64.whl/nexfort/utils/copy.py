import dataclasses
import torch
import nexfort

def tree_copy_(dest, src):
    if isinstance(dest, torch.Tensor):
        nexfort._C.copy_with_internal_overlap(dest, src)
    elif isinstance(dest, (list, tuple)):
        assert len(dest) == len(src)
        for (x, y) in zip(dest, src):
            tree_copy_(x, y)
    elif dataclasses.is_dataclass(dest):
        assert len(dest) == len(src)
        for field in dataclasses.fields(dest):
            tree_copy_(getattr(dest, field.name), getattr(src, field.name))
    elif isinstance(dest, dict):
        assert len(dest) == len(src)
        for k in dest:
            tree_copy_(dest[k], src[k])
    else:
        assert type(dest) is type(src)

def tree_copy(src):
    if isinstance(src, torch.Tensor):
        dst = torch.empty_strided(src.size(), src.stride(), dtype=src.dtype, layout=src.layout, device=src.device, pin_memory=src.is_pinned())
        dst = nexfort._C.copy_with_internal_overlap(dst, src)
        dst.requires_grad_(src.requires_grad)
        return dst
    elif isinstance(src, (list, tuple)):
        return type(src)((tree_copy(x) for x in src))
    elif dataclasses.is_dataclass(src):
        return type(src)(**{field.name: tree_copy(getattr(src, field.name)) for field in dataclasses.fields(src)})
    elif isinstance(src, dict):
        return type(src)(((k, tree_copy(v)) for (k, v) in src.items()))
    else:
        return src

def tree_shadow_copy(obj):
    if isinstance(obj, torch.Tensor):
        return nexfort._C.create_shadow_tensor(obj) if obj.device.type == 'cuda' else obj
    elif isinstance(obj, (list, tuple)):
        return type(obj)((tree_shadow_copy(x) for x in obj))
    elif dataclasses.is_dataclass(obj):
        return type(obj)(**{field.name: tree_shadow_copy(getattr(obj, field.name)) for field in dataclasses.fields(obj)})
    elif isinstance(obj, dict):
        return type(obj)(((k, tree_shadow_copy(v)) for (k, v) in obj.items()))
    else:
        return obj

def can_be_perfectly_copied(obj):
    if obj is None:
        return True
    elif isinstance(obj, (torch.Tensor, float, int, str, bytes)):
        return True
    elif isinstance(obj, (list, tuple)):
        return all((can_be_perfectly_copied(x) for x in obj))
    elif dataclasses.is_dataclass(obj):
        return all((can_be_perfectly_copied(getattr(obj, field.name)) for field in dataclasses.fields(obj)))
    elif isinstance(obj, dict):
        return all((can_be_perfectly_copied(v) for v in obj.values()))
    else:
        return False

def tree_empty_strided_like(obj):
    if isinstance(obj, torch.Tensor):
        return torch.empty_strided(obj.size(), obj.stride(), dtype=obj.dtype, layout=obj.layout, device=obj.device, requires_grad=obj.requires_grad, pin_memory=obj.is_pinned())
    elif isinstance(obj, (list, tuple)):
        return type(obj)((tree_empty_strided_like(x) for x in obj))
    elif dataclasses.is_dataclass(obj):
        return type(obj)(**{field.name: tree_empty_strided_like(getattr(obj, field.name)) for field in dataclasses.fields(obj)})
    elif isinstance(obj, dict):
        return type(obj)(((k, tree_empty_strided_like(v)) for (k, v) in obj.items()))
    else:
        return obj

def tree_has_internal_overlap(obj):
    if isinstance(obj, torch.Tensor):
        return nexfort._C.has_internal_overlap(obj)
    elif isinstance(obj, (list, tuple)):
        return any((tree_has_internal_overlap(x) for x in obj))
    elif dataclasses.is_dataclass(obj):
        return any((tree_has_internal_overlap(getattr(obj, field.name)) for field in dataclasses.fields(obj)))
    elif isinstance(obj, dict):
        return any((tree_has_internal_overlap(v) for v in obj.values()))
    else:
        return False

def tree_convert_to_no_internal_overlap(obj):
    if isinstance(obj, torch.Tensor):
        return nexfort._C.convert_to_no_internal_overlap(obj)
    elif isinstance(obj, (list, tuple)):
        return type(obj)((tree_convert_to_no_internal_overlap(x) for x in obj))
    elif dataclasses.is_dataclass(obj):
        return type(obj)(**{field.name: tree_convert_to_no_internal_overlap(getattr(obj, field.name)) for field in dataclasses.fields(obj)})
    elif isinstance(obj, dict):
        return type(obj)(((k, tree_convert_to_no_internal_overlap(v)) for (k, v) in obj.items()))
    else:
        return obj