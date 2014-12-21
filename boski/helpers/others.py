# -*- coding: utf-8 -*-
import re
import cStringIO

from PIL import Image
from django.core.files.base import ContentFile

__author__ = 'Daniel Alkemic Czuba <dc@danielczuba.pl>'


def get_params(request):
    """
    Returns dict with params stored in GET and POST. Params from POST shadows GET.
    """
    _params, params = dict(request.GET.items() + request.POST.items()), {}

    for k in _params:
        match = re.match(r'(.*)\[(.*)\]', k, re.I)
        if match:
            # if not params.has_key(match.group(1)):
            if not match.group(1) in params:
                params[match.group(1)] = {}

            params[match.group(1)][match.group(2)] = _params[k]
        else:
            params[k] = _params[k]

    del _params

    return params


def get_values(iterable, keys, index_key='id', as_tuple=False):
    """
    Returns dict of given keys from iterable object, then index them by index_key. If as_tuple is True, then return
    as two-dimensional tuple.
    """
    to_return = {}

    for entry in iterable:
        if not isinstance(keys, tuple):
            to_return[entry.__getattribute__(index_key)] = entry.__getattribute__(keys)
        else:
            to_return[entry.__getattribute__(index_key)] = {}
            for key in keys:
                to_return[entry.__getattribute__(index_key)][key] = entry.__getattribute__(key)

    if as_tuple:
        tmp = {(i, to_return[i]) for i in to_return}
        to_return = tuple(tmp)

    return to_return


def reindex(iterable, index_key='id', as_tuple=False):
    """
    Reindex, and return iterable by index_key. If as_tuple is True, then return as two-dimensional tuple.
    Beware, that this break optimisation from generators, etc.
    """
    to_return = {}

    for entry in iterable:
        to_return[entry.__getattribute__(index_key)] = entry

    if as_tuple:
        tmp = {(i, to_return[i]) for i in to_return}
        to_return = tuple(tmp)

    return to_return


def generate_thumb(img, thumb_size, output_format, crop=False, upscale=False):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail

    Parameters:
    ===========
    img         File object

    thumb_size  desired thumbnail size, ie: (200,120)

    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """

    img.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)
    """:type : PIL.JpegImagePlugin.JpegImageFile"""

    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')

    max_width, max_height = thumb_size
    thumb_w, thumb_h = thumb_size

    # gdy zachodzi potrzeba zwiększenia rozmiaru obrazka, tak aby szerokość bądź wysokość była równa wartości dla miniaturki
    if upscale:
        src_width, src_height = image.size
        if src_height < max_height and src_width < max_width:
            pass
        elif src_height < max_height:
            image.resize((max_width, int(float(src_width * max_height) / float(max_width))), Image.CUBIC)
        elif src_width < max_width:
            image.resize((int(float(src_height * max_width) / float(max_height)), max_height), Image.CUBIC)

            # If you want to generate a square thumbnail
    if thumb_w == thumb_h:
        # quad
        xsize, ysize = image.size
        # get minimum size
        minsize = min(xsize, ysize)
        # largest square possible in the image
        xnewsize = (xsize - minsize) / 2
        ynewsize = (ysize - minsize) / 2
        # crop it
        image2 = image.crop((xnewsize, ynewsize, xsize - xnewsize, ysize - ynewsize))
        """:type : PIL.JpegImagePlugin.JpegImageFile"""
        # load is necessary after crop
        image2.load()
        # thumbnail of the cropped image (with ANTIALIAS to make it look better)
        image2.thumbnail(thumb_size, Image.ANTIALIAS)
    elif crop:
        src_width, src_height = image.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(float(src_width - crop_width) / 2)
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(float(src_height - crop_height) / 3)

        image2 = image.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
        image2 = image2.resize(thumb_size, Image.ANTIALIAS)
    else:
        # not quad
        image2 = image
        image2.thumbnail(thumb_size, Image.ANTIALIAS)

    io = cStringIO.StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if output_format.upper() == 'JPG':
        output_format = 'JPEG'

    image2.save(io, output_format)
    return ContentFile(io.getvalue())
