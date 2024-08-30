#!/usr/bin/env python3

import argparse
import yaml
import seaborn as sns
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt

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
    },
    "independent": {
        "name": "Independent",
        "color": SNS_PURPLE,
        "symbol": "d",
        "linestyle": "solid",
    },
    "ddfsam2": {
        "name": "DDF-SAM2",
        "color": SNS_GREEN,
        "symbol": "X",
        "linestyle": "solid",
    },
    "imesa": {
        "name": "iMESA",
        "color": SNS_BLUE,
        "symbol": "*",
        "linestyle": "solid",
    },
    "raido": {
        "name": "RaiDO",
        "color": SNS_ORANGE,
        "symbol": "s",
        "linestyle": "solid",
    },
    "raido_kn": {
        "name": "RaiDOInit",
        "color": SNS_RED,
        "symbol": "s",
        "linestyle": "solid",
    },
}


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
    sns.set(style="whitegrid")  # Set the style of the plot

    print(args.input)
    # load the yaml file
    aggregated_results = None
    with open(args.input, "rb") as pickle_file:
        aggregated_results = pkl.load(pickle_file)

    iv = "2d_5r_noised_prior"

    for method in aggregated_results[iv]:
        print(method)
        data = aggregated_results[iv][method]["iate_trans"]
        # average every 3 values
        data = [sum(data[i : i + 3]) / 3 for i in range(0, len(data), 3)]

        n = len(data)
        print(n)
        x = range(n)
        x = np.array(x)+5

        # set line alpha to 0.5 dashed lines
        sns.lineplot(
            x=x,
            y=data,
            alpha=0.7,
            color=METHOD_STYLE_SHEET[method]["color"],
            linestyle="solid",
        )
        sns.scatterplot(
            x=x,
            y=data,
            label=METHOD_STYLE_SHEET[method]["name"],
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=50,
        )

    # Add title and labels
    plt.title("iATE vs. Noise of initialization.")
    plt.xlabel("Noise of initialization (m)")
    plt.ylabel("iATE")
    plt.legend(
        markerscale=1.5,
        handletextpad=0.5,
        fontsize="medium",
        loc="upper center",
        # Adjusted the vertical position further down
        bbox_to_anchor=(0.5, -0.2),
        ncol=3,
        frameon=False,  # Draw a frame around the legend
        borderpad=0.3,  # Padding inside the legend box
        labelspacing=0.5,  # Vertical space between legend entries
        handlelength=2,  # Length of the legend markers
        handleheight=2,  # Height of the legend markers
        borderaxespad=0.5,  # Padding between the axes and the legend box
        columnspacing=0.5,  # Space between the columns
    )
    plt.subplots_adjust(bottom=0.3)  # Add space at the bottom of the figure

    # save svg
    plt.savefig("iate_noise.svg")

    has_nr = "2d_nr_noised" not in aggregated_results

    # Show the plot
    plt.show(block=~has_nr)

    fig_nr = plt.figure()

    if not has_nr:
        return

    for method in aggregated_results["2d_nr_noised"]:
        data = aggregated_results["2d_nr_noised"][method]["iate_trans"]
        # average every 3 values
        n = len(data)
        print(n)
        x = range(n)
        x = np.array(x)+2

        # set line alpha to 0.5 dashed lines
        sns.lineplot(
            x=x,
            y=data,
            alpha=0.7,
            color=METHOD_STYLE_SHEET[method]["color"],
            linestyle="solid",
        )
        sns.scatterplot(
            x=x,
            y=data,
            label=METHOD_STYLE_SHEET[method]["name"],
            marker=METHOD_STYLE_SHEET[method]["symbol"],
            color=METHOD_STYLE_SHEET[method]["color"],
            s=60,
        )

    # Add title and labels
    plt.title("iATE vs. Number of robots.")
    plt.xlabel("Noise of initialization (m)")
    plt.ylabel("iATE(trans)")
    plt.legend(
        markerscale=1,
        handletextpad=0.5,
        fontsize="medium",
        loc="upper center",
        # Adjusted the vertical position further down
        bbox_to_anchor=(0.5, -0.2),
        ncol=3,
        frameon=False,  # Draw a frame around the legend
        borderpad=0.3,  # Padding inside the legend box
        labelspacing=0.5,  # Vertical space between legend entries
        handlelength=2,  # Length of the legend markers
        handleheight=2,  # Height of the legend markers
        borderaxespad=0.5,  # Padding between the axes and the legend box
        columnspacing=0.5,  # Space between the columns
    )
    plt.subplots_adjust(bottom=0.3)  # Add space at the bottom of the figure

    # save svg
    plt.savefig("iate_nr.svg")

    # Show the plot
    plt.show(block=True)


if __name__ == "__main__":
    main()
