"""
Random utilities
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import time
import warnings
from collections import OrderedDict
from collections.abc import Iterable
from functools import lru_cache
from logging import Logger
from typing import List

import numpy as np
import scipy
import scipy.stats
from scipy.stats import circmean, circstd

try:
    from mahotas.features import zernike_moments

    HAS_MAHO = True
except ImportError:
    HAS_MAHO = False

DEFAULT_MPL_BACKEND = None
on_CI = os.environ.get("CI") or os.environ.get("CONTINUOUS_INTEGRATION")
if not on_CI and os.environ.get("DISPLAY") and os.environ.get("DISPLAY") != "":
    DEFAULT_MPL_BACKEND = "TKAgg"
else:
    DEFAULT_MPL_BACKEND = "Agg"

try:
    import matplotlib as mpl

    mpl.use(DEFAULT_MPL_BACKEND)
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    # This is necessary. Random backends might respond incorrectly.
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def _generic_dummy_decorator(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return args[0]
    else:

        def decorator(func):
            def decorated(*args, **kwargs):
                return func(*args, **kwargs)

            return decorated

        return decorator


try:
    from numba import jit, njit, vectorize

    HAS_NUMBA = True
except ImportError:
    warnings.warn("Numba not installed. Faking it")

    jit = njit = vectorize = _generic_dummy_decorator
    HAS_NUMBA = False


__all__ = [
    "calculate_beam_fom",
    "calculate_zernike_moments",
    "compare_strings",
    "ds9_like_log_scale",
    "get_center_of_mass",
    "interpolate_invalid_points_image",
    "jit",
    "mad",
    "standard_byte",
    "standard_string",
    "tqdm",
    "vectorize",
]


try:
    from tqdm import tqdm
except ImportError:

    def tqdm(x):
        return x


try:
    from statsmodels.robust import mad  # pylint: disable=unused-import

    HAS_STATSM = True
except ImportError:
    HAS_STATSM = False

    def mad(data, c=0.6745, axis=None):
        """Straight from statsmodels's source code, adapted"""
        data = np.asarray(data)
        if axis is not None:
            center = np.apply_over_axes(np.median, data, axis)
        else:
            center = np.median(data)
        return np.median((np.fabs(data - center)) / c, axis=axis)


ListOfStrings = List[str]
TWOPI = 2 * np.pi

if HAS_NUMBA:

    @vectorize
    def normalize_angle_mpPI(angle):  # pragma: no cover
        """Normalize angle between minus pi and pi."""
        angle = angle % TWOPI
        if angle > np.pi:
            angle -= TWOPI
        if angle < -np.pi:
            angle += TWOPI
        return angle

else:

    def _normalize_angle_mpPI_vec(angle):
        """Normalize angle between minus pi and pi."""
        angle = np.asarray(angle)
        angle = angle % TWOPI
        angle[angle >= np.pi] -= TWOPI
        return angle

    def normalize_angle_mpPI(angle):
        """Normalize angle between minus pi and pi."""
        if isinstance(angle, Iterable):
            return _normalize_angle_mpPI_vec(angle)
        angle = angle % TWOPI
        if angle >= np.pi:
            angle -= TWOPI
        return angle


@lru_cache(10)
def warn_once(logger: Logger, msg: str):
    logger.warning(msg)


@lru_cache(10)
def info_once(logger: Logger, msg: str):
    logger.info(msg)


def get_circular_statistics(array):
    """Get min, max, mean, std of a circular array.

    If the array wraps around 360/0, the min and max will be swapped.

    Only valid for a reasonably small range around 2pi/0 degrees.

    Examples
    --------
    >>> array = np.array([6.1, 6.2, 0.16, 0.26])
    >>> res = get_circular_statistics(array)
    >>> assert np.isclose(res['min'], 6.1 - 2*np.pi)
    >>> assert res['max'] == 0.26
    """
    array = np.asarray(array) % TWOPI
    mean_ = circmean(array)
    std_ = circstd(array)
    diff_ = array - mean_
    diff_[diff_ > np.pi] -= TWOPI
    diff_[diff_ <= -np.pi] += TWOPI
    return dict(min=np.min(diff_) + mean_, max=np.max(diff_) + mean_, mean=mean_, std=std_)


