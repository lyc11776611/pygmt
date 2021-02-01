"""
Utilities for dealing with temporary file management.
"""
import os
import uuid
from tempfile import NamedTemporaryFile

import numpy as np


def unique_name():
    """
    Generate a unique name.

    Useful for generating unique names for figures (otherwise GMT will plot
    everything on the same figure instead of creating a new one).

    Returns
    -------
    name : str
        A unique name generated by :func:`uuid.uuid4`
    """
    return uuid.uuid4().hex


class GMTTempFile:
    """
    Context manager for creating closed temporary files.

    This class does not return a file-like object. So, you can't do
    ``for line in GMTTempFile()``, for example, or pass it to things that
    need file objects.

    Parameters
    ----------
    prefix : str
        The temporary file name begins with the prefix.
    suffix : str
        The temporary file name ends with the suffix.

    Examples
    --------
    >>> import numpy as np
    >>> with GMTTempFile() as tmpfile:
    ...     # write data to temporary file
    ...     x = y = z = np.arange(0, 3, 1)
    ...     np.savetxt(tmpfile.name, (x, y, z), fmt="%.1f")
    ...     lines = tmpfile.read()
    ...     print(lines)
    ...     nx, ny, nz = tmpfile.loadtxt(unpack=True, dtype=float)
    ...     print(nx, ny, nz)
    ...
    0.0 1.0 2.0
    0.0 1.0 2.0
    0.0 1.0 2.0
    <BLANKLINE>
    [0. 0. 0.] [1. 1. 1.] [2. 2. 2.]
    """

    def __init__(self, prefix="pygmt-", suffix=".txt"):
        args = dict(prefix=prefix, suffix=suffix)
        with NamedTemporaryFile(**args) as tmpfile:
            self.name = tmpfile.name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if os.path.exists(self.name):
            os.remove(self.name)

    def read(self, keep_tabs=False):
        """
        Read the entire contents of the file as a Unicode string.

        Parameters
        ----------
        keep_tabs : bool
            If False, replace the tabs that GMT uses with spaces.

        Returns
        -------
        content : str
            Content of the temporary file as a Unicode string.
        """
        with open(self.name) as tmpfile:
            content = tmpfile.read()
            if not keep_tabs:
                content = content.replace("\t", " ")
            return content

    def loadtxt(self, **kwargs):
        """
        Load data from the temporary file using numpy.loadtxt.

        Parameters
        ----------
        kwargs : dict
            Any keyword arguments that can be passed to numpy.loadtxt.

        Returns
        -------
        ndarray
            Data read from the text file.
        """
        return np.loadtxt(self.name, **kwargs)
