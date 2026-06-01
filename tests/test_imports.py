imports = [
    ("numpy", "np"),
    ("pandas", "pd"),
    ("scipy", None),
    ("laspy", None),
    ("open3d", None),
    ("geopandas", "gpd"),
    ("shapely", None),
    ("rasterio", None),
    ("pyproj", None),
    ("pyvista", None),
    ("matplotlib", None),
    ("plotly", None),
    ("streamlit", None),
    ("sklearn", None),
    ("openpyxl", None),
    ("fastapi", None),
    ("pydantic", None),
    ("rich", None),
    ("typer", None),
]

ok, fail = 0, 0
for mod, alias in imports:
    try:
        __import__(mod)
        ok += 1
    except ImportError:
        print(f"  MISSING: {mod}")
        fail += 1

print(f"{ok}/{ok+fail} libraries OK")
if fail:
    print(f"Install missing libraries: pip install -r requirements.txt")