def remove_suffixes_and_prefixes(
    name: str, suffixes: ListOfStrings = [], prefixes: ListOfStrings = []
) -> str:
    """Eliminate a list of prefixes and suffixes from names.

    Additionaly, this will remove any trailing or leading underscores.

    Examples
    --------
    >>> remove_suffixes_and_prefixes('bla_ra_dec', ["_ra", "_dec"])
    'bla'
    >>> remove_suffixes_and_prefixes('bla_RA_Dec_', ["_ra", "_dec"])
    'bla'
    >>> remove_suffixes_and_prefixes('_bla_ra_K', suffixes=["_ra", "_dec", "_k"])
    'bla'
    >>> remove_suffixes_and_prefixes('k_bla_ra', prefixes=["k_"])
    'bla_ra'
    """
    name = name.strip("_")
    regex = rf"({'|'.join(suffixes)})+$"
    name = re.sub(regex, "", name, flags=re.IGNORECASE)

    regex = rf"^({'|'.join(prefixes)})+"
    name = re.sub(regex, "", name, flags=re.IGNORECASE)

    return name.strip("_")


def force_move_file(src, dst):
    """Force moving a file, even if it exists.

    Examples
    --------
    >>> with open('bla', 'w') as fobj:
    ...    print(file=fobj)
    >>> with open('bla2', 'w') as fobj:
    ...    print(file=fobj)
    >>> force_move_file('bla', './bla') is None
    True
    >>> force_move_file('bla2', 'bla') == 'bla'
    True
    >>> os.path.exists('bla2')
    False
    """
    if os.path.abspath(src) == os.path.abspath(dst):
        return None
    if os.path.exists(dst):
        os.unlink(dst)
    shutil.move(src, dst)
    return dst


def standard_string(s):
    """Standard string representation for a given Python version

    Examples
    --------
    >>> standard_string(b'a')
    'a'
    >>> standard_string(None) is None
    True
    """
    if s is None:
        return None

    # for Python 3
    # This indexing should work for both lists of strings, and strings
    if hasattr(s, "decode"):
        s = s.decode()  # or  s = str(s)[2:-1]
    # Try to see if it's a numpy array
    elif hasattr(s, "dtype") and s.dtype.char == "S":
        if s.size > 1:
            s = np.array(s, dtype="U")
    return s


def standard_byte(s):
    """Standard byte representation for a given Python version

    Examples
    --------
    >>> standard_byte(b'a') == b'a'
    True
    >>> standard_byte(np.array([u'a'])[0]) == b'a'
    True
    """
    if hasattr(s, "encode"):
        s = s.encode()
    elif hasattr(s, "dtype") and s.dtype.char == "U":
        if s.size > 1:
            s = np.array(s, dtype="S")
    return s


def compare_strings(s1, s2):
    """Compare strings, that might be bytes and unicode in some cases.

    Parameters
    ----------
    s1: string, byte or array of str/bytes
    s2 : string or byte

    Examples
    --------
    >>> compare_strings(b'a', 'a')
    True
    >>> compare_strings('a', u'a')
    True
    >>> import numpy as np
    >>> res = np.array([ True, False], dtype=bool)
    >>> assert np.all(compare_strings(np.array(['a', 'b'], dtype='S'), u'a') == res)
    """
    s1 = standard_string(s1)
    s2 = standard_string(s2)
    return s1 == s2


