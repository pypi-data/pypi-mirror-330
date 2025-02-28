import glob
import os
import warnings

import numpy as np

import astropy.units as u
from astropy.table import Table, vstack
from astropy.time import Time

from . import logging
from .fit import contiguous_regions
from .read_config import read_config

try:
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def load_data(fnames, outroot=None):
    if outroot is None:
        outroot = ""
    else:
        outroot = outroot.rstrip("_") + "_"
    tables = {}

    for fname in sorted(fnames):
        full_table = Table.read(fname)
        backend = full_table.meta["backend"]
        if backend == "TP":
            logging.info(f"Skipping {fname} because it is a total power dataset.")
            continue

        receiver = full_table.meta["receiver"]

        channels = [col for col in full_table.colnames if col.startswith("Feed")]

        for ch in channels:
            label = f"{receiver}_{backend}_{ch}"
            logging.info(f"{fname} - {label}")
            if label not in tables:
                tables[label] = []
            if "bad_chans" not in full_table[ch].meta:
                continue
            start_freq = full_table[ch].meta["frequency"].to(u.MHz).value

            bad_chans = np.array(list(full_table[ch].meta["bad_chans"].keys()))
            bad_freqs = np.array(list(full_table[ch].meta["bad_chans"].values()))
            times = [Time(full_table[ch].meta["DATE"]).mjd] * len(bad_freqs)
            new_tab = {
                "time": times,
                "freq_chans": bad_chans,
                "ref_freq": [start_freq] * len(bad_freqs),
                "freq_from_ref": bad_freqs,
            }
            for coord in "ra", "dec", "az", "el":
                new_tab[coord] = [np.rad2deg(full_table[coord][0])] * len(bad_freqs)
            tables[label].extend(Table(new_tab))

    outfiles = []
    for label, local_tables in tables.items():
        if len(local_tables) == 0:
            continue
        outfile = f"{outroot}{label}_rfi.hdf5"
        table = vstack(local_tables)
        table.write(outfile, path="data", overwrite=True)
        outfiles.append(outfile)
    return outfiles


