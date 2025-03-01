import astropy.units as u
import numpy as np
import plotly.graph_objects as go
from astropy.time import Time
from sunpy.coordinates import (
    HeliocentricInertial,
    get_body_heliographic_stonyhurst,
    get_horizons_coord,
)


class Plotter:
    def __init__(self, obstime, frame, period, direction):
        self.obstime = obstime
        self.frame = frame
        self.period = period
        assert direction in [
            "forward",
            "backward",
            "both",
        ], "direction must be forward, backward or both"
        self.direction = direction

    def orbit(self, fig, kind, name, color, search_name=None):
        obstime = self.obstime
        hci_frame = self.frame
        period = self.period
        direction = self.direction

        if kind == "planet":
            f = get_body_heliographic_stonyhurst
        elif kind == "mission":
            f = get_horizons_coord

        try:
            if search_name:
                coord = f(search_name, obstime)
            else:
                coord = f(name, obstime)
        except Exception:
            return None, None
        coord = coord.transform_to(hci_frame)
        fig.add_trace(
            go.Scatterpolar(
                r=[coord.distance.to(u.AU).value],
                theta=[coord.lon.to(u.deg).value],
                mode="markers",
                marker=dict(size=10, color=color),
                name=name,
            )
        )

        if direction == "forward":
            times = obstime + np.arange(period) * u.day
        if direction == "backward":
            times = sorted(obstime - np.arange(period) * u.day)
        if direction == "both":
            forward_times = obstime + np.arange(period) * u.day
            backward_times = sorted(obstime - np.arange(period) * u.day)
            times = np.concatenate([backward_times, forward_times])

        if search_name:
            coords = f(search_name, times)
        else:
            coords = f(name, times)
        coords = coords.transform_to(hci_frame)
        fig.add_trace(
            go.Scatterpolar(
                r=coords.distance.to(u.AU).value,
                theta=coords.lon.to(u.deg).value,
                mode="lines",
                line=dict(color=color),
                name=name,
                showlegend=False,
            )
        )
        return coord, coords


def plot_body_position_plotly(
    names, obstime, period, direction, earth_adjust, earth_lon
):
    obstime = Time(obstime)
    hci_frame = HeliocentricInertial(obstime=obstime)
    if direction == "forward":
        title_str = f"Next {period} days"
    if direction == "backward":
        title_str = f"Previous {period} days"
    if direction == "both":
        title_str = f"Previous and Next {period} days"
    plotter = Plotter(
        obstime=obstime, frame=hci_frame, period=period, direction=direction
    )

    fig = go.Figure()
    # ==============================================================================
    fig.add_trace(
        go.Scatterpolar(
            r=[0],
            theta=[0],
            mode="markers",
            marker=dict(size=10, color="yellow"),
            name="Sun",
        )
    )
    # ------------------------------------------------------------
    earth_coord, _ = plotter.orbit(
        fig, kind="planet", name="Earth", color="lime"
    )
    if earth_adjust:
        earth_pos = earth_lon
        fig.update_layout(
            polar=dict(
                angularaxis_rotation=earth_pos
                - earth_coord.lon.to(u.deg).value,
            )
        )
    # ------------------------------------------------------------
    for name in names:
        if name == "Mercury":
            kind, color = "planet", "lavender"
            search_name = None
        if name == "Venus":
            kind, color = "planet", "coral"
            search_name = None
        if name == "Mars":
            kind, color = "planet", "red"
            search_name = None
        if name == "Jupiter":
            kind, color = "planet", "peachpuff"
            search_name = None
        if name == "Saturn":
            kind, color = "planet", "lightsteelblue"
            search_name = None
        if name == "Uranus":
            kind, color = "planet", "skyblue"
            search_name = None
        if name == "Neptune":
            kind, color = "planet", "deepskyblue"
            search_name = None
        if name == "STEREO-A":
            kind, color = "mission", "cyan"
            search_name = None
        if name == "STEREO-B":
            kind, color = "mission", "magenta"
            search_name = None
        if name == "Parker Solar Probe":
            kind, color = "mission", "violet"
            search_name = None
        if name == "Solar Orbiter":
            kind, color = "mission", "blue"
            search_name = None
        if name == "Juno":
            kind, color = "mission", "pink"
            search_name = "Juno (spacecraft)"
        if name == "Voyager 1":
            kind, color = "mission", "gold"
            search_name = None
        if name == "Voyager 2":
            kind, color = "mission", "silver"
            search_name = None
        plotter.orbit(
            fig, kind=kind, name=name, color=color, search_name=search_name
        )

    # ==============================================================================
    fig.update_layout(
        polar=dict(
            bgcolor="black",
            radialaxis=dict(color="white"),
            angularaxis=dict(
                color="white", direction="counterclockwise", tickmode="array"
            ),
        ),
        paper_bgcolor="black",
        font=dict(color="white"),
        title=f"{obstime.strftime('%Y-%m-%d %H:%M UTC')}<br>{title_str}<br>Heliocentric Inertial (HCI) System",
        title_y=0.95,
        title_x=0.5,
        title_xanchor="center",
        title_font=dict(color="white"),
        legend=dict(
            bgcolor="rgba(0, 0, 0, 0.7)",
            bordercolor="white",
            font=dict(color="white"),
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig
