class AdaptiveSignalGrid:

    def __init__(self, intersections):

        self.intersections = intersections

        self.density = {
            i: {"north_south":0.25,"east_west":0.25}
            for i in intersections
        }


    def set_density(self, intersection, lane, value):

        self.density[intersection][lane] = value


    def state(self):

        result={}

        for i in self.intersections:

            result[i]={
                "active_lane":"north_south",
                "remaining_green_sec":10,
                "lane_densities":self.density[i],
                "lane_green_targets":{
                    "north_south":10,
                    "east_west":10
                },
                "lane_waits":{
                    "north_south":0,
                    "east_west":0
                }
            }

        return result


    def step(self, seconds):

        pass