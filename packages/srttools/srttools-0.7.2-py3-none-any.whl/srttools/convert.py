import copy
import glob
import os
import shutil
import warnings

import numpy as np

import astropy.units as u
from astropy.io import fits
from astropy.table import Table
from astropy.time import Time
from astropy.utils.exceptions import AstropyWarning

from .converters.classfits import CLASSFITS_creator
from .converters.mbfits import MBFITS_creator
from .converters.sdfits import SDFITS_creator
from .io import (
    correct_offsets,
    get_coords_from_altaz_offset,
    get_rest_angle,
    locations,
    observing_angle,
)
from .scan import _is_summary_file, find_summary_file_in_dir


def convert_to_complete_fitszilla(fname, outname):
    if outname == fname:
        raise ValueError("Files cannot have the same name")
    with fits.open(fname, memmap=False) as lchdulist:
        _convert_to_complete_fitszilla(lchdulist, outname)
        lchdulist.writeto(outname + ".fits", overwrite=True)


def _convert_to_complete_fitszilla(lchdulist, outname):
    feed_input_data = lchdulist["FEED TABLE"].data
    xoffsets = feed_input_data["xOffset"] * u.rad
    yoffsets = feed_input_data["yOffset"] * u.rad
    # ----------- Extract generic observation information ------------------
    site = lchdulist[0].header["ANTENNA"].lower()
    location = locations[site]

    rest_angles = get_rest_angle(xoffsets, yoffsets)

    datahdu = lchdulist["DATA TABLE"]
    data_table_data = Table(datahdu.data)

    new_table = Table()
    info_to_retrieve = [
        "time",
        "derot_angle",
        "el",
        "az",
        "raj2000",
        "decj2000",
    ]
    for info in info_to_retrieve:
        new_table[info.replace("j2000", "")] = data_table_data[info]

    el_save = new_table["el"]
    az_save = new_table["az"]
    derot_angle = new_table["derot_angle"]
    el_save.unit = u.rad
    az_save.unit = u.rad
    derot_angle.unit = u.rad
    times = new_table["time"]

    for i, (xoffset, yoffset) in enumerate(zip(xoffsets, yoffsets)):
        obs_angle = observing_angle(rest_angles[i], derot_angle)

        # offsets < 0.001 arcseconds: don't correct (usually feed 0)
        if (
            np.abs(xoffset) < np.radians(0.001 / 60.0) * u.rad
            and np.abs(yoffset) < np.radians(0.001 / 60.0) * u.rad
        ):
            continue
        el = copy.deepcopy(el_save)
        az = copy.deepcopy(az_save)
        xoffs, yoffs = correct_offsets(obs_angle, xoffset, yoffset)
        obstimes = Time(times * u.day, format="mjd", scale="utc")

        # el and az are also changed inside this function (inplace is True)
        ra, dec = get_coords_from_altaz_offset(
            obstimes, el, az, xoffs, yoffs, location=location, inplace=True
        )
        ra = fits.Column(array=ra, name="raj2000", format="1D")
        dec = fits.Column(array=dec, name="decj2000", format="1D")
        el = fits.Column(array=el, name="el", format="1D")
        az = fits.Column(array=az, name="az", format="1D")
        new_data_extension = fits.BinTableHDU.from_columns([ra, dec, el, az])
        new_data_extension.name = f"Coord{i}"
        lchdulist.append(new_data_extension)


def launch_convert_coords(name, label, save_locally=False):
    allfiles = []
    if os.path.isdir(name):
        allfiles += glob.glob(os.path.join(name, "*.fits"))
    else:
        allfiles += [name]

    for fname in allfiles:
        if _is_summary_file(fname):
            continue
        outroot = fname.replace(".fits", "_" + label)
        if save_locally:
            outroot = os.path.basename(outroot)

        convert_to_complete_fitszilla(fname, outroot)
    return outroot


# from memory_profiler import profile
# fp = open('memory_profiler_basic_mean.log', 'w+')
# precision = 10
#
# @profile(precision=precision, stream=fp)
def launch_mbfits_creator(name, label, test=False, wrap=False, detrend=False, save_locally=False):
    if not os.path.isdir(name):
        raise ValueError("Input for MBFITS conversion must be a directory.")
    name = name.rstrip("/")
    random_name = "tmp_" + str(np.random.random())
    mbfits = MBFITS_creator(random_name, test=test)
    summary = find_summary_file_in_dir(name)
    if os.path.exists(summary):
        mbfits.fill_in_summary(summary)

    for fname in sorted(glob.glob(os.path.join(name, "*.fits"))):
        if _is_summary_file(fname):
            continue
        mbfits.add_subscan(fname, detrend=detrend)

    mbfits.update_scan_info()
    if save_locally:
        name = os.path.basename(name)

    outname = name + "_" + label
    if os.path.exists(outname):
        shutil.rmtree(outname)

    if wrap:
        fnames = mbfits.wrap_up_file()
        for febe, fname in fnames.items():
            shutil.move(fname, name + "." + febe + ".fits")
    shutil.move(random_name, outname)
    return outname, mbfits


