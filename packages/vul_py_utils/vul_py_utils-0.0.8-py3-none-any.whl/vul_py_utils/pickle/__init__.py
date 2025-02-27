"""
  This module provides a simple interface for compressing and decompressing
"""

import zlib
import pickle


def compress(obj) -> bytes:
    p = pickle.dumps(obj)
    return zlib.compress(p)


def decompress(pickled) -> object:
    p = zlib.decompress(pickled)
    return pickle.loads(p)

