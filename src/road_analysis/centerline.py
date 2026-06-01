import ezdxf, math
import numpy as np
import pandas as pd

def load_centerlines(dxf_path):
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    lines = []
    for e in msp:
        if e.dxftype() != "POLYLINE":
            continue
        verts = list(e.vertices)
        pts = []
        for v in verts:
            loc = v.dxf.location
            pts.append((loc.x, loc.y, loc.z))
        lines.append({
            "handle": e.dxf.handle,
            "vertices": np.array(pts, dtype=np.float64),
            "n_vertices": len(pts),
        })
    return lines


def interpolate_chainage(vertices, step=20.0):
    xy = vertices[:, :2]
    z = vertices[:, 2]
    seg_dists = np.sqrt(np.sum(np.diff(xy, axis=0) ** 2, axis=1))
    cum_dist = np.insert(np.cumsum(seg_dists), 0, 0.0)
    total = cum_dist[-1]
    n_interp = max(2, int(total / step))
    chainage = np.linspace(0, total, n_interp)
    xi = np.interp(chainage, cum_dist, xy[:, 0])
    yi = np.interp(chainage, cum_dist, xy[:, 1])
    zi = np.interp(chainage, cum_dist, z)
    return pd.DataFrame({
        "chainage": chainage,
        "x_dxf": xi,
        "y_dxf": yi,
        "z_dxf": zi,
    })


def extract_all(dxf_path, step=20.0):
    lines = load_centerlines(dxf_path)
    segments = []
    for line in lines:
        v = line["vertices"]
        z_vals = v[:, 2]
        has_z = np.any(z_vals != 0)
        if not has_z:
            continue
        df = interpolate_chainage(v, step)
        df["handle"] = line["handle"]
        df["vertex_index"] = line["n_vertices"]
        segments.append(df)
    if segments:
        return pd.concat(segments, ignore_index=True)
    return pd.DataFrame()
