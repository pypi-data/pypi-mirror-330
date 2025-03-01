from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sunpy.time import parse_time


def goes_xray_flux(
    data_type,
    primary=True,
    kst=False,
    flare_config={"show": True, "X": True, "M": True, "C": False},
):
    sat_class = "primary" if primary else "secondary"
    assert data_type in [
        "6-hour",
        "1-day",
        "3-day",
        "7-day",
    ], "data_type must be one of ['6-hour', '1-day', '3-day', '7-day']"

    plt.rcParams.update({"font.size": 20})

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
        f"https://services.swpc.noaa.gov/json/goes/{sat_class}/xrays-{data_type}.json"
    )
    goes_xrsa = goes_json_data[goes_json_data["energy"] == "0.05-0.4nm"]
    goes_xrsb = goes_json_data[goes_json_data["energy"] == "0.1-0.8nm"]

    # get satellite number
    satellite = str(goes_json_data["satellite"].unique()[0])

    # get time range
    time_array = parse_time(goes_xrsa["time_tag"]).datetime + td
    first_time = time_array[0]
    last_time = time_array[-1]

    # create figure and plot
    fig, ax = plt.subplots(figsize=(15, 10))

    # plot GOES X-ray flux
    ax.plot(
        parse_time(goes_xrsb["time_tag"]).datetime + td,
        goes_xrsb["flux"].values,
        label=f"GOES-{satellite} " + r"0.5$-$4.0 $\mathrm{\AA}$",
        color="red",
    )
    ax.plot(
        parse_time(goes_xrsa["time_tag"]).datetime + td,
        goes_xrsa["flux"].values,
        label=f"GOES-{satellite} " + r"1.0$-$8.0 $\mathrm{\AA}$",
        color="blue",
    )

    # set y-axis scale and limit
    ax.set_yscale("log")
    ax.set_ylim(1e-9, 1e-2)
    ax.set_ylabel(r"W $\cdot$ m$^{-2}$", fontsize=25)
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
    labels = ["A", "B", "C", "M", "X"]
    centers = np.logspace(-7.6, -3.6, len(labels))
    for value, label in zip(centers, labels):
        ax.text(
            1.02,
            value,
            label,
            transform=ax.get_yaxis_transform(),
            horizontalalignment="center",
            fontsize=25,
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
        loc="upper right", bbox_to_anchor=(0.85, 0), ncols=2, fontsize=25
    )

    fig.suptitle(
        f"GOES X-ray Flux (1-minute data)\n\n{first_time.strftime('%Y-%m-%d %H:%M')} {tz} $-$ {last_time.strftime('%Y-%m-%d %H:%M')} {tz}\n\nUpdated: {now.strftime('%Y-%m-%d %H:%M')} {tz}",
        fontsize=25,
    )

    flare = flare_config["show"]
    if flare:
        # plot flare events
        goes_xray_flare_week = pd.read_json(
            f"https://services.swpc.noaa.gov/json/goes/{sat_class}/xray-flares-7-day.json"
        )
        goes_xray_flare_week["max_time_datetime"] = parse_time(
            goes_xray_flare_week["max_time"]
        ).datetime
        goes_xray_flare_week = goes_xray_flare_week[
            goes_xray_flare_week["max_time_datetime"] >= first_time
        ]
        for i, s in goes_xray_flare_week.iterrows():
            max_time = parse_time(s["max_time"]).datetime + td
            begin_time = parse_time(s["begin_time"]).datetime + td
            end_time = parse_time(s["end_time"]).datetime + td

            max_class = s["max_class"]

            # No flare class selected
            if (
                not flare_config["X"]
                and not flare_config["M"]
                and not flare_config["C"]
            ):
                continue

            # Only X-class selected
            if (
                flare_config["X"]
                and not flare_config["M"]
                and not flare_config["C"]
            ):
                if max_class.startswith("X"):
                    pass
                else:
                    continue

            # Only M-class selected
            if (
                not flare_config["X"]
                and flare_config["M"]
                and not flare_config["C"]
            ):
                if max_class.startswith("M"):
                    pass
                else:
                    continue

            # Only C-class selected
            if (
                not flare_config["X"]
                and not flare_config["M"]
                and flare_config["C"]
            ):
                if max_class.startswith("C"):
                    pass
                else:
                    continue

            # X-class and M-class selected
            if (
                flare_config["X"]
                and flare_config["M"]
                and not flare_config["C"]
            ):
                if max_class.startswith("X") or max_class.startswith("M"):
                    pass
                else:
                    continue

            # X-class and C-class selected
            if (
                flare_config["X"]
                and not flare_config["M"]
                and flare_config["C"]
            ):
                if max_class.startswith("X") or max_class.startswith("C"):
                    pass
                else:
                    continue

            # M-class and C-class selected
            if (
                not flare_config["X"]
                and flare_config["M"]
                and flare_config["C"]
            ):
                if max_class.startswith("M") or max_class.startswith("C"):
                    pass
                else:
                    continue

            # X-class, M-class, and C-class selected
            if flare_config["X"] and flare_config["M"] and flare_config["C"]:
                if (
                    max_class.startswith("X")
                    or max_class.startswith("M")
                    or max_class.startswith("C")
                ):
                    pass
                else:
                    continue

            ax.axvline(
                max_time, color="green", linestyle="-", linewidth=1, ymax=0.855
            )
            ax.axvspan(
                begin_time, end_time, color="green", alpha=0.2, ymax=0.855
            )
            if data_type == "6-hour":
                class_text = f"{max_class}\n{max_time.strftime('%H:%M')}"
                ax.text(
                    max_time,
                    1.3e-3,
                    class_text,
                    color="green",
                    rotation=0,
                    verticalalignment="bottom",
                    horizontalalignment="center",
                )
            if data_type == "1-day":
                class_text = f"{max_class}\n{max_time.strftime('%H:%M')}"
                ax.text(
                    max_time,
                    1.3e-3,
                    class_text,
                    color="green",
                    rotation=0,
                    verticalalignment="bottom",
                    horizontalalignment="center",
                )
            if data_type == "3-day":
                class_text = f"{max_class}\n{max_time.strftime('%H:%M')}"
                ax.text(
                    max_time,
                    1.3e-3,
                    class_text,
                    color="green",
                    rotation=0,
                    verticalalignment="bottom",
                    horizontalalignment="center",
                )
            if data_type == "7-day":
                class_text = f"{max_class}\n{max_time.strftime('%H:%M')}"
                ax.text(
                    max_time,
                    1.22e-3,
                    class_text,
                    color="green",
                    rotation=0,
                    verticalalignment="bottom",
                    horizontalalignment="center",
                )

    plt.tight_layout()
    return fig
