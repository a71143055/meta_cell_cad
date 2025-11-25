def manhattan_route(nl, coords):
    paths = []
    for u, v in nl.g.edges:
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        path = []
        x, y = x1, y1
        while x != x2:
            x += 1 if x < x2 else -1
            path.append((x, y))
        while y != y2:
            y += 1 if y < y2 else -1
            path.append((x, y))
        paths.append(path)
    return paths