def compare_anything(value1, value2):
    """Compare two whatever.

    They must be identical. Same type, same variable types, etc.
    ``1 != 1.0``, to ble clear. See examples.

    Examples
    --------
    >>> compare_anything(1, 2)
    False
    >>> compare_anything(int(1), float(1))
    False
    >>> compare_anything([1], 2)
    False
    >>> compare_anything([1], [2])
    False
    >>> compare_anything([1, 2], [1, 2])
    True
    >>> compare_anything({1: 2}, [1, 2])
    False
    >>> compare_anything({1: 2}, {1: 2})
    True
    >>> compare_anything({1: [2]}, {1: [2]})
    True
    >>> compare_anything({1: {1: 2}}, {1: {1: 2}})
    True
    >>> compare_anything({1: {1: 2}, 2: {1: 2}}, {2: {1: 2}, 1: {1: 2}})
    True
    >>> compare_anything({1: {1: "2"}, 2: {1: 2}}, {2: {1: 2}, 1: {1: "2"}})
    True
    >>> compare_anything("aa", "aa")
    True
    >>> compare_anything(u"aa", b"aa")
    False
    >>> compare_anything("aa", "bb")
    False
    >>> compare_anything({1: {1: "2"}, 2: {1: 2}}, {})
    False
    """
    if not isinstance(value1, value2.__class__):
        return False

    if not isinstance(value1, Iterable) or isinstance(value1, str):
        return value1 == value2
    elif not isinstance(value1, dict):
        for i, j in zip(value1, value2):
            if not compare_anything(i, j):
                return False
    else:
        items1 = value1.items()
        items2 = value2.items()
        if len(list(items1)) != len(list(items2)):
            return False
        value1_sort = OrderedDict(sorted(items1))
        value2_sort = OrderedDict(sorted(items2))
        for i, j in zip(value1_sort.items(), value2_sort.items()):
            if not compare_anything(i, j):
                return False

    return True


def interpolate_invalid_points_image(array, zeros_are_invalid=False):
    """Interpolates invalid points in an image.

    Examples
    --------
    >>> img = np.ones((3, 3))
    >>> img[1, 1] = np.nan
    >>> assert np.all(interpolate_invalid_points_image(img) == np.ones((3, 3)))
    >>> img = np.ones((3, 3))
    >>> img[1, 1] = 0
    >>> assert np.all(interpolate_invalid_points_image(img, True) == np.ones((3, 3)))
    """
    from scipy import interpolate

    if zeros_are_invalid:
        # 0/0 gives nan
        array = array / array * array

    x = np.arange(0, array.shape[1])
    y = np.arange(0, array.shape[0])
    # mask invalid values
    array = np.ma.masked_invalid(array)
    xx, yy = np.meshgrid(x, y)
    # get only the valid values
    x1 = xx[~array.mask]
    y1 = yy[~array.mask]
    newarr = array[~array.mask]

    GD1 = interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method="cubic", fill_value=0)
    return GD1


def ds9_like_log_scale(im_to_analyze, a=1000):
    """Rescale the image to a log scale.

    The scale is the same documented in the ds9 docs, for consistency.
    After normalizing the image from 0 to 1, the log-rescaled image is
    log(ax + 1) / log a, with ``x`` the normalized image and ``a`` a
    constant fixed here at 1000

    Parameters
    ----------
    im_to_analyze : 2d array
        The image to rescale

    Other Parameters
    ----------------
    a : float
        The scale parameter, default 1000

    Returns
    -------
    im_rescaled : 2d array
        The rescaled image
    """
    vmin = im_to_analyze.min()
    vmax = im_to_analyze.max()
    rescaled_image = (im_to_analyze - vmin) / (vmax - vmin)

    return np.log(a * rescaled_image + 1) / np.log(a)


