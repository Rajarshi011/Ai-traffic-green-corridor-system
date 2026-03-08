from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np
import pydeck as pdk
import streamlit as st

from backend.emergency_grid import (
    NODE_METADATA,
    CONTROLLED_INTERSECTIONS,
)

from backend.router import get_road_routes
from backend.signal_controller import AdaptiveSignalGrid
from backend.traffic_ai import analyze_frame, read_video_frame


PROJECT_ROOT = Path(__file__).resolve().parent
VIDEO_PATH = PROJECT_ROOT / "traffic.mp4"

INTERSECTIONS = {i: ["north_south", "east_west"] for i in CONTROLLED_INTERSECTIONS}


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

def init_state():

    if "grid" not in st.session_state:
        st.session_state.grid = AdaptiveSignalGrid(INTERSECTIONS)

    if "sim_time" not in st.session_state:
        st.session_state.sim_time = 0

    if "analysis" not in st.session_state:
        st.session_state.analysis = None

    if "route_coords" not in st.session_state:
        st.session_state.route_coords = None

    if "routes" not in st.session_state:
        st.session_state.routes = []

    if "route_index" not in st.session_state:
        st.session_state.route_index = 0

    if "eta" not in st.session_state:
        st.session_state.eta = None

    if "frame_index" not in st.session_state:
        st.session_state.frame_index = 0

    for i in INTERSECTIONS:
        for lane in INTERSECTIONS[i]:
            key = f"density_{i}_{lane}"
            if key not in st.session_state:
                st.session_state[key] = 0.25


# -------------------------------------------------
# DENSITY CONTROL
# -------------------------------------------------

def get_key(i, lane):
    return f"density_{i}_{lane}"


def sync_densities():

    grid = st.session_state.grid

    for i in INTERSECTIONS:
        for lane in INTERSECTIONS[i]:

            grid.set_density(
                i,
                lane,
                st.session_state[get_key(i, lane)]
            )


# -------------------------------------------------
# TRAFFIC VISION
# -------------------------------------------------

def run_detection(conf):

    frame, _, _ = read_video_frame(
        str(VIDEO_PATH),
        st.session_state.frame_index
    )

    if frame is None:
        return None

    result = analyze_frame(frame, conf)

    return result


# -------------------------------------------------
# SIMULATION STEP
# -------------------------------------------------

def step_sim(seconds):

    sync_densities()

    st.session_state.grid.step(seconds)

    st.session_state.sim_time += seconds


# -------------------------------------------------
# SIGNAL TABLE
# -------------------------------------------------

def build_rows():

    snapshot = st.session_state.grid.state()

    rows = []

    for i in snapshot:

        state = snapshot[i]

        rows.append(
            {
                "Intersection": i,
                "Active Lane": state["active_lane"],
                "Green Remaining": state["remaining_green_sec"],
                "NS Density": state["lane_densities"]["north_south"],
                "EW Density": state["lane_densities"]["east_west"],
                "NS Target": state["lane_green_targets"]["north_south"],
                "EW Target": state["lane_green_targets"]["east_west"],
                "NS Wait": state["lane_waits"]["north_south"],
                "EW Wait": state["lane_waits"]["east_west"],
            }
        )

    return rows


# -------------------------------------------------
# MAP
# -------------------------------------------------

def build_map():

    route = st.session_state.route_coords

    node_data = []

    for node, meta in NODE_METADATA.items():

        color = [66, 135, 245]

        if meta["type"] == "hospital":
            color = [225, 74, 74]

        if meta["type"] == "ambulance":
            color = [245, 158, 11]

        if meta["type"] == "fire":
            color = [249, 115, 22]

        node_data.append(
            {
                "name": meta["name"],
                "lat": float(meta["lat"]),
                "lon": float(meta["lon"]),
                "color": color,
            }
        )

    layers = []

    if route:

        layers.append(
            pdk.Layer(
                "PathLayer",
                data=[{"path": route}],
                get_path="path",
                get_color=[0, 255, 0],
                get_width=6,
            )
        )

    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=node_data,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius=120,
        )
    )

    layers.append(
        pdk.Layer(
            "TextLayer",
            data=node_data,
            get_position="[lon, lat]",
            get_text="name",
            get_size=14,
            get_color=[240, 240, 240],
        )
    )

    lat_center = sum(float(n["lat"]) for n in NODE_METADATA.values()) / len(NODE_METADATA)
    lon_center = sum(float(n["lon"]) for n in NODE_METADATA.values()) / len(NODE_METADATA)

    return pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=lat_center,
            longitude=lon_center,
            zoom=13.5,
            pitch=35,
        ),
    )


