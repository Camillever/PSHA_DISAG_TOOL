""" Module containing all plots used for PSHA or disaggregation results by Openquake """
import os
import sys
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import cm  # import colormap
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.patches import Patch
import seaborn as sns
import typing
from typing import List, Dict

wd = os.getcwd()
sys.path.insert(0, wd)

from psha_disag_mod.utils import *
from psha_disag_mod.compartiment import *

###########################################
## PSHA


def hazard_curves_plot(
    metadata: Dict,
    files_folder: str,
    files: List[str],
    type_plot: str = "all_type_acc",
    plotsave_folder: str = None,
    show: bool = True,
):
    """Plot the curve of PSHA calculation results.

    Args:
        files_folder (str): folder containing the csv files
        files (List[str]): List of filenames
        type_plot (str, optional): Type of plot wanted :
            - "all_type_acc" plots all threshold of acceleration on one plot.
                The given list of filenames (files input) is all the filenames written as :
                "hazard_curve-mean-{type_acc}_{seed}.csv" with type_acc : PGA, SA(...), ...
            - "all_type_data" plots for the given threshold of acceleration all type of data (mean, quantile) on one plot.
                The given list of filenames (files input) is all the filenames written as, for the given type_acc (PGA in instance):
                "{startname}_curve-{type_data}-PGA_{seed}.csv" with startname_[...]_type_data : quantile_[...]_0.5, hazard_[...]_mean, ...
            Defaults to "all_type_acc".
        plotsave_folder (str, optional): Folder path to save plot(s). Defaults to None.
        show (bool, optional): Display the figure is True. Defaults to True.
    """
    fig_curve = plt.figure(figsize=[11, 7])

    if type_plot == "all_type_acc":
        colors = plt.cm.rainbow(np.linspace(0, 1, len(files)))
        linestyles = ["-"] * len(files)
        plt.title(
            f" Annual Probability of exceedance in function of acceleration \n for each acceleration threshold",
            fontsize=18,
            fontfamily="serif",
            fontweight="demibold",
        )
    else:
        assert len(files) == 4
        colors = ["black", "black", "black", "black"]
        linestyles = ["-"] * 4
        type_acc = read_psha_params(files[0])["type_acc"]
        plt.title(
            f" Annual Probability of exceedance in function of acceleration \n {type_acc}",
            fontsize=18,
            fontfamily="serif",
            fontweight="demibold",
        )

    for index_file, filename in enumerate(files):
        df = pd.read_csv(os.path.join(files_folder, filename), header=1)
        all_poes_str = df.columns[3:]
        acc_values = [extract_poes_value(str, sep="-") for str in all_poes_str]
        poes_values = [float(df[str(poes_name)]) for poes_name in all_poes_str]
        if type_plot == "all_type_acc":
            line_label = read_psha_params(filename)["type_acc"]
        else:
            line_label = read_psha_params(filename)["type_data"]
            if line_label == "mean":
                colors[index_file] = "red"
            else:
                if line_label == "0.05" or line_label == "0.95":
                    linestyles[index_file] = "--"
                line_label = "quantile " + line_label

        plt.plot(
            acc_values,
            poes_values,
            label=line_label,
            color=colors[index_file],
            linestyle=linestyles[index_file],
        )

    plt.xscale("log")
    plt.xticks(fontsize=14)
    plt.xlabel("Acc. [g]", fontfamily="serif", fontsize=16)
    plt.yscale("log")
    plt.yticks(fontsize=14)
    plt.ylabel("Annual Probability of exceedance", fontfamily="serif", fontsize=16)
    plt.legend(prop={"family": "serif", "size": 14})
    plt.grid()
    plt.tight_layout()
    if show:
        plt.show()
    if plotsave_folder is not None:
        if type_plot == "all_type_data":
            type_plot = f"{type_plot}_{type_acc}"
        fig_name = f"hazard_curve_{type_plot}_plot.png"
        fig_path = os.path.join(plotsave_folder, fig_name)
        fig_curve.savefig(fig_path, bbox_inches="tight")