def get_center_of_mass(im, radius=1, approx=None):
    """Get center of mass of image, filtering by radius around the maximum.

    Examples
    --------
    >>> image = np.array(([0,0,0,0],
    ...                   [0,1,1,0],
    ...                   [0,1,1,0],
    ...                   [0,1,1,0]))
    >>> cm = get_center_of_mass(image)
    >>> assert np.all(cm == np.array([2.0, 1.5]))
    >>> image = np.array(([0, 0,0,0,0, 0],
    ...                   [0, 0,0,0,0, 0],
    ...                   [0, 0,1,1,0, 0],
    ...                   [0, 0,1,1,0, 0],
    ...                   [0, 0,1,1,0, 0],
    ...                   [0, 0,0,0,0, 0]))
    >>> cm = get_center_of_mass(image, radius=0.4)
    >>> assert not np.all(cm == np.array([2.5, 2.5]))
    >>> cm = get_center_of_mass(image, radius=0.4, approx='max')
    >>> assert np.all(cm == np.array([2.5, 2.5]))
    >>> cm = get_center_of_mass(image)
    >>> assert np.all(cm == np.array([3., 2.5]))
    """
    import scipy.ndimage

    if approx is None:
        approx = np.array(im.shape) // 2
    elif approx == "max":
        approx = np.unravel_index(im.argmax(), im.shape)

    npix = int(radius * min(im.shape))
    xmin, xmax = max(0, approx[0] - npix), min(approx[0] + npix, im.shape[0])
    ymin, ymax = max(0, approx[1] - npix), min(approx[1] + npix, im.shape[1])
    good_x = slice(xmin, max(xmax, xmin + 1))
    good_y = slice(ymin, max(ymax, ymin + 1))

    cm = np.asarray(scipy.ndimage.center_of_mass(im[good_x, good_y]))
    cm[0] += xmin
    cm[1] += ymin
    return cm


def calculate_zernike_moments(
    im,
    cm=None,
    radius=0.3,
    norder=8,
    label=None,
    use_log=False,
    show_plot=False,
):
    """Calculate the Zernike moments of the image.

    These moments are useful to single out asymmetries in the image:
    for example, when characterizing the beam of the radio telescope using
    a map of a calibrator, it is useful to calculate these moments to
    understand if the beam is radially symmetric or has distorted side
    lobes.

    Parameters
    ----------
    im : 2-d array
        The image to be analyzed

    Other Parameters
    ----------------
    cm : [int, int]
        'Center of mass' of the image
    radius : float
        The radius around the center of mass, in percentage of the image
        size (0 <= radius <= 0.5)
    norder : int
        Maximum order of the moments to calculate
    use_log: bool
        Rescale the image to a log scale before calculating the coefficients.
        The scale is the same documented in the ds9 docs, for consistency.
        After normalizing the image from 0 to 1, the log-rescaled image is
        log(ax + 1) / log a, with ``x`` the normalized image and ``a`` a
        constant fixed here at 1000
    show_plot : bool, default False
        show the plots immediately

    Returns
    -------
    moments_dict : dict
        Dictionary containing the order, the sub-index and the moment, e.g.
        {0: {0: 0.3}, 1: {1: 1e-16}, 2: {0: 0.95, 2: 6e-19}, ...}
        Moments are symmetrical, so only the unique values are reported.

    """
    if np.all(np.isnan(im)):
        return None
    im_to_analyze = im.copy()
    im_to_analyze = interpolate_invalid_points_image(im_to_analyze, zeros_are_invalid=True)

    if cm is None or np.any(np.isnan(cm)):
        cm = get_center_of_mass(im_to_analyze, radius, approx="max")
    if (
        (cm[0] >= im_to_analyze.shape[0])
        or (cm[1] >= im_to_analyze.shape[1])
        or (cm[0] < 1)
        or (cm[1] < 1)
    ):
        cm = np.array(im_to_analyze.shape) // 2

    if use_log:
        im_to_analyze = ds9_like_log_scale(im_to_analyze, 1000)

    radius_pix = int(np.min(im.shape) * radius)
    moments = zernike_moments(im_to_analyze, radius_pix, norder, cm=cm)
    count = 0
    moments_dict = {}
    description_string = f"Zernike moments (cm: {cm}, radius: {radius_pix}):\n"

    if HAS_MPL:
        fig = plt.figure("Zernike moments", figsize=(10, 10))
        x, y = int(cm[0]), int(cm[1])
        shape = im_to_analyze.shape
        vmax = np.max(im_to_analyze)

        if (x < shape[0]) & (y < shape[1]):
            vmax = im_to_analyze[x, y]

        plt.imshow(im_to_analyze, vmin=0, vmax=vmax, origin="lower", cmap="magma")
        circle = plt.Circle((y, x), radius_pix, color="r", fill=False)
        plt.gca().add_patch(circle)
        plt.colorbar()

    for i in range(norder + 1):
        description_string += str(i) + ": "
        moments_dict[i] = {}
        for j in range(i + 1):
            if (i - j) % 2 == 0:
                description_string += f"{i}/{j} {moments[count]:.1e} "
                moments_dict[i][j] = moments[count]
                count += 1
        description_string += "\n"

    if HAS_MPL:
        plt.text(
            0.05,
            0.95,
            description_string,
            horizontalalignment="left",
            verticalalignment="top",
            transform=plt.gca().transAxes,
            color="white",
        )

        if label is None:
            label = str(np.random.randint(0, 100000))
        plt.savefig("Zernike_debug_" + label + ".png")
        if show_plot:
            plt.show()
        plt.close(fig)

    logging.debug(description_string)

    moments_dict["Description"] = description_string

    return moments_dict


