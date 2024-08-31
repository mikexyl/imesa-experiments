#!/usr/bin/env python3

import argparse
import yaml
import seaborn as sns
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Liberation Serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["pdf.fonttype"] = 42
# set font size
plt.rcParams.update({"font.size": 18})
figsize = (8, 5)  # Adjust the width (10) and height (6)
markerscale = 1.5  # Adjust the size of the markers in the legend
scattersize = 80
boxanchors = (0.5, -0.15)  # Adjust the position of the legend


SNS_BLUE = "#0173b2"
SNS_ORANGE = "#de8f05"
SNS_GREEN = "#029e73"
SNS_RED = "#d55e00"
SNS_PURPLE = "#cc78bc"
SNS_BROWN = "#ca9161"
SNS_PINK = "#fbafe4"
SNS_GREY = "#949494"
SNS_YELLOW = "#ece133"
SNS_LIGHT_BLUE = "#56b4e9"


METHOD_STYLE_SHEET = {
    "centralized": {
        "name": "Centralized",
        "color": SNS_GREY,
        "symbol": "o",
        "linestyle": "solid",
        "zorder": 1,
    },
    "independent": {
        "name": "Independent",
        "color": SNS_PURPLE,
        "symbol": "d",
        "linestyle": "solid",
        "zorder": 2,
    },
    "ddfsam2": {
        "name": "DDF-SAM2",
        "color": SNS_GREEN,
        "symbol": "X",
        "linestyle": "solid",
        "zorder": 3,
    },
    "imesa": {
        "name": "iMESA",
        "color": SNS_BLUE,
        "symbol": "h",
        "linestyle": "solid",
        "zorder": 4,
    },
    "raido": {
        "name": "RaiDO",
        "color": SNS_ORANGE,
        "symbol": "s",
        "linestyle": "solid",
        "zorder": 6,
    },
    "raido_kn": {
        "name": "RaiDOInit",
        "color": SNS_RED,
        "symbol": "s",
        "linestyle": "solid",
    },
}

LOG_Y_SCALE = False


