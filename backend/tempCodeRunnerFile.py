from __future__ import annotations

import heapq
from collections import defaultdict
import math


# -------------------------------------------------
# NODE METADATA (REAL LOCATIONS)
# -------------------------------------------------

NODE_METADATA = {

    "AMB_BASE": {
        "name": "Kolkata Ambulance Hub",
        "lat": 22.5726,
        "lon": 88.3639,
        "type": "ambulance"
    },

    "FIRE_BASE": {
        "name": "Kolkata Fire Station",
        "lat": 22.5740,
        "lon": 88.3600,
        "type": "fire"
    },

    # INTERSECTIONS

    "Park_Street": {
        "name": "Park Street Crossing",
        "lat": 22.5535,
        "lon": 88.3525,
        "type": "intersection"
    },

    "Esplanade": {
        "name": "Esplanade Junction",
        "lat": 22.5675,
        "lon": 88.3630,
        "type": "intersection"
    },

    "Sealdah": {
        "name": "Sealdah Junction",
        "lat": 22.5655,
        "lon": 88.3725,
        "type": "intersection"
    },

    "Howrah_Bridge": {
        "name": "Howrah Bridge Signal",
        "lat": 22.5850,
        "lon": 88.3468,
        "type": "intersection"
    },

    # HOSPITALS

    "Apollo": {
        "name": "Apollo Gleneagles Hospital",
        "lat": 22.5147,
        "lon": 88.3924,
        "type": "hospital"
    },

    "Fortis": {
        "name": "Fortis Anandapur",
        "lat": 22.5120,
        "lon": 88.4000,
        "type": "hospital"
    },

    "AMRI": {
        "name": "AMRI Salt Lake",
        "lat": 22.5175,
        "lon": 88.3650,
        "type": "hospital"
    },

    "Medica": {
        "name": "Medica Superspeciality",
        "lat": 22.5075,
        "lon": 88.4012,
        "type": "hospital"
    },

    "Ruby": {
        "name": "Ruby General Hospital",
        "lat": 22.5129,
        "lon": 88.4011,
        "type": "hospital"
    },

    "SSKM": {
        "name": "SSKM Hospital",
        "lat": 22.5415,
        "lon": 88.3426,
        "type": "hospital"
    },

    "BelleVue": {
        "name": "Belle Vue Clinic",
        "lat": 22.5342,
        "lon": 88.3498,
        "type": "hospital"
    },

    "Peerless": {
        "name": "Peerless Hospital",
        "lat": 22.4973,
        "lon": 88.4026,
        "type": "hospital"
    },

    "Woodlands": {
        "name": "Woodlands Hospital",
        "lat": 22.5336,
        "lon": 88.3506,
        "type": "hospital"
    },

    "ILS": {
        "name": "ILS Hospital Salt Lake",
        "lat": 22.5721,
        "lon": 88.4142,
        "type": "hospital"
    },
}


CONTROLLED_INTERSECTIONS = {
    "Park_Street",
    "Esplanade",
    "Sealdah",
    "Howrah_Bridge"
}


# -------------------------------------------------
# ROAD GRAPH (SIMPLIFIED CITY NETWORK)
# -------------------------------------------------

ROAD_EDGES = [

    {"from": "AMB_BASE", "to": "Park_Street", "travel_sec": 18},
    {"from": "Park_Street", "to": "AMB_BASE", "travel_sec": 18},

    {"from": "FIRE_BASE", "to": "Esplanade", "travel_sec": 16},
    {"from": "Esplanade", "to": "FIRE_BASE", "travel_sec": 16},

    {"from": "Park_Street", "to": "Esplanade", "travel_sec": 20},
    {"from": "Esplanade", "to": "Park_Street", "travel_sec": 20},

    {"from": "Park_Street", "to": "Sealdah", "travel_sec": 18},
    {"from": "Sealdah", "to": "Park_Street", "travel_sec": 18},

    {"from": "Esplanade", "to": "Howrah_Bridge", "travel_sec": 16},
    {"from": "Howrah_Bridge", "to": "Esplanade", "travel_sec": 16},

    {"from": "Sealdah", "to": "Howrah_Bridge", "travel_sec": 15},
    {"from": "Howrah_Bridge", "to": "Sealdah", "travel_sec": 15},

    # connections to hospitals

    {"from": "Sealdah", "to": "Apollo", "travel_sec": 25},
    {"from": "Sealdah", "to": "AMRI", "travel_sec": 20},

    {"from": "Park_Street", "to": "SSKM", "travel_sec": 12},
    {"from": "Park_Street", "to": "BelleVue", "travel_sec": 10},

    {"from": "Esplanade", "to": "Woodlands", "travel_sec": 14},

    {"from": "Sealdah", "to": "Ruby", "travel_sec": 22},
    {"from": "Sealdah", "to": "Medica", "travel_sec": 24},

    {"from": "Sealdah", "to": "Peerless", "travel_sec": 26},

    {"from": "Howrah_Bridge", "to": "ILS", "travel_sec": 28},

]


# -------------------------------------------------
# ROUTING ENGINE (DIJKSTRA)
# -------------------------------------------------

class EmergencyGridPlanner:

    def __init__(self, edges=None):

        self.edges = edges or ROAD_EDGES

        self._adj = defaultdict(list)

        for e in self.edges:
            self._adj[e["from"]].append(e)

    def shortest_path(self, source, destination):

        dist = {source: 0}
        prev = {}

        pq = [(0, source)]

        while pq:

            cost, node = heapq.heappop(pq)

            if node == destination:
                break

            for edge in self._adj[node]:

                nxt = edge["to"]

                new_cost = cost + edge["travel_sec"]

                if new_cost < dist.get(nxt, 1e9):

                    dist[nxt] = new_cost
                    prev[nxt] = node

                    heapq.heappush(pq, (new_cost, nxt))

        path = [destination]

        while path[-1] != source:

            if path[-1] not in prev:
                raise ValueError("No route found")

            path.append(prev[path[-1]])

        path.reverse()

        return path, dist[destination]