def calculate_beam_fom(im, cm=None, radius=0.3, label=None, use_log=False, show_plot=False):
    """Calculate various figures of merit (FOMs) in an image.

    These FOMs are useful to single out asymmetries in a beam shape:
    for example, when characterizing the beam of the radio telescope using
    a map of a calibrator, it is useful to understand if there are lobes
    appearing only in one direction.

    Parameters
    ----------
    im : 2-d array
        The image to be analyzed

    Other Parameters
    ----------------
    cm : [int, int]
        'Center of mass' of the image
    radius : float
        The radius around the center of mass, in percentage of the image
        size (0 <= radius <= 0.5)
    use_log: bool
        Rescale the image to a log scale before calculating the coefficients.
        The scale is the same documented in the ds9 docs, for consistency.
        After normalizing the image from 0 to 1, the log-rescaled image is
        log(ax + 1) / log a, with ``x`` the normalized image and ``a`` a
        constant fixed here at 1000
    show_plot : bool, default False
        show the plots immediately

    Returns
    -------
    results_dict : dict
        Dictionary containing the results
    """
    if np.all(np.isnan(im)):
        return None
    im_to_analyze = im.copy()
    im_to_analyze = interpolate_invalid_points_image(im_to_analyze, zeros_are_invalid=True)
    if cm is None:
        cm = get_center_of_mass(im_to_analyze, radius, approx="max")
    if (
        (cm[0] >= im_to_analyze.shape[0])
        or (cm[1] >= im_to_analyze.shape[1])
        or (cm[0] < 1)
        or (cm[1] < 1)
    ):
        cm = np.array(im_to_analyze.shape) // 2

    if use_log:
        im_to_analyze = ds9_like_log_scale(im_to_analyze, 1000)

    radius_pix = int(np.min(im.shape) * radius)

    moments_dict = {}
    description_string = f"Figures of Merit (cm: {cm}, radius: {radius_pix}):\n"

    img_max = np.unravel_index(im.argmax(), im.shape)
    npix = int(radius * min(im.shape))
    xmin, xmax = max(0, img_max[0] - npix), min(img_max[0] + npix, im.shape[0])
    ymin, ymax = max(0, img_max[1] - npix), min(img_max[1] + npix, im.shape[1])
    good_x = slice(xmin, xmax)
    good_y = slice(ymin, ymax)

    y_slice = im_to_analyze[good_x, int(np.rint(cm[1]))]
    x_slice = im_to_analyze[int(np.rint(cm[0])), good_y]

    y_pixels = np.arange(xmax - xmin) + xmin
    x_pixels = np.arange(ymax - ymin) + ymin

    if HAS_MPL:
        fig = plt.figure("FOM", figsize=(10, 10))
        gs = GridSpec(2, 2, height_ratios=(1, 3), width_ratios=(3, 1), hspace=0)
        img_ax = plt.subplot(gs[1, 0])
        hor_ax = plt.subplot(gs[0, 0], sharex=img_ax)
        ver_ax = plt.subplot(gs[1, 1], sharey=img_ax)

        x, y = int(cm[0]), int(cm[1])
        img_ax.imshow(
            im_to_analyze,
            vmin=0,
            vmax=im_to_analyze[x, y],
            origin="lower",
            cmap="magma",
        )

        img_ax.axvline(cm[1], color="white")
        img_ax.axhline(cm[0], color="white")

        ver_ax.plot(y_slice - np.max(y_slice) + 1, y_pixels)

        hor_ax.plot(x_pixels, x_slice - np.max(x_slice) + 1)

        circle = plt.Circle(cm, radius_pix, color="r", fill=False)
        plt.gca().add_patch(circle)
        img_ax.set_xlim([0, im_to_analyze.shape[1] - 1])
        img_ax.set_ylim([0, im_to_analyze.shape[0] - 1])

    xmoments = calculate_moments(x_slice)
    ymoments = calculate_moments(y_slice)

    description_string += "Skewness : \n"
    description_string += "X: {}\n".format(xmoments["skewness"])
    description_string += "Y: {}\n".format(ymoments["skewness"])
    description_string += "Kurtosis : \n"
    description_string += "X: {}\n".format(xmoments["kurtosis"])
    description_string += "Y: {}\n".format(ymoments["kurtosis"])

    moments_dict["XSK"] = xmoments["skewness"]
    moments_dict["YSK"] = ymoments["skewness"]
    moments_dict["XKU"] = xmoments["kurtosis"]
    moments_dict["YKU"] = ymoments["kurtosis"]

    if HAS_MPL:
        img_ax.text(
            0.05,
            0.95,
            description_string,
            horizontalalignment="left",
            verticalalignment="top",
            transform=img_ax.transAxes,
            color="white",
            zorder=10,
        )

        if label is None:
            label = str(np.random.randint(0, 100000))
        plt.savefig("FOM_debug_" + label + ".png")
        if show_plot:
            plt.show()
        plt.close(fig)

    logging.debug(description_string)

    moments_dict["Description"] = description_string

    return moments_dict