def hazard_UHS_plot(
    metadata: Dict,
    files_folder: str,
    files: List[str],
    plotsave_folder: str = None,
    show: bool = True,
):

    fig_uhs = plt.figure(figsize=[11, 7])
    assert len(files) == len(metadata["output"]["type_data"] + 1)
    all_poes = metadata["output"]["poes"]
    colors = ["black"] * len(files)
    linestyles = ["-"] * len(files)
    for poe in all_poes:
        for index_file, filename in enumerate(files):
            df = pd.read_csv(os.path.join(files_folder, filename), header=1)
            all_freq_acc_str = df.columns[2:]
            if index_file == 0:  # Extract the return period concerned
                # poes = extract_poes_value(all_freq_acc_str[0], sep="~")
                return_period = int(1 / float(poe))
                plt.title(
                    f" Uniformed Hazard (response) Spectra \n {return_period} years",
                    fontsize=18,
                    fontfamily="serif",
                    fontweight="demibold",
                )

            freq_values = [extract_frequency(str) for str in all_freq_acc_str]
            acc_values = [float(df[str(column)]) for column in all_freq_acc_str]

            line_label = read_psha_params(filename)["type_data"]
            if line_label == "mean":
                colors[index_file] = "red"
            else:
                if line_label == "0.05" or line_label == "0.95":
                    linestyles[index_file] = "--"
                line_label = "quantile " + line_label

            plt.plot(
                freq_values,
                acc_values,
                label=line_label,
                color=colors[index_file],
                linestyle=linestyles[index_file],
            )

        plt.xscale("log")
        plt.xticks(fontsize=14)
        plt.xlabel("Frequency [Hz]", fontfamily="serif", fontsize=16)
        plt.yscale("log")
        plt.yticks(fontsize=14)
        plt.ylabel("Acceleration [g]", fontfamily="serif", fontsize=16)
        plt.legend(prop={"family": "serif", "size": 14})
        plt.grid()
        plt.tight_layout()
        if show:
            plt.show()
        if plotsave_folder is not None:
            fig_name = f"hazard_uhs_{return_period}_plot.png"
            fig_path = os.path.join(plotsave_folder, fig_name)
            fig_uhs.savefig(fig_path, bbox_inches="tight")


###########################################
## DISAGGREGATION


def disag_hist3D_plot(
    metadata: Dict,
    files_folder: str,
    files: List[str],
    plotsave_folder: str = None,
    show: bool = True,
):
    """3D histogram - disaggregation results (Mag/Dist/Weight)

    Args:
        files_folder (str): Folder containing all output results files of Openquake
        files (List[str]): Filename ('Mag_Dist-0_{seed}.csv') of disaggregation results
        all_poes (List[float]): List of all values of poes
        Magbin (float): Magnitudes bin
        Distbin (float): Distance bin
        plotsave_folder (str, optional): Folder path where plots are saved. Defaults to None.
        show (bool, optional): Display figures on matplotlib window. Defaults to True.

    Returns:
        _type_: _description_
    """

    assert len(files) == 1
    types_acc = metadata["calculation"]["im_types_levels"].keys()
    all_poes = metadata["disaggregation"]["disag_poes"]
    Magbin = metadata["disaggregation"]["magbin"]
    Distbin = metadata["disaggregation"]["distbin"]
    eps = metadata["disaggregation"]["eps"]

    for poe in all_poes:
        for type_acc in types_acc:
            fig_hist3D = plt.figure(figsize=[11, 7])
            frequency = equivalent_frequency(type_acc)
            period_return = 1 / float(poe)
            plt.title(
                f" Return period : {period_return:.0f} years \
                    \n Seismic Hazard Weight in function of Magnitude and Distance\
                     \n F = {frequency:.2f} Hz "
            )
            ax = plt.axes(projection="3d")
            df = pd.read_csv(
                os.path.join(files_folder, files[0]), header=1, index_col=0
            )

            colorbar = cm.get_cmap("hsv", eps)
            Mag, Dist, dz = [], [], []
            for eps_index in range(eps):
                eps_value = df.eps[eps_index]
                # print("eps_value :", eps_value)
                df_poe_eps = df[(df["poe"] == float(poe)) & (df["eps"] == eps_value)]
                # print("df_poe_eps :", df_poe_eps)
                Mag.append(list(df_poe_eps.mag[type_acc]))
                Dist.append(list(df_poe_eps.dist[type_acc]))
                dz.append(list(df_poe_eps.rlz5[type_acc]))
            dx = np.ones(len(Mag[0])) * Magbin / 1.5
            dy = np.ones(len(Mag[0])) * Distbin / 1.5
            rlz = np.zeros(len(Mag[0]))
            z_pos = rlz
            for eps_index in range(eps):
                eps_value = df.eps[eps_index]
                eps_legend = f"{eps_index} eps"
                # print("z_pos :", z_pos)
                # print("len(z_pos) :", len(z_pos))
                ax.bar3d(
                    Mag[eps_index],
                    Dist[eps_index],
                    z_pos,
                    dx,
                    dy,
                    dz[eps_index],
                    color=colorbar(np.linspace(0, 1, eps))[eps_index],
                    label=eps_legend,
                )
                z_pos += dz[eps_index]
            ax.set_xlabel("Magnitude")
            ax.set_ylabel("Distance [km]")
            ax.set_zlabel("Contribution")
            # plt.legend()
            if show:
                plt.show()
            if plotsave_folder is not None:
                fig_name = f"disagg_Mag_Dist_hist3Dplot_{poe}_{type_acc}.png"
                fig_path = os.path.join(plotsave_folder, fig_name)
                fig_hist3D.savefig(fig_path, bbox_inches="tight")