def main_rfistat(args=None):
    import argparse

    description = "Calculate statistics on the RFI filtered out by SDTpreprocess."

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "files",
        nargs="*",
        help="List of files produced by SDTimage or SDTpreprocess (HDF5 format).",
        type=str,
    )
    parser.add_argument(
        "--threshold", help=r"Threshold (%% from maximum) for RFI flagging", default=10, type=float
    )
    parser.add_argument("-c", "--config", type=str, default=None, help="Config file")

    parser.add_argument("--outroot", help="Root for output files", default=None, type=str)
    args = parser.parse_args(args)

    preproc_files = args.files

    if len(preproc_files) == 0 and args.config is not None:
        config = read_config(args.config)
        datadir = config["datadir"]
        dirlist = config["list_of_directories"]
        preproc_files = []
        for d in dirlist:
            preproc_files.extend(glob.glob(os.path.join(datadir, d, "*.hdf5")))

    if len(preproc_files) == 0:
        outfiles = glob.glob("*rfi.hdf5")
    else:
        outfiles = load_data(preproc_files)

    receiver_class_data = {}
    for fname in outfiles:
        if args.outroot is not None:
            fname = fname.replace(args.outroot + "_", "")

        receiver = fname[:3]
        if receiver not in receiver_class_data:
            receiver_class_data[receiver] = []
        receiver_class_data[receiver].append(fname)

    if not HAS_MPL:
        warnings.warn("Matplotlib is required for this function.")
        return

    for receiver, outfiles in receiver_class_data.items():
        logging.info(f"Treating data from {receiver}")
        fig1, axs = plt.subplots(
            nrows=len(outfiles) + 1,
            ncols=2,
            width_ratios=(3, 2),
            height_ratios=[0.6] + [1] * len(outfiles),
            constrained_layout=True,
            sharex="col",
            sharey="row",
            figsize=(10, 3.3333 * len(outfiles)),
        )
        tmin, tmax = np.inf, -np.inf
        fmin, fmax = np.inf, -np.inf
        coords_plotted = False
        for ax_row, outfile in zip(axs[1:], outfiles):
            logging.info(f"Plotting{outfile}")
            ax_scatter, ax_hist = ax_row
            label = outfile.replace("_rfi.hdf5", "")
            t = Table.read(outfile, path="data")
            mjd = t["time"]

            central_mjd = float(f"{mjd.mean():.0f}")
            time = (mjd - central_mjd) * 24
            data = t["freq_from_ref"] + t["ref_freq"]

            freq_chans = np.unique(t["freq_chans"])

            if not coords_plotted:
                time_label = Time(central_mjd, format="mjd").to_value("iso", subfmt="date")
                plt.suptitle(f"RFI stats for {receiver} on {time_label}")
                coords_plotted = True
                axs[0][0].plot(time, t["el"][:, 0], label="El", color="b", lw=0.5)
                axs[0][0].plot(time, t["az"][:, 0], label="Az", color="r", lw=0.5)
                axs[0][0].scatter(time, t["el"][:, 0], s=2, alpha=0.2, color="b")
                axs[0][0].scatter(time, t["az"][:, 0], s=2, alpha=0.2, color="r")
                axs[0][1].axis("off")

            ax_scatter.scatter(time, data, color="k", s=2, alpha=0.2)
            ax_scatter.set_xlabel(f"Time (hours since MJD {central_mjd})")

            ax_scatter.set_ylabel("Frequency (MHz)")
            ax_scatter.text(0.01, 0.95, label, transform=ax_scatter.transAxes)
            ax_scatter.grid(True)
            tmin = min(tmin, time.min())
            tmax = max(tmax, time.max())
            fmin = min(fmin, data.min())
            fmax = max(fmax, data.max())

            stat_bins = np.linspace(
                data.min() - 0.0001, data.max() + 0.0001, freq_chans.max() - freq_chans.min() + 1
            )
            data_hist, _, _ = ax_hist.hist(
                data, bins=stat_bins, orientation="horizontal", label="RFI", color="k"
            )
            # ax_hist.plot(data_hist, stat_bins[:-1], label="RFI", color="k")
            ax_hist.grid(True)

            threshold = args.threshold / 100 * data_hist.max()

            regs = contiguous_regions(data_hist > threshold)
            logging.info("Bad intervals:")
            bad_intervals_str = ""
            for r in regs:
                logging.info(f"{stat_bins[r[0]]}--{stat_bins[min(r[1], stat_bins.size - 1)]}")
                bad_intervals_str += (
                    f"{stat_bins[r[0]]}:{stat_bins[min(r[1], stat_bins.size - 1)]},"
                )
                for ax in ax_row:
                    ax.axhspan(stat_bins[r[0]], stat_bins[r[1]], color="r", alpha=0.3, zorder=10)

            bad_intervals_str = bad_intervals_str.rstrip(",")
            ax_hist.axvline(threshold, color="r")
            logging.info(f"Cleaning string from {outfile}: {bad_intervals_str}")

        for ax_row in axs:
            ax_scatter, ax_hist = ax_row
            ax_scatter.set_xlim(tmin - 60 / 3600, tmax + 60 / 3600)
        for ax_row in axs[1:]:
            ax_scatter, ax_hist = ax_row
            ax_scatter.set_ylim(fmin - 1, fmax + 1)

        axs[0][0].set_xlabel(f"Time (hours since MJD {central_mjd})")
        axs[0][0].set_ylabel("Angle (deg)")
        axs[0][0].legend()
        axs[0][0].grid(True)
        plt.tight_layout()
        plt.savefig(f"rfi_stats_{receiver}_{time_label}.jpg", dpi=300)
        # plt.show()
