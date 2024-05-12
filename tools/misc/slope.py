slope_window_before = 15 # meters behind
slope_window_ahead = 5 # meters ahead

slope_cap_window_before = slope_window_before*4
slope_cap_window_ahead = slope_window_ahead*4


def calculate_slope(data):
    data_by_dist = _precalculate_data_by_distance(data)

    print("Calculating slope")

    for ts in data:
        dst = data[ts]['distance']

        slope = _slope_between(dst - slope_window_before, dst + slope_window_ahead, data_by_dist)

        #capping runaway slope to bigger window
        cap = _slope_between(dst - slope_cap_window_before, dst + slope_cap_window_ahead, data_by_dist)
        if slope*cap > 0:
            if abs(slope) > abs(cap):
                slope = cap 

        data[ts]['slope'] = slope*100 #converted to pct

    return data


def _precalculate_data_by_distance(data):
    print("Precalculating data by distance")
    data_by_dist = {}

    for ts in data:
        dst = data[ts]['distance']

        if dst not in data_by_dist:
            data_by_dist[dst] = []

        data_by_dist[dst].append(data[ts])
    
    return data_by_dist


def _get_by_distance(dist, data_by_dist, first=True):
    if dist in data_by_dist:
        return data_by_dist[dist][0 if first else -1]

    prev = None
    next = None

    for d,points in data_by_dist.items():
        if prev is None: #a
            prev = points[-1]
            next = points[0]

        if d < dist: #b
            prev = points[-1]
            next = points[0]

        if d > dist: #c
            next = points[0]
            break

    if prev['distance'] == next['distance']:
        if dist < prev['distance']:
            return prev
        return next

    ratio = (dist - prev['distance']) / (next['distance'] - prev['distance'])

    virt = {}
    for k in prev:
        if k in next:
            virt[k] = prev[k] + ratio * (next[k] - prev[k])
    
    return virt

def _slope_between(dst_a, dst_b, data_by_dist):
    point_a = _get_by_distance(dst_a, data_by_dist, False)
    point_b = _get_by_distance(dst_b, data_by_dist)

    if 'altitude' in point_a and 'distance' in point_a and 'altitude' in point_b and 'distance' in point_b:
        if point_b['distance'] - point_a['distance'] > 0: #check if distance is above 0 to be safe
            return (point_b['altitude'] - point_a['altitude'])/((point_b['distance'] - point_a['distance']))

    return None