def calculate_moments(y, imax=None, window_length=5):
    """Calculate moments of a curve.

    Parameters
    ----------
    y : array-like
        The curve to be analyzed

    Other Parameters
    ----------------
    imax : int, default None
        The index of the center of the curve to be analyzed. If None, the
        index of the maximum of y is taken
    window_length : int, default 5
        The window to be used for smoothing

    Returns
    -------
    moments : dict
        Dictionary containing the moments, e.g.
        ``{'skewness': 0.0, 'kurtosis' : 0.00123456}``

    Examples
    --------
    >>> y = np.exp(-np.linspace(-10, 10, 1101)**2/2)
    >>> mo = calculate_moments(y)
    >>> assert np.all(np.isclose(mo['skewness'], 0))
    """
    from scipy.signal import savgol_filter

    yk = savgol_filter(np.asarray(y), window_length=window_length, polyorder=3)

    if imax is None:
        imax = np.argmax(yk)

    N = len(y)
    xk = imax - np.arange(N)
    # Avoid negative numbers
    yk -= yk.min()
    yk = np.round(yk / np.sum(yk), decimals=7)

    xslice_dist = scipy.stats.rv_discrete(name="custm", values=(xk, yk))
    moments = {}
    moments["skewness"] = xslice_dist.stats(moments="s")
    moments["kurtosis"] = xslice_dist.stats(moments="k")
    return moments


def get_maxvar_and_direction_from_data(data):
    if data is None:
        return 1e32, ""
    data = np.asarray(data)
    if len(data.shape) == 2:
        data = data[:, 0]

    diff = data[-1] - data[0]
    if diff > 0:
        scan_direction = ">"
    else:
        scan_direction = "<"
    return np.abs(diff), scan_direction


