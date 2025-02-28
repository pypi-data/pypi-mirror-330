
import io
import os
import shutil
import sys
import numpy as np
from PIL import Image
from .climage import _get_color_type, _toAnsi
from .image_to_ansi import rgb2short_fast
from .imgcat import print_image as imgcat_print_image

def _in_notebook():
    '\n    Returns ``True`` if the module is running in IPython kernel,\n    ``False`` if in IPython shell or other Python shell.\n    '
    return ('ipykernel' in sys.modules)

def _image_to_ansi_with_image_to_ansi(im, *, max_width=None):
    (w, h) = im.size
    if (max_width is not None):
        max_width //= 2
        max_width = max(1, max_width)
        if (w > max_width):
            h = int(((h * max_width) / w))
            w = max_width
            im = im.resize((w, h), Image.CUBIC)
    x = im.size[0]
    im = list(im.getdata())
    s = []
    for (i, p) in enumerate(im):
        short = rgb2short_fast(p[0], p[1], p[2])
        if ((len(p) > 3) and (p[3] == 0)):
            s.append('\x1b[0m  ')
        else:
            s.append(('\x1b[48;5;%sm  ' % short))
        if (((i + 1) % x) == 0):
            s.append('\x1b[0m\n')
    s.append('\n')
    return ''.join(s)

def _image_to_ansi_with_climage(im, *, max_width=None, is_unicode=False, is_truecolor=False, is_256color=False, is_16color=False, is_8color=False, palette='default'):
    (w, h) = im.size
    if (max_width is None):
        if is_unicode:
            width = w
        else:
            width = (w * 2)
    elif is_unicode:
        width = min(max_width, w)
    else:
        width = min(max_width, (w * 2))
    ctype = _get_color_type(is_truecolor=is_truecolor, is_256color=is_256color, is_16color=is_16color, is_8color=is_8color)
    return _toAnsi(im, oWidth=width, is_unicode=is_unicode, color_type=ctype, palette=palette)

def print_image(image, *, max_width=None, background=255, out=sys.stdout, backend='climage', **kwargs):
    assert (backend in ('climage', 'image_to_ansi'))
    if isinstance(image, (bytes, bytearray)):
        image = Image.open(io.BytesIO(image))
    else:
        image = np.asarray(image)
        image = Image.fromarray(image)
    if (image.mode == 'RGBA'):
        background = (background, background, background, 255)
        background = Image.new('RGBA', image.size, background)
        image = Image.alpha_composite(background, image)
    image = image.convert('RGB')
    if (max_width is None):
        term_size = shutil.get_terminal_size()
        max_width = term_size.columns
    if (backend == 'climage'):
        if ('is_unicode' not in kwargs):
            kwargs['is_unicode'] = True
        if (not any(((x in kwargs) for x in ('is_truecolor', 'is_256color', 'is_16color', 'is_8color')))):
            if (os.getenv('COLORTERM') in ('truecolor', '24bit')):
                kwargs['is_truecolor'] = True
            else:
                kwargs['is_256color'] = True
        s = _image_to_ansi_with_climage(image, max_width=max_width, **kwargs)
    else:
        s = _image_to_ansi_with_image_to_ansi(image, max_width=max_width)
    out.write(s)

def display_image(image, *, width=None, height=None, background=255, output_format='jpeg'):
    assert (image is not None)
    terminal = os.environ.get('TERM', '')
    if terminal.startswith('screen'):
        return
    if isinstance(image, (bytes, bytearray)):
        image = Image.open(io.BytesIO(image))
    else:
        image = np.asarray(image)
        image = Image.fromarray(image)
    if (image.mode == 'RGBA'):
        background = (background, background, background, 255)
        background = Image.new('RGBA', image.size, background)
        image = Image.alpha_composite(background, image)
    image = image.convert('RGB')
    encoded_image_bytes = io.BytesIO()
    image.save(encoded_image_bytes, format=output_format)
    encoded_image_bytes = encoded_image_bytes.getvalue()
    if _in_notebook():
        try:
            import IPython.display as ipd
        except ImportError:
            ipd = None
        if (ipd is not None):
            if (isinstance(width, str) and width.enddswith('px')):
                width = int(width[:(- 2)])
            else:
                width = None
            if (isinstance(height, str) and height.enddswith('px')):
                height = int(height[:(- 2)])
            else:
                height = None
            ipd.display(ipd.Image(data=encoded_image_bytes, width=width, height=height))
    else:
        if ((width is None) and (height is None)):
            (width, height) = (f'{min(image.size[0], 1280)}px', f'{min(image.size[1], 720)}px')
        imgcat_print_image(data=encoded_image_bytes, width=width, height=height)
        print()
