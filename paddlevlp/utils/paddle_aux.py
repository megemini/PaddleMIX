# This file is generated by PaConvert ToolKit, please Don't edit it!
import math
import paddle
from paddlevlp.utils.resample import resample
from paddlevlp.utils.kaldi import fbank


def reshape(self, *args, **kwargs):
    if args:
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            return paddle.reshape(self, args[0])
        else:
            return paddle.reshape(self, list(args))
    elif kwargs:
        return paddle.reshape(self, **kwargs)


setattr(paddle.Tensor, 'reshape', reshape)


# This file is generated by PaConvert ToolKit, please Don't edit it!


def to(self, *args, **kwargs):
    args_list = ["x", "y", "non_blocking", "copy", "memory_format"]
    new_kwargs = {}
    for i, node in enumerate(args):
        k = args_list[i]
        new_kwargs[k] = node
    for node in kwargs:
        v = kwargs[node]
        new_kwargs[node] = v
    kwargs = new_kwargs
    if not kwargs:
        return self
    elif "tensor" in kwargs:
        return paddle.cast(self, "{}.dtype".format(kwargs["tensor"]))
    elif "dtype" in kwargs:
        return paddle.cast(self, "{}".format(kwargs["dtype"]))
    elif "device" in kwargs and "dtype" not in kwargs:
        return self
    elif kwargs:
        if "y" not in kwargs and "x" in kwargs:
            if isinstance(kwargs["x"], paddle.dtype):
                dtype = kwargs["x"]
            elif isinstance(kwargs["x"], str) and kwargs["x"] not in [
                'cpu',
                'cuda',
                'ipu',
                'xpu',
            ]:
                dtype = kwargs["x"]
            elif isinstance(kwargs["x"], paddle.Tensor):
                dtype = kwargs["x"].dtype
            else:
                dtype = self.dtype
            return paddle.cast(self, dtype)

        elif "y" in kwargs and "x" in kwargs:
            if isinstance(kwargs["x"], paddle.dtype):
                dtype = kwargs["x"]
            elif isinstance(kwargs["x"], str):
                if x not in ['cpu', 'cuda', 'ipu', 'xpu']:
                    dtype = kwargs["x"]
                else:
                    dtype = kwargs["y"] if isinstance(kwargs["y"], str) else self.dtype
            else:
                dtype = kwargs["x"]
            return paddle.cast(self, dtype)
        else:
            return self


setattr(paddle.Tensor, 'to', to)


def split(self, *args, **kwargs):
    if args:
        if len(args) == 1:
            return paddle.split(self, self.shape[0] // args[0])
        else:
            return paddle.split(self, self.shape[args[1]] // args[0], args[1])
    elif kwargs:
        if "dim" in kwargs:
            kwargs["axis"] = kwargs.pop("dim")
            kwargs["num_or_sections"] = self.shape[kwargs["axis"]] // kwargs.pop(
                "split_size"
            )
        else:
            kwargs["num_or_sections"] = self.shape[0] // kwargs.pop("split_size")
        return paddle.split(self, **kwargs)


setattr(paddle.Tensor, 'split', split)


def i0(self, input):
    import math

    K = paddle.arange(0, 20).astype("float32")
    m = 0
    for k in K:
        m += ((input**2) / 4) ** k / math.factorial(k) ** 2
    return m


setattr(paddle, "i0", i0)

setattr(paddle.audio.functional, "resample", resample)


def stride(self, dim):
    shape = self.shape
    shape.append(1)
    return paddle.cumprod(paddle.to_tensor(shape)[dim + 1 :], dim=0)[-1].item()


setattr(paddle.Tensor, "stride", stride)


# def as_strided(self, size, stride):
#     dx, dy = self.shape
#     x = paddle.arange(0, dx)
#     xx = paddle.expand(x, (dy, dx)).flatten(0)
#     y = paddle.arange(0, dy).reshape((-1, 1))
#     yy = paddle.expand(y, (dy, dx)).flatten(0)
#     datas = []
#     for i in range(0, size[0]*stride[0], stride[0]):
#         axes = [0,]
#         starts = [i,]
#         ends = [stride[1]*size[1]+i,]
#         strides = [stride[1],]
#         new_x = paddle.strided_slice(
#             xx, axes=axes, starts=starts, ends=ends, strides=strides)
#         new_y = paddle.strided_slice(
#             yy, axes=axes, starts=starts, ends=ends, strides=strides)
#         datas.append(self[new_y, new_x])
#     return paddle.stack(datas)


def as_strided(self, size, stride):
    if self.dim() == 1:
        self = self.unsqueeze(0)
    dx, dy = self.shape
    w = paddle.arange(0, dy)
    ww = paddle.expand(w, (dx, dy)).flatten(0)
    h = paddle.arange(0, dx).reshape((-1, 1))
    hh = paddle.expand(h, (dx, dy)).flatten(0)
    datas = []
    for i in range(0, size[0] * stride[0], stride[0]):
        axes = [
            0,
        ]
        starts = [
            i,
        ]
        ends = [
            stride[1] * size[1] + i,
        ]
        strides = [
            stride[1],
        ]
        new_x = paddle.strided_slice(
            ww, axes=axes, starts=starts, ends=ends, strides=strides
        )
        new_y = paddle.strided_slice(
            hh, axes=axes, starts=starts, ends=ends, strides=strides
        )
        datas.append(self[new_y, new_x])
    return paddle.stack(datas)


setattr(paddle.Tensor, "as_strided", as_strided)


def hann_window(window_length, periodic=True, **kwargs):
    N = window_length
    x = paddle.arange(N)
    if periodic:
        return paddle.sin(math.pi * x / (N)) ** 2
    else:
        return paddle.sin(math.pi * x / (N - 1)) ** 2


setattr(paddle, "hann_window", hann_window)


def hamming_window(window_length, periodic=True, alpha=0.54, beta=0.46, **kwargs):
    N = window_length
    x = paddle.arange(N)
    if periodic:
        return alpha - beta * paddle.cos(2 * math.pi * x / N)
    else:
        return alpha - beta * paddle.cos(2 * math.pi * x / (N - 1))


setattr(paddle, "hamming_window", hamming_window)


def pad(input, pad, mode="constant", value=0.0):
    data_formats = {3: "NCL", 4: "NCHW", 5: "NCDHW"}
    shape = input.shape
    if input.dim() == 2:
        input = input.unsqueeze(0)
    n = len(input.shape)
    pad = list(pad) + [0] * (n - 3) * 2
    pad = pad[: (n - 2) * 2]
    return paddle.nn.functional.pad(
        input, pad=tuple(pad), mode=mode, value=value, data_format=data_formats[n]
    ).squeeze()


setattr(paddle, "pad_from_torch", pad)

setattr(paddle.audio, "fbank", fbank)
