
import os

from .conf import settings

basename = os.path.basename
splitext = os.path.splitext

def dataset_name(dset):
    if 'DATASET_NAMES' in settings.__dict__:
        return str(settings.DATASET_NAMES[dset])
    if isinstance(dset, tuple):
        txt = ''
        for name in dset:
            bname = basename(name)
            exts = splitext(bname)
            start = exts[0]
            txt += start + '_'
        txt = txt.rstrip('_')
    else:
        bname = basename(dset)
        exts = splitext(bname)
        start = exts[0]
        txt = start
    return txt