# -------------------------------------------------
# APP
# -------------------------------------------------

st.set_page_config(layout="wide")

init_state()

st.title("Dynamic AI Traffic Flow Optimizer & Emergency Grid")


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("Control Panel")

signal_mode = st.sidebar.radio(
    "Signal Control Mode",
    ["Adaptive AI", "Manual Control"]
)

confidence = st.sidebar.slider("YOLO Confidence", 0.1, 0.9, 0.35)


# -------------------------------------------------
# MANUAL SIGNAL CONTROL
# -------------------------------------------------

if signal_mode == "Manual Control":

    st.sidebar.subheader("Manual Signal Control")

    for intersection in INTERSECTIONS:

        st.sidebar.markdown(f"**{intersection}**")

        ns = st.sidebar.slider(
            f"{intersection} NS Green",
            5, 90, 30
        )

        ew = st.sidebar.slider(
            f"{intersection} EW Green",
            5, 90, 30
        )

        st.session_state.grid.lane_targets[intersection]["north_south"] = ns
        st.session_state.grid.lane_targets[intersection]["east_west"] = ew


# -------------------------------------------------
# TRAFFIC DENSITY
# -------------------------------------------------

target_intersection = st.sidebar.selectbox(
    "Apply Density To Intersection",
    list(INTERSECTIONS.keys())
)

target_lane = st.sidebar.radio(
    "Lane",
    INTERSECTIONS[target_intersection]
)

if st.sidebar.button("Run Vision Analysis"):

    analysis = run_detection(confidence)

    if analysis:

        st.session_state.analysis = analysis

        density = analysis["density_score"]

        st.session_state[get_key(target_intersection, target_lane)] = density


tick = st.sidebar.slider("Simulation Tick", 1, 20, 5)

if st.sidebar.button("Advance Signal Network"):
    step_sim(tick)


# -------------------------------------------------
# LAYOUT
# -------------------------------------------------

left, right = st.columns([1.1, 1])


# -------------------------------------------------
# LEFT PANEL
# -------------------------------------------------

with left:

    st.subheader("Traffic Vision")

    if st.session_state.analysis:

        a = st.session_state.analysis

        c1, c2, c3 = st.columns(3)

        c1.metric("Vehicles", a["vehicle_count"])
        c2.metric("Density", a["density_label"])
        c3.metric("Score", f"{a['density_score']:.2f}")

        st.image(a["annotated_frame"], channels="BGR")

    st.subheader("Adaptive Signal Grid")

    sync_densities()

    st.dataframe(build_rows(), width="stretch")


# -------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------

with right:

    st.subheader("Emergency Dispatch")

    vehicle = st.selectbox("Vehicle Type", ["ambulance", "fire_service"])

    source = st.selectbox("Source", ["AMB_BASE", "FIRE_BASE"])

    dest = st.selectbox(
        "Destination",
        [n for n in NODE_METADATA if NODE_METADATA[n]["type"] == "hospital"],
    )

    if st.button("Activate Green Corridor"):

        src = NODE_METADATA[source]
        dst = NODE_METADATA[dest]

        routes = get_road_routes(
            src["lat"], src["lon"],
            dst["lat"], dst["lon"]
        )

        if routes:

            st.session_state.routes = routes
            st.session_state.route_index = 0

            best = routes[0]

            st.session_state.route_coords = best["path"]
            st.session_state.eta = best["duration"]

            st.success(f"Route activated | ETA {int(best['duration'])} seconds")

        else:

            st.error("No route found")

    if st.button("Reroute Ambulance"):

        routes = st.session_state.routes

        if routes:

            st.session_state.route_index += 1

            if st.session_state.route_index >= len(routes):
                st.session_state.route_index = 0

            new_route = routes[st.session_state.route_index]

            st.session_state.route_coords = new_route["path"]
            st.session_state.eta = new_route["duration"]

            st.success(f"Switched route | ETA {int(new_route['duration'])} seconds")

        else:

            st.warning("Activate Green Corridor first.")


    st.subheader("Green Corridor Map")

    st.pydeck_chart(build_map())