def launch_classfits_creator(name, label, test=False, save_locally=False):
    if not os.path.isdir(name):
        raise ValueError("Input for CLASSFITS conversion must be a directory.")
    name = name.rstrip("/")
    outname = name + "_" + label
    if save_locally:
        outname = os.path.basename(outname)
    if os.path.exists(outname):
        shutil.rmtree(outname)
    random_name = "tmp_" + str(np.random.random())
    classfits = CLASSFITS_creator(random_name, scandir=name, average=True)
    shutil.move(random_name, outname)
    return outname, classfits


def launch_sdfits_creator(name, label, test=False, save_locally=False):
    if not os.path.isdir(name):
        raise ValueError("Input for SDFITS conversion must be a directory.")
    name = name.rstrip("/")
    outname = name + "_" + label
    if save_locally:
        outname = os.path.basename(outname)

    if os.path.exists(outname):
        shutil.rmtree(outname)
    random_name = "tmp_" + str(np.random.random())
    classfits = SDFITS_creator(random_name, scandir=name)
    shutil.move(random_name, outname)
    return outname, classfits


def match_srt_name(name):
    """
    Examples
    --------
    >>> matchobj = match_srt_name('blabla/20180212-150835-S0000-3C84_RA/')
    >>> matchobj.group(1)
    '20180212'
    >>> matchobj.group(2)
    '150835'
    >>> matchobj.group(3)
    'S0000'
    >>> matchobj.group(4)
    '3C84_RA'
    """
    name = os.path.basename(name.rstrip("/"))
    import re

    name_re = re.compile(r"([0-9]+).([0-9]+)-([^\-]+)-([^\-]+)")
    return name_re.match(name)


def main_convert(args=None):
    import argparse

    description = "Load a series of scans and convert them to various" "formats"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "files",
        nargs="*",
        help="Single files to process or directories",
        default=None,
        type=str,
    )

    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="fitsmod",
        help="Format of output files (options: "
        "mbfits, indicating MBFITS v. 1.65; "
        "mbfitsw, indicating MBFITS v. 1.65 wrapped in a"
        "single file for each FEBE; "
        "fitsmod (default), indicating a fitszilla with "
        "converted coordinates for feed number *n* in "
        "a separate COORDn extensions); "
        "classfits, indicating a FITS file readable into "
        "CLASS, calibrated when possible;"
        "sdfits, for the SDFITS convention",
    )

    parser.add_argument(
        "--test",
        help="Only to be used in tests!",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--detrend",
        help="Detrend data before converting to MBFITS",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--save-locally",
        help="Save all data in the current directory, not" "alongside the original data.",
        action="store_true",
        default=False,
    )

    args = parser.parse_args(args)

    outnames = []
    for fname in args.files:
        if args.format == "fitsmod":
            outname = launch_convert_coords(fname, args.format, save_locally=args.save_locally)
            outnames.append(outname)
        elif args.format == "mbfits":
            outname, mbfits = launch_mbfits_creator(
                fname,
                args.format,
                test=args.test,
                wrap=False,
                detrend=args.detrend,
                save_locally=args.save_locally,
            )

            if args.test:
                fname = "20180212-150835-S0000-3C84_RA"
            matchobj = match_srt_name(fname)
            if matchobj:
                date = matchobj.group(1)

                new_name = f"{mbfits.site.strip().upper()}_{date}_{mbfits.obsid:04d}_{next(iter(mbfits.FEBE.keys()))}"
                if os.path.exists(new_name):
                    shutil.rmtree(new_name)
                shutil.move(outname, new_name)
                outname = new_name
            outnames.append(outname)
        elif args.format == "mbfitsw":
            outname, mbfits = launch_mbfits_creator(
                fname,
                args.format,
                test=args.test,
                wrap=True,
                detrend=args.detrend,
                save_locally=args.save_locally,
            )
            outnames.append(outname)
        elif args.format == "classfits":
            outname, mbfits = launch_classfits_creator(
                fname,
                args.format,
                test=args.test,
                save_locally=args.save_locally,
            )
            outnames.append(outname)
        elif args.format == "sdfits":
            outname, mbfits = launch_sdfits_creator(
                fname,
                args.format,
                test=args.test,
                save_locally=args.save_locally,
            )
            outnames.append(outname)
        else:
            warnings.warn("Unknown output format", AstropyWarning)
    return outnames
