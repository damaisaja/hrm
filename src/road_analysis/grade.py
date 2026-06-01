import rasterio
import numpy as np
import pandas as pd


def sample_elevation(dtm_path, x, y):
    with rasterio.open(dtm_path) as src:
        if isinstance(x, (list, np.ndarray, pd.Series)):
            xy = np.column_stack([np.asarray(x), np.asarray(y)])
            samples = list(src.sample(xy))
            z = np.array([s[0] for s in samples], dtype=np.float64)
            nodata = src.nodata
            if nodata is not None:
                z = np.where(z == nodata, np.nan, z)
            return z
        else:
            samples = list(src.sample([(x, y)]))
            return float(samples[0][0])


def calc_grade(df, elev_col="z_dtm"):
    dz = np.diff(df[elev_col].values, prepend=np.nan)
    dx = np.diff(df["chainage"].values, prepend=np.nan)
    epsilon = 1e-6
    grade = np.where(dx > epsilon, dz / dx * 100, np.nan)
    df["grade_pct"] = grade
    return df


def calc_crossfall(df):
    crossfall = np.full(len(df), np.nan)
    for i in range(len(df)):
        c = df.iloc[i]
        elev = c.get("z_dtm", np.nan)
        elev_left = c.get("z_dtm_left", np.nan)
        elev_right = c.get("z_dtm_right", np.nan)
        if not np.isnan(elev_left) and not np.isnan(elev_right) and not np.isnan(elev):
            half_width = 7.0
            crossfall[i] = ((elev_left + elev_right) / 2 - elev) / half_width * 100
    df["crossfall_pct"] = crossfall
    return df


def inspect_flags(df):
    flags = []
    for i, row in df.iterrows():
        seg_flags = []
        g = row.get("grade_pct", 0)
        if not np.isnan(g):
            if g > 10:
                seg_flags.append("Grade Berlebih")
            elif g > 8:
                seg_flags.append("Grade Tinggi")
        cf = row.get("crossfall_pct", np.nan)
        if not np.isnan(cf):
            if cf < 2:
                seg_flags.append("Crossfall Datar")
            elif cf > 5:
                seg_flags.append("Crossfall Curam")
        flags.append("; ".join(seg_flags) if seg_flags else "")
    df["flags"] = flags
    return df


def process_road(dtm_path, df_centerline):
    z = sample_elevation(dtm_path, df_centerline["x_dxf"], df_centerline["y_dxf"])
    df = df_centerline.copy()
    df["z_dtm"] = z
    df["dz"] = df["z_dtm"] - df["z_dxf"]
    df = calc_grade(df)
    df = calc_crossfall(df)
    df = inspect_flags(df)
    return df