def disagg_MReps(
    Mbin, dbin, poe_disagg, path_disagg_results, output_dir, n_rows=1, iplot=False
):
    """
    This scripts reads the results of the disaggregation

    Parameters
    ----------
    poe_disagg : list
        disaggregation probability of exceedances
    path_disagg_results: str
        Path to the hazard results
        :param iplot:
        :param Mbin:
        :param dbin:
        :param n_rows:


    """
    cmap = cm.get_cmap("gnuplot2")  # Get desired colormap
    lat = []
    lon = []
    modeLst, meanLst = [], []
    im = []
    poe = []
    Tr = []
    apoe_norm = []
    M, R, eps = [], [], []
    probs = []
    mags = []
    dists = []

    for file in os.listdir(path_disagg_results):
        if file.startswith("rlz") and file.find("Mag_Dist_Eps") > 0:
            print("passed")
            # Load the dataframe
            df = pd.read_csv("".join([path_disagg_results, "/", file]), skiprows=1)
            # Strip the IM out of the file name
            im.append(file.rsplit("-")[2])
            # Get some salient values
            f = open("".join([path_disagg_results, "/", file]), "r")
            ff = f.readline().split(",")
            try:  # for OQ version <3.11
                inv_t = float(ff[9].replace(" investigation_time=", ""))
                poe.append(float(ff[12].replace(" poe=", "").replace("'", "")))
            except:
                inv_t = float(ff[6].replace(" investigation_time=", ""))
                poe.append(
                    float(
                        ff[-1].replace(" poe=", "").replace('"', "").replace("\n", "")
                    )
                )
            lon.append(float(ff[10].replace(" lon=", "")))
            lat.append(float(ff[11].replace(" lat=", "")))
            Tr.append(-inv_t / np.log(1 - poe[-1]))

            # Extract the poe and annualise
            df["apoe"] = -np.log(1 - df["poe"]) / inv_t

            # Normalise the apoe for disaggregation plotting
            df["apoe_norm"] = df["apoe"] / df["apoe"].sum()
            apoe_norm.append(df["apoe_norm"])

            # Compute the modal value (highest apoe)
            mode = df.sort_values(by="apoe_norm", ascending=False)[0:1]
            modeLst.append(
                [mode["mag"].values[0], mode["dist"].values[0], mode["eps"].values[0]]
            )

            # Compute the mean value
            meanLst.append(
                [
                    np.sum(df["mag"] * df["apoe_norm"]),
                    np.sum(df["dist"] * df["apoe_norm"]),
                    np.sum(df["eps"] * df["apoe_norm"]),
                ]
            )

            M.append(df["mag"])
            R.append(df["dist"])
            eps.append(df["eps"])
            probs.append(df["poe"])

    lon = [x for _, x in sorted(zip(Tr, lon))]
    lat = [x for _, x in sorted(zip(Tr, lat))]
    im = [x for _, x in sorted(zip(Tr, im))]
    M = [x for _, x in sorted(zip(Tr, M))]
    R = [x for _, x in sorted(zip(Tr, R))]
    eps = [x for _, x in sorted(zip(Tr, eps))]
    apoe_norm = [x for _, x in sorted(zip(Tr, apoe_norm))]
    modeLst = [x for _, x in sorted(zip(Tr, modeLst))]
    meanLst = [x for _, x in sorted(zip(Tr, meanLst))]

    Tr = -inv_t / np.log(1 - np.asarray(poe_disagg))
    n_Tr = len(np.unique(np.asarray(Tr)))
    Tr = sorted(Tr)
    ims = np.unique(im)
    n_im = len(ims)
    n_eps = len(np.unique(np.asarray(eps)))
    min_eps = np.min(
        np.unique(np.asarray(eps))
    )  # get range of colorbars so we can normalize
    max_eps = np.max(np.unique(np.asarray(eps)))

    lon = lon[0]
    lat = lat[0]

    n_cols = int(np.floor(n_Tr / n_rows))
    if np.mod(n_Tr, n_rows):
        n_cols += 1
    if iplot:
        for idx1 in range(n_im):
            fig = plt.figure(figsize=(19.2, 10.8))
            for idx2 in range(n_Tr):
                i = idx1 * n_Tr + idx2
                ax1 = fig.add_subplot(n_rows, n_cols, idx2 + 1, projection="3d")

                # scale each eps to [0,1], and get their rgb values
                rgba = [
                    cmap((k - min_eps) / max_eps / 2)
                    for k in (np.unique(np.asarray(eps)))
                ]
                num_triads_M_R_eps = len(R[i])
                Z = np.zeros(int(num_triads_M_R_eps / n_eps))

                for l in range(n_eps):
                    X = np.array(R[i][np.arange(l, num_triads_M_R_eps, n_eps)])
                    Y = np.array(M[i][np.arange(l, num_triads_M_R_eps, n_eps)])

                    dx = np.ones(int(num_triads_M_R_eps / n_eps)) * dbin / 2
                    dy = np.ones(int(num_triads_M_R_eps / n_eps)) * Mbin / 2
                    dz = (
                        np.array(apoe_norm[i][np.arange(l, num_triads_M_R_eps, n_eps)])
                        * 100
                    )

                    ax1.bar3d(
                        X,
                        Y,
                        Z,
                        dx,
                        dy,
                        dz,
                        color=rgba[l],
                        zsort="average",
                        alpha=0.7,
                        shade=True,
                    )
                    Z += (
                        dz  # add the height of each bar to know where to start the next
                    )

                ax1.set_xlabel("Rjb [km]")
                ax1.set_ylabel("$M_{w}$")
                if np.mod(idx2 + 1, n_cols) == 1:
                    ax1.set_zlabel("Hazard Contribution [%]")
                    ax1.zaxis.set_rotate_label(False)  # disable automatic rotation
                    ax1.set_zlabel("Hazard Contribution [%]", rotation=90)
                ax1.zaxis._axinfo["juggled"] = (1, 2, 0)

                plt.title(
                    "$T_{R}$=%s years\n$M_{mod}$=%s, $R_{mod}$=%s km, $\epsilon_{mod}$=%s\n$M_{mean}$=%s, $R_{mean}$=%s "
                    "km, $\epsilon_{mean}$=%s"
                    % (
                        "{:.0f}".format(Tr[i]),
                        "{:.2f}".format(modeLst[i][0]),
                        "{:.0f}".format(modeLst[i][1]),
                        "{:.1f}".format(modeLst[i][2]),
                        "{:.2f}".format(meanLst[i][0]),
                        "{:.0f}".format(meanLst[i][1]),
                        "{:.1f}".format(meanLst[i][2]),
                    ),
                    fontsize=11,
                    loc="right",
                    va="top",
                    y=0.95,
                )

                mags.append(meanLst[i][0])
                dists.append(meanLst[i][1])

            legend_elements = []
            for j in range(n_eps):
                legend_elements.append(
                    Patch(
                        facecolor=rgba[n_eps - j - 1],
                        label="\u03B5 = %.2f"
                        % (np.unique(np.asarray(eps))[n_eps - j - 1]),
                    )
                )

            fig.legend(
                handles=legend_elements,
                loc="lower center",
                bbox_to_anchor=(0.5, 0.05),
                borderaxespad=0.0,
                ncol=n_eps,
            )
            plt.subplots_adjust(
                hspace=0.05, wspace=0.05
            )  # adjust the subplot to the right for the legend
            fig.suptitle(
                "Disaggregation of Seismic Hazard\nIntensity Measure: %s\nLatitude: %s, Longitude: %s"
                % (ims[idx1], "{:.4f}".format(lat), "{:.4f}".format(lon)),
                fontsize=14,
                weight="bold",
                ha="left",
                x=0.12,
                y=0.97,
            )
            fname = os.path.join(
                output_dir, "Disaggregation_MReps_" + ims[idx1] + ".png"
            )
            plt.savefig(fname, format="png", dpi=600)
            # plt.show()
            plt.close()

    return meanLst, M, R, probs