def get_valid_data(data, status, repeat):
    # take any of every repeat statuses
    run_status = [any(status[i : i + repeat]) for i in range(0, len(status), repeat)]
    run_status = np.array(run_status)
    mean_data = np.array(len(status) * [0.0]).flatten()
    mean_data[status == True] = data
    mean_data[status == False] = np.nan

    valid_mean = np.array(len(run_status) * [0.0])
    for i in range(0, len(run_status)):
        if run_status[i] == True:
            total = 0
            n = 0
            for j in range(0, repeat):
                if status[i * repeat + j] == True:
                    total += mean_data[i * repeat + j]
                    n += 1
            valid_mean[i] = total / n

    x = range(len(run_status))

    valid_x = np.array(
        [x[i] for i in range(0, len(run_status)) if run_status[i] == True]
    )
    valid_mean = valid_mean[valid_mean > 0]

    return valid_x, valid_mean, run_status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="/workspaces/src/imesa-experiments/data/results/metric_summary.pkl",
    )
    args = parser.parse_args()
    # Create a scatter plot with Seaborn
    # sns.set(style="whitegrid")  # Set the style of the plot

    # load the yaml file
    aggregated_results = None
    with open(args.input, "rb") as pickle_file:
        aggregated_results = pkl.load(pickle_file)

    iv = "2d_5r_noised_prior"

    n_data = 0

    method_list = ["raido", "imesa", "ddfsam2", "independent", "centralized"]
    methods_reverse = method_list
    methods_reverse.reverse()

    fig_noise = plt.figure(figsize=figsize)

    last_value = {}
    first_value = {}
    all_success = {}
    repeat = 3
    for method in methods_reverse:
        if method not in aggregated_results[iv]:
            continue
        data = aggregated_results[iv][method]["iate_trans"]
        status = aggregated_results[iv][method]["statuses"]
        status = np.array(status)

        valid_x, valid_mean, run_status = get_valid_data(data, status, repeat)

        n_data = len(run_status)

        # set line alpha to 0.5 dashed lines
        if all(run_status):
            all_success[method] = True
            sns.lineplot(
                x=valid_x,
                y=valid_mean,
                alpha=0.7,
                color=METHOD_STYLE_SHEET[method]["color"],
                linestyle="solid",
                zorder=METHOD_STYLE_SHEET[method]["zorder"],
            )
        sns.scatterplot(
            x=valid_x,
            y=valid_mean,
            label=METHOD_STYLE_SHEET[method]["name"],
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=scattersize,
            zorder=METHOD_STYLE_SHEET[method]["zorder"],
        )

        last_value[method] = valid_mean[-1]
        if method not in first_value:
            first_value[method] = valid_mean[0]

    has_nr = "2d_nr" in aggregated_results

    iv = "2d_5r_zero_prior"
    for method in methods_reverse:
        if method not in aggregated_results[iv]:
            continue
        data = aggregated_results[iv][method]["iate_trans"]
        if len(data) == 0:
            continue
        data = [sum(data) / len(data)]
        x = 0.5 + n_data
        sns.scatterplot(
            x=[x],
            y=data,
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=scattersize,
            zorder=METHOD_STYLE_SHEET[method]["zorder"],
        )
        if method in all_success and all_success[method]:
            plt.plot(
                [n_data - 1, x],
                [last_value[method], data[0]],
                alpha=1.0,
                color=METHOD_STYLE_SHEET[method]["color"],
                linestyle="--",
                zorder=METHOD_STYLE_SHEET[method]["zorder"],
            )

    iv = "2d_5r_gt_prior"
    for method in methods_reverse:
        if method not in aggregated_results[iv]:
            continue
        data = aggregated_results[iv][method]["iate_trans"]
        if len(data) == 0:
            continue
        # take the average of all the values
        data = [sum(data) / len(data)]
        x = -1.5
        sns.scatterplot(
            x=[x],
            y=data,
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=scattersize,
            zorder=METHOD_STYLE_SHEET[method]["zorder"],
        )
        if method in all_success and all_success[method]:
            plt.plot(
                [-1.5, 0],
                [data[0], first_value[method]],
                alpha=1.0,
                color=METHOD_STYLE_SHEET[method]["color"],
                linestyle="--",
                zorder=METHOD_STYLE_SHEET[method]["zorder"],
            )

    # Add title and labels
    # plt.title("iATE vs. Noise of initialization.")
    # Set x-axis limits to create a separation
    plt.xlim(-2, n_data + 1)

    # Customize x-axis labels to create a gap and label the isolated column as "inf"
    plt.xticks(
        [-1.5] + list(range(0, n_data)) + [n_data + 0.5],
        ["GT"] + list(range(1, n_data + 1)) + ["  None"],
    )

    plt.yscale("log" if LOG_Y_SCALE else "linear")

    plt.xlabel("Noise of initialization (m)")
    plt.ylabel("iATE(Translation)")
    # Extract handles and labels from the original legend
    handles, labels = plt.gca().get_legend_handles_labels()

    # Reverse the order of handles and labels
    handles.reverse()
    labels.reverse()
    plt.legend(
        handles,
        labels,
        markerscale=markerscale,
        handletextpad=0.0,
        fontsize="medium",
        loc="upper center",
        # Adjusted the vertical position further down
        bbox_to_anchor=boxanchors,
        ncol=5,
        frameon=False,  # Draw a frame around the legend
        borderpad=0.1,  # Padding inside the legend box
        labelspacing=0.1,  # Vertical space between legend entries
        handlelength=1,  # Length of the legend markers
        handleheight=1,  # Height of the legend markers
        borderaxespad=1.0,  # Padding between the axes and the legend box
        columnspacing=0.5,  # Space between the columns
    )
    plt.subplots_adjust(bottom=0.22)  # Add space at the bottom of the figure

    # Disable the grid lines entirely
    plt.grid(False)

    # Manually add grid lines except for the gap
    for i in range(0, n_data):
        plt.axvline(x=i, color="lightgrey", linestyle="--", linewidth=0.7, zorder=0)

    # Add a grid line for the "inf" column if desired
    plt.axvline(
        x=n_data + 0.5, color="lightgrey", linestyle="--", linewidth=0.7, zorder=0
    )

    plt.axvline(x=-1.5, color="lightgrey", linestyle="--", linewidth=0.7, zorder=0)

    for i in range(2, 10, 2):
        plt.axhline(y=i, color="lightgrey", linestyle="--", linewidth=0.7, zorder=0)

    # set font to serif

    # save svg
    plt.savefig("iate_noise.svg")
    plt.savefig("iate_noise.pdf")

    handles, labels = plt.gca().get_legend_handles_labels()

    # Show the plot
    plt.show(block=False)

    fig_nr = plt.figure(figsize=figsize)
    plt.grid(True, linestyle="--", zorder=0)

    if not has_nr:
        return

    repeat = 3
    nr_range = range(2, 21, 2)
    for method in method_list:
        data = aggregated_results["2d_nr"][method]["iate_trans"]
        if len(data) == 0:
            continue
        status = aggregated_results["2d_nr"][method]["statuses"]
        # take all of every repeat statuses
        status = np.array(status)

        valid_x, valid_mean, run_status = get_valid_data(data, status, repeat)

        valid_x = valid_x * 2 + 2
        all_success = all(run_status)

        # set line alpha to 0.5 dashed lines
        if all_success:
            sns.lineplot(
                x=valid_x,
                y=valid_mean / valid_x,
                alpha=0.7,
                color=METHOD_STYLE_SHEET[method]["color"],
                linestyle="solid",
                zorder=METHOD_STYLE_SHEET[method]["zorder"],
            )
        sns.scatterplot(
            x=valid_x,
            y=valid_mean / valid_x,
            label=METHOD_STYLE_SHEET[method]["name"],
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=scattersize,
            zorder=METHOD_STYLE_SHEET[method]["zorder"],
        )

    # Add title and labels
    # plt.title("iATE vs. Number of robots.")
    plt.xticks(nr_range, nr_range)
    # Extract handles and labels from the original legend
    handles, labels = plt.gca().get_legend_handles_labels()

    # Reverse the order of handles and labels
    handles.reverse()
    labels.reverse()
    plt.legend(
        handles,
        labels,
        markerscale=markerscale,
        handletextpad=0.0,
        fontsize="medium",
        loc="upper center",
        # Adjusted the vertical position further down
        bbox_to_anchor=boxanchors,
        ncol=5,
        frameon=False,  # Draw a frame around the legend
        borderpad=0.1,  # Padding inside the legend box
        labelspacing=0.1,  # Vertical space between legend entries
        handlelength=1,  # Length of the legend markers
        handleheight=1,  # Height of the legend markers
        borderaxespad=1.0,  # Padding between the axes and the legend box
        columnspacing=0.5,  # Space between the columns
    )
    plt.subplots_adjust(bottom=0.22)  # Add space at the bottom of the figure

    plt.xlabel("Number of robots")
    plt.ylabel("Mean iATE(Translation)")

    # save svg
    plt.savefig("iate_nr.svg")
    plt.savefig("iate_nr.pdf")

    # Show the plot
    plt.show(block=True)


if __name__ == "__main__":
    main()
