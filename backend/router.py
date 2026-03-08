import requests

# OSRM public routing server
OSRM_URL = "http://router.project-osrm.org/route/v1/driving"


def get_road_routes(lat1, lon1, lat2, lon2):
    """
    Returns multiple road routes between two coordinates using OSRM.

    Output format:
    [
        {
            "path": [[lon, lat], [lon, lat], ...],
            "distance": meters,
            "duration": seconds
        },
        ...
    ]
    """

    url = (
        f"{OSRM_URL}/"
        f"{lon1},{lat1};{lon2},{lat2}"
        f"?overview=full&geometries=geojson&alternatives=true"
    )

    try:

        response = requests.get(url, timeout=10)

        # Check server response
        if response.status_code != 200:
            print("OSRM server error:", response.status_code)
            return []

        data = response.json()

        if "routes" not in data:
            print("No routes returned")
            return []

        routes = []

        for route in data["routes"]:

            coords = route["geometry"]["coordinates"]
            distance = route["distance"]
            duration = route["duration"]

            routes.append(
                {
                    "path": coords,
                    "distance": distance,
                    "duration": duration,
                }
            )

        # Sort routes by shortest distance
        routes = sorted(routes, key=lambda x: x["distance"])

        return routes

    except requests.exceptions.RequestException as e:

        print("Routing request failed:", e)
        return []

    except Exception as e:

        print("Routing error:", e)
        return []