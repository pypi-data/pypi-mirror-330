from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sunpy.time import parse_time


def goes_proton_flux(
    data_type,
    primary=True,
    kst=False,
):
    sat_class = "primary" if primary else "secondary"

    assert data_type in [
        "6-hour",
        "1-day",
        "3-day",
        "7-day",
    ], "data_type must be one of ['6-hour', '1-day', '3-day', '7-day']"

    root = Path("figures")
    root.mkdir(exist_ok=True)

    # KST?
    if kst:
        td = timedelta(hours=9)
    else:
        td = timedelta(hours=0)

    # get current time
    now = datetime.now(timezone.utc) + td

    # get GOES X-ray data
    goes_json_data = pd.read_json(
        f"https://services.swpc.noaa.gov/json/goes/{sat_class}/integral-protons-{data_type}.json"
    )
    goes_10mev = goes_json_data[goes_json_data["energy"] == ">=10 MeV"]
    goes_50mev = goes_json_data[goes_json_data["energy"] == ">=50 MeV"]
    goes_100mev = goes_json_data[goes_json_data["energy"] == ">=100 MeV"]
    goes_500mev = goes_json_data[goes_json_data["energy"] == ">=500 MeV"]

    # get satellite number
    satellite = str(goes_json_data["satellite"].unique()[0])

    # get time range
    time_array = parse_time(goes_10mev["time_tag"]).datetime + td
    first_time = time_array[0]
    last_time = time_array[-1]

    # create figure and plot
    fig, ax = plt.subplots(figsize=(15, 10))

    # plot GOES Proton flux
    ax.plot(
        parse_time(goes_10mev["time_tag"]).datetime + td,
        goes_10mev["flux"].values,
        label=f"GOES-{satellite} " + r"$\geq$ 10 MeV",
        color="red",
    )
    ax.plot(
        parse_time(goes_50mev["time_tag"]).datetime + td,
        goes_50mev["flux"].values,
        label=f"GOES-{satellite} " + r"$\geq$ 50 MeV",
        color="blue",
    )
    ax.plot(
        parse_time(goes_100mev["time_tag"]).datetime + td,
        goes_100mev["flux"].values,
        label=f"GOES-{satellite} " + r"$\geq$ 100 MeV",
        color="green",
    )
    ax.plot(
        parse_time(goes_500mev["time_tag"]).datetime + td,
        goes_500mev["flux"].values,
        label=f"GOES-{satellite} " + r"$\geq$ 500 MeV",
        color="orange",
    )

    # set y-axis scale and limit
    ax.set_yscale("log")
    ax.set_ylim(1e-2, 1e4)
    ax.set_ylabel(
        r"Particles $\cdot$ cm$^{-2}$ $\cdot$ s$^{-1}$ $\cdot$ sr$^{-1}$",
        fontsize=25,
    )
    ax.yaxis.set_tick_params(labelsize=25)

    # set x-axis limit
    ax.set_xlim(first_time, last_time + timedelta(hours=1))
    ax.xaxis.set_tick_params(labelsize=25)

    # set grid and ticks
    ax.yaxis.grid(True, "major")
    ax.xaxis.grid(False, "major")
    ax.tick_params(axis="x", which="minor", length=4, width=1, color="black")
    ax.tick_params(axis="x", which="major", length=8, width=1, color="black")
    ax.tick_params(axis="y", which="minor", length=4, width=1, color="black")
    ax.tick_params(axis="y", which="major", length=8, width=1, color="black")

    # set y-axis labels (flare class)
    labels = [" ", " "]
    centers = np.logspace(-1, 1, len(labels))
    for value, label in zip(centers, labels):
        ax.text(
            1.02,
            value,
            label,
            transform=ax.get_yaxis_transform(),
            horizontalalignment="center",
        )

    # x-axis tick time format
    plt.xticks(rotation=0)
    if data_type == "6-hour":
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 1)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%m-%d\n%Y"))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 30]))
    if data_type == "1-day":
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%m-%d\n%Y"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 1)))
    if data_type == "3-day":
        ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 12)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%m-%d\n%Y"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 6)))
    if data_type == "7-day":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%m-%d\n%Y"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 6)))

    # set legend and title
    tz = "KST" if kst else "UTC"
    fig.legend(
        loc="upper right", bbox_to_anchor=(0.9, 0), ncols=2, fontsize=25
    )
    fig.suptitle(
        f"GOES Proton Flux (5-minute data)\n\n{first_time.strftime('%Y-%m-%d %H:%M')} {tz} $-$ {last_time.strftime('%Y-%m-%d %H:%M')} {tz}\n\nUpdated: {now.strftime('%Y-%m-%d %H:%M')} {tz}",
        fontsize=25,
    )

    plt.tight_layout()
    return fig
