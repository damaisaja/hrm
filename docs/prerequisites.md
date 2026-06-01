# Haulling — Prerequisites Library

## Mine Road Intelligence Platform

Dokumen ini menjelaskan setiap library yang dibutuhkan, perannya dalam platform, dan kaitannya dengan 7 ide yang telah dijelaskan.

---

## 1. Core Data Science

### NumPy
- **Peran**: Fondasi semua komputasi numerik. Matrix operations untuk transformasi point cloud, perhitungan grade, fuel consumption.
- **Digunakan di**: Semua modul
- **Ide**: 1, 2, 3, 4, 5, 6, 7
- **Instalasi**: `pip install numpy`
- **Catatan**: Sudah terinstall otomatis dengan banyak library lain

### Pandas
- **Peran**: Data tabular untuk fleet data, fuel data, segment analysis. Output dashboard berupa DataFrame.
- **Digunakan di**: fuel_optimizer, esg_calculator, dashboard, utils
- **Ide**: 1, 2, 3, 4, 5, 7
- **Instalasi**: `pip install pandas`

### SciPy
- **Peran**: Interpolasi spatial (griddata, RBF) untuk membuat DTM dari point cloud. Optimasi route.
- **Digunakan di**: point_cloud, road_analysis, fuel_optimizer
- **Ide**: 1, 4, 6
- **Instalasi**: `pip install scipy`

---

## 2. Point Cloud Processing

### laspy
- **Peran**: Membaca/menulis LAS/LAZ file dari drone. Ekstraksi XYZ, intensity, classification, return number.
- **Digunakan di**: point_cloud module
- **Ide**: 1, 2, 4, 7
- **Instalasi**: `pip install laspy[laszip]`
- **Catatan**: Gunakan `[laszip]` untuk dukungan LAZ compression. Pure Python — tidak perlu C++ compiler.

### Open3D
- **Peran**: Point cloud processing: filtering (statistical outlier removal, voxel downsampling), normal estimation, segmentation, registration ICP.
- **Digunakan di**: point_cloud, ai_detector
- **Ide**: 1, 2, 4, 6
- **Instalasi**: `pip install open3d`
- **Catatan**: Sudah include visualizer GUI. Optimal untuk pipelining point cloud.

### Pyntcloud (optional)
- **Peran**: Alternatif lighter untuk structural analysis point cloud.
- **Digunakan di**: point_cloud
- **Instalasi**: `pip install pyntcloud`

---

## 3. Geospatial & GIS

### GeoPandas
- **Peran**: Geospatial DataFrame untuk road segments, DXF haul road, grade map. Semua analisis berbasis geography.
- **Digunakan di**: road_analysis, fuel_optimizer, dashboard, esg_calculator
- **Ide**: 1, 2, 3, 4, 5, 7
- **Instalasi**: `pip install geopandas`
- **Catatan**: Sudah include Fiona, pyproj, Shapely sebagai dependencies.

### Shapely
- **Peran**: Geometric operations: buffering road centerline, intersection segment boundaries, measuring distances.
- **Digunakan di**: road_analysis, utils
- **Ide**: 1, 2, 6
- **Instalasi**: `pip install shapely` (auto-installed by GeoPandas)

### Rasterio
- **Peran**: Membaca/menulis DTM/DEM raster. Ekstraksi elevasi untuk perhitungan grade. Visualisasi slope map.
- **Digunakan di**: point_cloud, road_analysis
- **Ide**: 1, 2, 4
- **Instalasi**: `pip install rasterio`
- **Catatan**: Membutuhkan GDAL binary. Jika error, gunakan wheel dari Christoph Gohlke.

### PyProj
- **Peran**: Transformasi koordinat (UTM, Geodetic, Local Grid). Krusial untuk tambang yang pakai local coordinate system.
- **Digunakan di**: point_cloud, utils
- **Ide**: 1, 2, 4, 6
- **Instalasi**: `pip install pyproj` (auto-installed by GeoPandas)

### XArray
- **Peran**: Multi-dimensional raster data untuk time-series DTM (Road Digital Twin).
- **Digunakan di**: road_analysis, esg_calculator
- **Ide**: 4
- **Instalasi**: `pip install xarray`

---

## 4. 3D Visualization

### PyVista
- **Peran**: 3D visualization point cloud, DTM mesh, road alignment, grade heatmap. Lebih mudah daripada raw VTK.
- **Digunakan di**: point_cloud, road_analysis, dashboard
- **Ide**: 1, 2, 4, 6
- **Instalasi**: `pip install pyvista`
- **Catatan**: Wrapper VTK. Bisa export screenshot/HTML untuk laporan.

### Matplotlib
- **Peran**: 2D profile plots (long section), grade charts, fuel saving bar charts.
- **Digunakan di**: fuel_optimizer, dashboard, esg_calculator
- **Ide**: 1, 3, 5
- **Instalasi**: `pip install matplotlib`

