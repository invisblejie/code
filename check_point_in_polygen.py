def check_point_in_polygon( point, polygon):
    """point is the point which format is (x, y)"""
    """polygen is the tuple or list which contains point that form polygon , format is [(x1, y1), (x2, y2)....]"""
    status = False
    len_polygon = len(polygon)
    for i in range(len_polygon):
        j = (i + 1) % len_polygon
        if ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and (
            point[0] < (polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) +
            polygon[i][0]):
            status = not status
    return status