def scantype(ra, dec, az=None, el=None):
    """Get if scan is along RA or Dec, and if forward or backward.

    Examples
    --------
    >>> ras = np.linspace(1, 1.5, 100)
    >>> decs = np.linspace(0, 0.01, 100)
    >>> els = np.linspace(0.5, 0.7, 100)
    >>> azs = np.linspace(0.5, 0.7, 100)
    >>> st = scantype(ras, decs, azs, els)
    >>> assert np.all(st[0] == ras)
    >>> st[1] == 'RA>'
    True
    >>> # Opposite direction
    >>> ras = np.linspace(1, 1.5, 100)[::-1]
    >>> scantype(ras, decs, azs, els)[1]
    'RA<'
    >>> # Do not specify El and Dec, and test that it still works
    >>> scantype(ras, decs)[1]
    'RA<'
    >>> els, ras = ras, els
    >>> decs, azs = azs, decs
    >>> scantype(ras, decs, azs, els)[1]
    'El<'
    >>> ras = list(zip(np.linspace(1, 1.5, 100), np.linspace(1, 1.5, 100)))
    >>> decs = list(zip(np.linspace(0, 0.01, 100), np.linspace(0, 0.01, 100)))
    >>> els = list(zip(np.linspace(0.5, 0.7, 100), np.linspace(0.5, 0.7, 100)))
    >>> azs = list(zip(np.linspace(0.5, 0.7, 100), np.linspace(0.5, 0.7, 100)))
    >>> st = scantype(ras, decs, azs, els)
    >>> assert np.all(st[0] == ras)
    >>> st[1] == 'RA>'
    True
    """
    ravar, radir = get_maxvar_and_direction_from_data(ra)
    decvar, decdir = get_maxvar_and_direction_from_data(dec)
    elvar, eldir = get_maxvar_and_direction_from_data(el)
    azvar, azdir = get_maxvar_and_direction_from_data(az)

    direction = np.asarray([["RA", "Dec"], ["Az", "El"]])
    scandirection = np.asarray([[radir, decdir], [azdir, eldir]])

    vararray = np.asarray([[ravar, decvar], [azvar, elvar]])
    minshift = np.argmin(vararray[:, ::-1])

    scanarray = [ra, dec, az, el]

    xvariab = direction.flatten()[minshift]
    xscandir = scandirection.flatten()[minshift]

    x = scanarray[minshift]

    return x, xvariab + xscandir


def minmax(array):
    return np.min(array), np.max(array)


def median_diff(array, sorting=False):
    """Median difference after reordering the array or not.

    Examples
    --------
    >>> assert median_diff([1, 2, 0, 4, -1, -2]) == -1.0
    >>> assert median_diff([1, 2, 0, 4, -1, -2], sorting=True) == 1.0
    """
    if len(array) == 0:
        return 0
    array = np.array(array)
    # No NaNs
    array = array[array == array]
    if sorting:
        array = sorted(array)
    return np.median(np.diff(array))


def get_mH2O(TMP, U):
    """Get the meters of H2O, using the formula from old converter.

    Unsure if this is correct in all cases
    """
    RS = 8.314472
    mw = 0.018015
    md = 0.0289644
    eps0 = mw / md
    k1 = 77.60
    k2 = 70.4
    k3 = 3.739e5

    TMP = TMP - 273.15
    H = (np.log10(U) - 2.0) / 0.4343 + (17.62 * TMP) / (243.12 + TMP)

    DPT = 243.12 * H / (17.62 - H)

    TMP = TMP + 273.15

    Tm = 0.673 * TMP + 83.0
    C = 1e6 * mw / (k2 - k1 * eps0 + k3 / Tm) / RS
    e0 = np.exp(1.81 + 17.27 * DPT / (DPT + 237.5))
    ZWDS = 0.002277 * (0.005 + 1255 / TMP) * e0

    return ZWDS * C * 100.0


def look_for_files_or_bust(files, timeout):
    """Look for all files in the list, or raise an exception."""
    t0 = time.time()
    current_time = time.time()
    number_of_seconds = 0
    while current_time - t0 < timeout:
        import numpy as np

        all_exist = np.zeros(len(files), dtype=bool)
        for i, fname in enumerate(files):
            all_exist[i] = os.path.exists(fname)
        if np.all(all_exist):
            break
        current_time = time.time()
        if current_time - t0 > number_of_seconds:
            number_of_seconds += 1
            logging.info("Not all files were found. Keep going...")

    else:
        missing_files = [fname for exists, fname in zip(all_exist, files) if not exists]

        raise FileNotFoundError(
            "One or more of the expected files" f" were not found: {missing_files}"
        )