### Plotly
- **Peran**: Interactive web charts untuk dashboard Streamlit. Grade map interaktif, fuel trend.
- **Digunakan di**: dashboard
- **Ide**: 1, 3, 4, 7
- **Instalasi**: `pip install plotly`

---

## 5. Dashboard & Web

### Streamlit
- **Peran**: Rapid dashboard untuk manajemen tambang. Input file → langsung lihat grade map, fuel impact.
- **Digunakan di**: dashboard module
- **Ide**: 1, 2, 3, 4, 7
- **Instalasi**: `pip install streamlit`
- **Catatan**: Paling cepat untuk prototyping dashboard. Pakai st.columns, st.dataframe, st.plotly_chart.

### FastAPI
- **Peran**: REST API backend untuk integrasi dengan sistem tambang existing.
- **Digunakan di**: dashboard, utils
- **Ide**: 4, 7
- **Instalasi**: `pip install fastapi uvicorn`

### Pydantic
- **Peran**: Data validation untuk input config, fleet specs, road segment definitions.
- **Digunakan di**: utils, fuel_optimizer, esg_calculator
- **Ide**: 1, 5, 6
- **Instalasi**: `pip install pydantic` (auto-installed by FastAPI)

---

## 6. Machine Learning & AI

### Scikit-Learn
- **Peran**: Klasifikasi road defect, clustering segment berdasarkan kondisi, regression untuk fuel prediction.
- **Digunakan di**: ai_detector, fuel_optimizer
- **Ide**: 2, 6
- **Instalasi**: `pip install scikit-learn`

### PyTorch (optional)
- **Peran**: Deep learning untuk AI Haul Road Inspector — deteksi rutting, crossfall, berm secara otomatis.
- **Digunakan di**: ai_detector
- **Ide**: 2, 7
- **Instalasi**: `pip install torch` (CPU) atau `pip install torch --index-url https://download.pytorch.org/whl/cu118` (CUDA)
- **Catatan**: Opsional. Install hanya jika akan mengembangkan AI detection.

---

## 7. Utilities

### OpenPyXL
- **Peran**: Export laporan ke Excel — grade report, fuel saving report, ESG report.
- **Digunakan di**: esg_calculator, fuel_optimizer, dashboard
- **Ide**: 1, 2, 3
- **Instalasi**: `pip install openpyxl`

### Rich
- **Peran**: Terminal output formatting — progress bar processing point cloud, tabel summary di CLI.
- **Digunakan di**: utils
- **Instalasi**: `pip install rich`

### Typer
- **Peran**: CLI interface — `haulling process --las input.laz --dtm dtm.tif`
- **Digunakan di**: main entry point
- **Ide**: Semua
- **Instalasi**: `pip install typer`

### Python-Dotenv
- **Peran**: Environment configuration untuk path data, fleet database, API keys.
- **Digunakan di**: utils
- **Instalasi**: `pip install python-dotenv`

---

## 8. Mapping Library ke Ide

| Library | Ide 1 | Ide 2 | Ide 3 | Ide 4 | Ide 5 | Ide 6 | Ide 7 |
|---------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| numpy | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| pandas | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| scipy | ✓ | | | ✓ | | ✓ | |
| laspy | ✓ | ✓ | | ✓ | | | ✓ |
| open3d | ✓ | ✓ | | ✓ | | ✓ | |
| geopandas | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| shapely | ✓ | ✓ | | | | ✓ | |
| rasterio | ✓ | ✓ | | ✓ | | | |
| pyproj | ✓ | ✓ | | ✓ | | ✓ | |
| pyvista | ✓ | ✓ | | ✓ | | ✓ | |
| matplotlib | ✓ | | ✓ | | ✓ | | |
| plotly | ✓ | ✓ | ✓ | ✓ | | | ✓ |
| streamlit | ✓ | ✓ | ✓ | ✓ | | | ✓ |
| scikit-learn | | ✓ | | | | ✓ | |
| openpyxl | ✓ | ✓ | ✓ | | | | |

---

## 9. Instalasi Lengkap (Windows)

```powershell
# 1. (Opsional) Buat virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install semua library
pip install -r requirements.txt

# 3. Verifikasi instalasi
python -c "import laspy; import open3d; import geopandas; import rasterio; import pyvista; import streamlit; print('All libraries OK')"
```

### Troubleshooting Windows

**GDAL error**: Jika `rasterio` gagal karena GDAL:
```powershell
pip install rasterio --only-binary=:all:
```

**Open3D error**: Pastikan Visual C++ Redistributable terinstall.

**Streamlit di PowerShell**: Jika ada error encoding:
```powershell
$env:PYTHONUTF8 = "1"
streamlit run app.py
```

---

## 10. Verifikasi Cepat

Jalankan script berikut untuk verifikasi semua library:

```python
# tests/test_imports.py
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
```

---

*Dokumen ini diperbarui: 1 Juni 2026*
