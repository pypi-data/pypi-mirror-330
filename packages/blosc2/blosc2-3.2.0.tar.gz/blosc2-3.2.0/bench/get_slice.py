#######################################################################
# Copyright (c) 2019-present, Blosc Development Team <blosc@blosc.org>
# All rights reserved.
#
# This source code is licensed under a BSD-style license (found in the
# LICENSE file in the root directory of this source tree)
#######################################################################

import sys
from time import time

import numpy as np

import blosc2

# Dimensions, type and persistence properties for the arrays
shape = 10_000 * 10_000
chunksize = 100_000
blocksize = 10_000

dtype = np.float64

nchunks = shape // chunksize
# Set the compression and decompression parameters
cparams = blosc2.CParams(codec=blosc2.Codec.BLOSCLZ, typesize=8, blocksize=blocksize * 8)
dparams = blosc2.DParams()
contiguous = True
persistent = bool(sys.argv[1]) if len(sys.argv) > 1 else False

if persistent:
    urlpath = "bench_getitem.b2frame"
else:
    urlpath = None

storage = blosc2.Storage(contiguous=contiguous, urlpath=urlpath)
blosc2.remove_urlpath(urlpath)

# Create the empty SChunk
schunk = blosc2.SChunk(chunksize=chunksize * cparams.typesize, storage=storage, cparams=cparams, dparams=dparams)

# Append some chunks
for i in range(nchunks):
    buffer = i * np.arange(chunksize, dtype=dtype)
    nchunks_ = schunk.append_data(buffer)
    assert nchunks_ == (i + 1)

# Use get_slice for reading blocks individually
t0 = time()
for i in range(shape // blocksize):
    _ = schunk.get_slice(start=i * blocksize, stop=(i + 1) * blocksize - 1)
t1 = time()
print(f"Time for reading with get_slice: {t1 - t0:.3f}s")

blosc2.remove_urlpath(urlpath)
