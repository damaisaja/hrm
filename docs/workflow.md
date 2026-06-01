# HAULLING — Alur Kerja (Workflow)

## Mine Road Intelligence Platform

```
                      ┌─────────────────────────────────────────────┐
                      │            DRONE SURVEY (LiDAR)             │
                      │            Penerbangan Berkala              │
                      └─────────────────────┬───────────────────────┘
                                            │
                                            ▼
                      ┌─────────────────────────────────────────────┐
                      │              INPUT DATA                    │
                      │                                             │
                      │   ┌──────────┐       ┌─────────────────┐   │
                      │   │   DTM    │       │ DXF Centerline  │   │
                      │   │  (DEM)   │       │  (haul road)    │   │
                      │   └────┬─────┘       └───────┬─────────┘   │
                      │        │                     │              │
                      │   ┌────▼─────────────────────▼──────────┐   │
                      │   │      FLEET DATA (CSV / DB)          │   │
                      │   │  Model, trips, fuel price, carbon   │   │
                      │   └────────────────────────────────────┘   │
                      └─────────────────────┬───────────────────────┘
                                            │
                                            ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                      ROAD ANALYSIS                         │
          │                                                             │
          │   ┌────────────────────────────────────────────────────┐    │
          │   │  1. Load DXF → Parse centerline polyline           │    │
          │   │  2. Sample elevasi per titik dari DTM              │    │
          │   │  3. Interpolasi elevasi ke chainage (setiap 20m)   │    │
          │   │  4. Grade = Δelevasi / Δjarak × 100%               │    │
          │   │  5. Crossfall (jika ada 3 centerlines)             │    │
          │   │  6. Rule-based threshold inspection:               │    │
          │   │     • Grade berlebih      → grade > 10%            │    │
          │   │     • Crossfall salah     → < 2% atau > 5%         │    │
          │   │     • Rutting             → ΔZ > 5cm antar survey  │    │
          │   │     • Drainase buruk      → genangan lokal di DTM  │    │
          │   │  7. Output: GeoDataFrame segments + grade + flags  │    │
          │   └────────────────────────────────────────────────────┘    │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                     FUEL OPTIMIZER                         │
          │                                                             │
          │   Grade per Segment + Fleet Spec                            │
          │     ├── Tractive force  = (RR×cosθ + sinθ) × GVW × g       │
          │     ├── Power required  = Force × speed                     │
          │     ├── Fuel rate       = Power / (η × E_diesel)           │
          │     ├── Fuel per trip   = rate × distance/speed             │
          │     ├── Fuel per year   = trip × trips_per_year             │
          │     └── Cost            = Fuel × price + CO₂ × carbon_cost │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                   ESG CALCULATOR                           │
          │                                                             │
          │   Fuel Saving (L) ──→ CO₂ Reduction ──→ Carbon Cost        │
          │     • CO₂ = Fuel_L × 2.68 kg/L                             │
          │     • Carbon Credit = CO₂_ton × Rp 336.000                 │
          │     • ESG Report siap presentasi                           │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                  ROAD DIGITAL TWIN                         │
          │                                                             │
          │   Drone Minggu ke-1 ───┐                                   │
          │   Drone Minggu ke-2 ───┤──→ Time-series grade & RR         │
          │   Drone Minggu ke-3 ───┘                                   │
          │     • Historis grade & rolling resistance                   │
          │     • Trend kerusakan jalan                                 │
          │     • Prediksi fuel escalation                              │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                RECOMMENDATION ENGINE                       │
          │                                                             │
          │   Current Grade ──→ Target Grade ──→ Cut/Fill Design       │
          │     • "Cut 2.5m, Fill 1.8m pada CH 1+250"                  │
          │     • "Fuel saving 18%, cycle time turun 7%"               │
          │     • "Prioritas: HIGH — Rp 676 juta/tahun"                │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                      DASHBOARD                             │
          │                                                             │
          │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
          │  │ Grade Map    │  │ Road Defects  │  │ Fuel Saving  │      │
          │  │ Per Segment  │  │ Flagged Segm.│  │ Map          │      │
          │  └──────────────┘  └──────────────┘  └──────────────┘      │
          │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
          │  │ Cost Saving  │  │ ESG Summary  │  │ Digital Twin  │      │
          │  │ Chart        │  │ Card         │  │ Time-series  │      │
          │  └──────────────┘  └──────────────┘  └──────────────┘      │
          │                                                             │
          │  "Road section ini menyebabkan pemborosan                   │
          │   Rp 3,5 miliar/tahun"                                     │
          └─────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
          ┌─────────────────────────────────────────────────────────────┐
          │                      OUTPUT                                │
          │                                                             │
          │  • Streamlit Dashboard (interaktif)                         │
          │  • Excel Report (grade, fuel, ESG, defects)                 │
          │  • 3D Visualisasi (grade heatmap on road)                   │
          │  • CLI Report (terminal summary via Typer)                  │
          │  • REST API (integrasi sistem tambang existing)             │
          └─────────────────────────────────────────────────────────────┘
```

---

## Alur Data Detail

### Fase 1 — Input
```
Drone LiDAR ──→ DTM/DEM (GeoTIFF)
               DXF Centerline (haul road alignment, X-Y)
               CSV/DB (fleet data: model, trips, fuel price, carbon price)
```

### Fase 2 — Road Analysis (`src/road_analysis/`)
```
DTM + DXF Centerline
  │
  ├── 1. Ekstraksi centerline dari DXF (polyline 2D)
  ├── 2. Interpolasi ke chainage tetap (setiap 20m)
  ├── 3. Sampling elevasi Z dari DTM per titik chainage
  ├── 4. Grade = ΔZ / Δjarak × 100%
  ├── 5. Crossfall = sample 3 titik (kiri, center, kanan)
  ├── 6. Rule-based inspection threshold:
  │       grade > 10%         → flag "Grade Berlebih"
  │       crossfall < 2%       → flag "Crossfall Datar"
  │       crossfall > 5%       → flag "Crossfall Curam"
  │       ΔZ antar survey >5cm → flag "Potensi Rutting"
  │       genangan di DTM      → flag "Drainase Buruk"
  └── 7. Output: GeoDataFrame [chainage, X, Y, Z, grade, crossfall, flags]
```

**Catatan**: Point cloud (LAS/LAZ) bersifat opsional — hanya digunakan jika
DTM tidak tersedia, untuk generate DTM via TIN interpolation.

### Fase 3 — Fuel Optimization (`src/fuel_optimizer/`)
```
Grade per Segment + Fleet Spec
  │
  ├── Tractive force = (RR×cosθ + sinθ) × GVW × g
  ├── Power required = Force × speed
  ├── Fuel rate = Power / (η × E_diesel)
  ├── Fuel per trip = rate × distance/speed
  ├── Fuel per year = trip × trips_per_year
  └── Cost = Fuel × price + CO₂ × carbon_price
```

### Fase 4 — Dashboard (`src/dashboard/`)
```
Streamlit App
  │
  ├── Tab 1: Grade Map (grade per segment, heatmap 3D)
  ├── Tab 2: Road Defects (segmen flagged, inspection table)
  ├── Tab 3: Fuel Optimizer (fuel saving, cost chart)
  ├── Tab 4: ESG Summary (CO₂, carbon credit, report)
  └── Tab 5: Digital Twin (time series grade trends)
```

---

## Input → Output Mapping

| Input | Processing | Output | Value |
|-------|-----------|--------|-------|
| DTM + DXF Centerline | Sample elevasi + grade calc | Segmen jalan + grade per 20m | **Grade Map** |
| Segmen grade + threshold | Rule-based inspection | Segment flags (grade, crossfall, dll) | **Road Defects** |
| Grade data + Fleet DB | Fuel formula | Fuel L/trip/segment | **Fuel Impact Map** |
| Fuel + Harga solar | Cost calc | Rp/segment | **Cost Saving Priority** |
| Fuel saving × CO₂ factor | ESG calc | CO₂ ton, Carbon cost | **ESG Report** |
| Multi-week DTM survey | Time series grade comparison | Trend analysis | **Digital Twin** |

---

## Komponen Arsitektur

```
hauling/
│
├── main.py                         # CLI entry point (typer)
│
├── src/
│   ├── road_analysis/
│   │   ├── __init__.py
│   │   ├── centerline.py           # Load & interpolasi centerline DXF
│   │   ├── grade.py                # Grade & crossfall calc dari DTM
│   │   ├── segment.py              # Chainage segmentation
│   │   └── inspector.py            # Rule-based threshold inspection
│   │
│   ├── fuel_optimizer/
│   │   ├── __init__.py
│   │   ├── engine.py               # Formula perhitungan (DONE)
│   │   └── optimizer.py            # Multi-scenario optimizer
│   │
│   ├── esg_calculator/
│   │   ├── __init__.py
│   │   └── calculator.py           # CO₂ + carbon cost
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── app.py                  # Streamlit UI (DONE)
│   │   └── components/             # Reusable dashboard widgets
│   │
│   ├── point_cloud/                # Opsional — hanya jika DTM tidak ada
│   │   ├── __init__.py
│   │   └── dtm_generator.py        # LAS/LAZ → DTM (TIN interp)
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Constants, settings (DONE)
│       └── fleet_db.py             # Fleet database (DONE)
│
└── tests/
    ├── test_imports.py
    ├── test_fuel_engine.py
    └── test_fleet_10_40t.py
```

---

## Contoh Skenario End-to-End

### Input
```
DTM:        dtm_tambang_maret_2026.tif
DXF:        haul_road_2024.dxf (centerline polyline)
Fleet:      HD785_7, VOLVO_A40G
Trips:      5.000 trip/tahun
Solar:      Rp 12.000/liter
Carbon:     Rp 336.000/ton CO₂
```

### Proses
```
1. Load DTM (GeoTIFF) + DXF centerline
2. Interpolasi centerline ke chainage 20m
3. Sample Z dari DTM di setiap titik → grade per segment
4. Rule-based inspection:
     CH 1+250 – 1+340 → grade 14.2% → flag "Grade Berlebih"
     CH 0+800 – 0+860 → crossfall 1.2% → flag "Crossfall Datar"
5. Hitung fuel impact vs standar 8%
6. Fuel saving per model:
     HD785_7:   52.400 L/thn → Rp 676 juta/thn → 140 ton CO₂
     VOLVO_A40G: 18.420 L/thn → Rp 238 juta/thn →  49 ton CO₂
7. Tampilkan di dashboard + export Excel
```

### Output ke Manajemen
```
"Ramp Pit Selatan CH 1+250 sampai CH 1+340:
 • Grade saat ini: 14.2% (target: 8%)
 • Status: ⚠ Grade Berlebih (threshold >10%)
 • Segmen kritis: 90 meter dari total 2,5 km
 • Potensi fuel saving: Rp 676 juta/tahun (HD785-7)
 • CO₂ reduction: 140 ton/tahun
 • Prioritas: HIGH — perbaiki segera"
```

---

## Perubahan Arsitektur dari Versi Sebelumnya

| Sebelum | Sesudah | Alasan |
|---------|---------|--------|
| Input: LAS + DTM + DXF | Input: DTM + DXF Centerline | LAS hanya fallback untuk generate DTM |
| Point cloud processing sbg modul utama | Point cloud sbg modul opsional | Grade cukup dari DTM + centerline |
| Clip point cloud pakai buffer DXF | Langsung sample elevasi dari DTM | Tidak perlu clip, lebih ringan |
| AI Inspector (ML-based) | Inspector rule-based threshold | Semua deteksi cukup pakai if-else |
| Modul: ai_detector/ | Modul: road_analysis/inspector.py | Inspeksi jadi bagian road analysis |
| ML: scikit-learn | -- | Tidak perlu ML library |

---

## Teknologi Stack

| Layer | Teknologi |
|-------|-----------|
| Raster/GIS | rasterio, geopandas, shapely, pyproj |
| Centerline | ezdxf (parse DXF polyline) |
| 3D Viz | pyvista, matplotlib, plotly |
| Dashboard | streamlit |
| API | fastapi |
| CLI | typer |
| Config | pydantic |
| Point Cloud (opsional) | laspy, open3d |
