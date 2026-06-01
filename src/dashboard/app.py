import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os, pyproj

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.road_analysis.centerline import extract_all
from src.road_analysis.grade import process_road
from src.fuel_optimizer.engine import calc_fuel_per_trip, calc_round_trip
from src.utils.fleet_db import get_truck
from src.esg_calculator.calculator import esg_report

temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "temp_uploads"))
os.makedirs(temp_dir, exist_ok=True)

def save_uploaded_file(uploaded_file, name):
    if uploaded_file is None:
        return None
    path = os.path.join(temp_dir, name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def download_file_from_url(url, name):
    if not url:
        return None
    import urllib.request
    import re
    
    # Clean/Resolve Google Drive links
    if "drive.google.com" in url:
        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
        if match:
            file_id = match.group(1)
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
    # Clean/Resolve Dropbox links
    elif "dropbox.com" in url:
        url = url.replace("?dl=0", "?dl=1").replace("&dl=0", "&dl=1")
        if "?dl=" not in url and "&dl=" not in url:
            url += "?dl=1"
            
    path = os.path.join(temp_dir, name)
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
        out_file.write(response.read())
    return path

st.set_page_config(page_title="Haulling", layout="wide")

@st.cache_data(show_spinner=False)
def load_and_process_data(dxf_path, dtm_path, step):
    seg = extract_all(dxf_path, step=step)
    out = []
    for h in seg["handle"].unique():
        d = seg[seg["handle"] == h].copy()
        out.append(process_road(dtm_path, d))
    df = pd.concat(out, ignore_index=True)
    return df

utm_crs = pyproj.CRS("EPSG:32750")
wgs84 = pyproj.CRS("EPSG:4326")
to_latlon = pyproj.Transformer.from_crs(utm_crs, wgs84, always_xy=True)

if "processed" not in st.session_state:
    st.session_state.processed = False
    st.session_state.df = None
    st.session_state.handles_clean = []
    st.session_state.fuel_price = 12900
    st.session_state.selected_ch = None

# Custom CSS for premium styling, sticky header, and fixed map column
st.markdown(
    """
    <style>
    /* Full screen container padding adjustments */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Native header overlay for title */
    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(0,0,0,0.06) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.01) !important;
        z-index: 99999 !important;
    }
    
    header[data-testid="stHeader"]::before {
        content: "HAULLING — Mine Road Intelligence Platform";
        font-weight: 800;
        font-size: 1.25rem;
        color: #1d3557;
        display: flex;
        align-items: center;
        padding-left: 2rem;
        height: 100%;
        position: absolute;
        left: 0;
        top: 0;
    }
    
    @media (prefers-color-scheme: dark) {
        header[data-testid="stHeader"] {
            background: rgba(15, 23, 42, 0.85) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        header[data-testid="stHeader"]::before {
            color: #f1faee;
        }
    }
    
    @media (max-width: 992px) {
        header[data-testid="stHeader"]::before {
            content: "HAULLING";
            font-size: 1.15rem;
        }
    }
    
    @media (min-width: 992px) {
        /* Left container: scrollable */
        div[class*="st-key-hasil_container"] {
            width: 48% !important;
            max-width: 48% !important;
            float: left !important;
            margin-top: 4.5rem !important;
        }
        
        /* Right container: completely fixed on the right 50% of the screen */
        div[class*="st-key-map_container"] {
            position: fixed !important;
            right: 0 !important;
            top: 0 !important;
            width: 50% !important;
            height: 100vh !important;
            z-index: 100;
            background-color: var(--background-color, #ffffff);
            border-left: 1px solid rgba(0,0,0,0.1);
            overflow: hidden !important;
            padding: 0 !important;
            margin: 0 !important;
        }
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Clean, premium card containers for metric items */
    div[data-testid="stMetric"] {
        background-color: var(--background-color, #ffffff);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 8px;
        padding: 10px 14px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
        margin-bottom: 12px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.15rem !important;
        font-weight: 700;
        color: #1d3557;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"] {
            border: 1px solid rgba(255,255,255,0.06);
            background-color: rgba(255,255,255,0.02);
        }
        [data-testid="stMetricValue"] {
            color: #f1faee;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ── TWO-COLUMN CORE LAYOUT ──
col_hasil = st.container(key="hasil_container")
col_map = st.container(key="map_container")

with col_hasil:
    truck_options = {
        "HD785_7": "Komatsu HD785-7 (92 ton)",
        "CAT_773G": "Caterpillar 773G (56 ton)",
        "VOLVO_A40G": "Volvo A40G (39 ton)",
        "HD465_7": "Komatsu HD465-7 (55 ton)",
        "HM400_5": "Komatsu HM400-5 (40 ton)",
        "CAT_740": "Caterpillar 740 (40 ton)",
        "HD325_8": "Komatsu HD325-8 (37 ton)",
        "HD405_8": "Komatsu HD405-8 (40 ton)",
        "CAT_773D": "Caterpillar 773D (44 ton)",
        "CAT_725": "Caterpillar 725 (24 ton)",
        "CAT_730": "Caterpillar 730 (28 ton)",
        "CAT_735": "Caterpillar 735 (32 ton)",
        "VOLVO_A25G": "Volvo A25G (25 ton)",
        "VOLVO_A30G": "Volvo A30G (28 ton)",
        "VOLVO_A35G": "Volvo A35G (34 ton)",
        "HM300_5": "Komatsu HM300-5 (28 ton)",
        "DA30_5": "Doosan DA30-5 (28 ton)",
        "BELL_B40E": "Bell B40E (37 ton)",
        "A40E": "Volvo A40E (39 ton)",
        "CAT_773E": "Caterpillar 773E (50 ton)",
        "P460": "Scania P460 (35 ton)",
        "EH3500": "Hitachi EH3500 (181 ton)",
        "T282B": "Liebherr T282B (363 ton)",
    }

    with st.expander("Input Parameter & Konfigurasi Fleet", expanded=not st.session_state.processed):
        col_files1, col_files2 = st.columns(2, gap="medium")
        with col_files1:
            st.markdown("**DTM (TIF) Input**")
            dtm_source = st.radio("Source DTM", ["File Upload", "Cloud URL Link"], horizontal=True, key="dtm_src")
            if dtm_source == "File Upload":
                dtm_file = st.file_uploader("Upload DTM (TIF)", type=["tif", "tiff"])
                dtm_url = None
            else:
                dtm_url = st.text_input("DTM Cloud Download Link (Google Drive / Dropbox / S3)", placeholder="https://drive.google.com/file/d/...")
                dtm_file = None
                
        with col_files2:
            st.markdown("**DXF Centerline Input**")
            dxf_source = st.radio("Source DXF", ["File Upload", "Cloud URL Link"], horizontal=True, key="dxf_src")
            if dxf_source == "File Upload":
                dxf_file = st.file_uploader("Upload DXF Centerline (DXF)", type=["dxf"])
                dxf_url = None
            else:
                dxf_url = st.text_input("DXF Cloud Download Link (Google Drive / Dropbox)", placeholder="https://drive.google.com/file/d/...")
                dxf_file = None
            
        col_params1, col_params2, col_params3, col_params4 = st.columns([1.2, 1.0, 1.0, 1.0], gap="medium")
        with col_params1:
            fleet_key = st.selectbox("Fleet Model", list(truck_options.keys()),
                                     format_func=lambda k: truck_options[k])
        with col_params2:
            fuel_price = st.number_input("Harga Solar (Rp/L)", 5000, 30000, 12900, 500)
            st.session_state.fuel_price = fuel_price
        with col_params3:
            trips_yr = st.number_input("Trips/Year", 1000, 50000, 6000, 1000)
        with col_params4:
            step = st.slider("Chainage Interval (m)", 10, 100, 20)
            
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        col_btns1, col_btns2 = st.columns(2, gap="medium")
        with col_btns1:
            process_clicked = st.button("Process Data", type="primary", use_container_width=True)
        with col_btns2:
            clear_clicked = st.button("Clear Cache", use_container_width=True)

        t = get_truck(fleet_key)
        st.caption(f"Fleet: {t.manufacturer} {t.model} | {t.engine_power_hp:.0f} HP | Payload: {t.payload_tonnes:.1f}t | Speed: {t.top_speed_kmh}km/h | {t.fuel_consumption_L_per_hr_min}–{t.fuel_consumption_L_per_hr_max} L/h")

        if process_clicked:
            with st.spinner("Processing DXF & DTM..."):
                try:
                    # Handle DTM Path
                    if dtm_file is not None:
                        dtm_path = save_uploaded_file(dtm_file, "dtm.tif")
                    elif dtm_url:
                        dtm_path = download_file_from_url(dtm_url, "dtm.tif")
                    else:
                        dtm_path = "data/HR.tif"
                    
                    # Handle DXF Path
                    if dxf_file is not None:
                        dxf_path = save_uploaded_file(dxf_file, "centerline.dxf")
                    elif dxf_url:
                        dxf_path = download_file_from_url(dxf_url, "centerline.dxf")
                    else:
                        dxf_path = "data/HR_lin.dxf"
                        
                    df = load_and_process_data(dxf_path, dtm_path, step)
                    st.session_state.df = df
                    st.session_state.handles_clean = sorted(df.groupby("handle")["grade_pct"].apply(lambda x: x.notna().sum())[df.groupby("handle")["grade_pct"].apply(lambda x: x.notna().sum()) > 0].index.tolist())
                    st.session_state.processed = True
                    st.session_state.selected_ch = None
                    st.success("Successfully processed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")

        if clear_clicked:
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()

    if not st.session_state.processed:
        st.info("Silakan masukkan input di atas dan klik **Process Data** untuk memulai analisis.")
    else:
        df = st.session_state.df
        fp = st.session_state.fuel_price

        def color_for_grade(g):
            if np.isnan(g): return "gray"
            if g > 10: return "red"
            if g > 8: return "orange"
            return "green"

        # Select road
        opts = [f"{h} — {df[df['handle']==h]['chainage'].max():,.0f}m" for h in st.session_state.handles_clean]
        sel = st.selectbox("Pilih Haul Road", opts)
        sel_handle = sel.split(" — ")[0]

        sub_df = df[df["handle"] == sel_handle]
        valid = sub_df.dropna(subset=["grade_pct"])

        # Table click sync
        flagged = valid[valid["grade_pct"] > 8].sort_values("chainage")
        if "df_flagged" in st.session_state and st.session_state.df_flagged.get("selection", {}).get("rows"):
            idx = st.session_state.df_flagged["selection"]["rows"][0]
            if idx < len(flagged):
                st.session_state.selected_ch = int(flagged.iloc[idx]["chainage"])
        elif "df_esg" in st.session_state and st.session_state.df_esg.get("selection", {}).get("rows"):
            idx = st.session_state.df_esg["selection"]["rows"][0]
            if idx < len(flagged):
                st.session_state.selected_ch = int(flagged.iloc[idx]["chainage"])

        # ── Metrics Rows (Perfect Grid Alignment with 3 Rows of 4 Columns) ──
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        r1_1.metric("Panjang", f"{valid['chainage'].max():,.0f} m")
        r1_2.metric("Elevasi", f"{valid['z_dtm'].min():.0f} – {valid['z_dtm'].max():.0f} m")
        r1_3.metric("Grade Max", f"{valid['grade_pct'].max():.1f}%")
        r1_4.metric("Grade >10%", f"{(valid['grade_pct'] > 10).sum()} segmen")

        # Calculate ESG Report
        r = esg_report(valid, fleet_key=fleet_key, trips_per_year=trips_yr, diesel_price=fuel_price)
        pct_waste = (r["fuel_waste_per_trip_L"] / r["fuel_per_trip_L"]) * 100 if r["fuel_per_trip_L"] > 0 else 0
        
        r2_1, r2_2, r2_3, r2_4 = st.columns(4)
        r2_1.metric("Fleet", fleet_key)
        r2_2.metric("Trips/Year", f"{trips_yr:,}")
        r2_3.metric("Fuel Waste/Trip (pp)", f"{r['fuel_waste_per_trip_L']:.2f} L")
        r2_4.metric("Fuel Waste/Year", f"{r['fuel_waste_per_year_L']:,.0f} L ({pct_waste:.1f}%)")
        
        r3_1, r3_2, r3_3, r3_4 = st.columns(4)
        r3_1.metric("Fuel Cost Waste", f"Rp {r['fuel_cost_waste_Rp_per_year']:,.0f}/yr")
        r3_2.metric("CO₂ Reduction", f"{r['co2_reduction_ton_per_year']:,.0f} ton/yr")
        r3_3.metric("Carbon Credit", f"Rp {r['carbon_credit_value_Rp_per_year']:,.0f}/yr")
        r3_4.metric("Total Potential", f"Rp {r['total_saving_Rp_per_year']:,.0f}/yr")

        st.divider()

        # ── Grade bar chart ──
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=valid["chainage"], y=valid["grade_pct"],
            marker_color=[color_for_grade(g) for g in valid["grade_pct"]],
            width=step * 0.8, name="Grade %"))
        fig2.add_hline(y=10, line_dash="dash", line_color="red")
        fig2.add_hline(y=8, line_dash="dash", line_color="orange")
        fig2.update_layout(height=140, margin=dict(l=0, r=0, t=5, b=0),
            yaxis_range=[min(0, valid["grade_pct"].min() - 2), max(18, valid["grade_pct"].max() + 2)],
            yaxis_title="Grade %")
        st.plotly_chart(fig2, use_container_width=True)

        # Warnings
        steep_down = valid[valid["grade_pct"] < -8]
        if len(steep_down) > 0:
            st.warning(f"{len(steep_down)} segmen grade < -8% — Laden turun curam (rem blong). Kosong naik deras.")
        steep_up_empty = valid[valid["grade_pct"] > 8]
        if len(steep_up_empty) > 0:
            st.info(f"{len(steep_up_empty)} segmen grade > 8% — Laden naik deras (boros BBM pit→ROM).")

        # CH Selector
        ch_opts = sorted(valid["chainage"].dropna().unique().astype(int).tolist())
        if len(ch_opts) > 0:
            options = ["--- Tampilkan Seluruh Lintasan (Extent) ---"] + ch_opts
            if st.session_state.selected_ch in ch_opts:
                default_idx = options.index(st.session_state.selected_ch)
            else:
                default_idx = 0
            sel_ch = st.selectbox("Pilih segmen (CH) untuk lihat di peta", options, index=default_idx)
            if sel_ch == "--- Tampilkan Seluruh Lintasan (Extent) ---":
                st.session_state.selected_ch = None
            else:
                st.session_state.selected_ch = sel_ch
        truck = get_truck(fleet_key)

        # Tabs
        tab_flag, tab_esg, tab_brkt = st.tabs(["Segmen >8%", "ESG Detail", "Bracket Grade"])

        with tab_flag:
            if len(flagged) > 0:
                flagged_display = flagged[["chainage", "z_dtm", "grade_pct", "flags"]].copy()
                flagged_display["chainage"] = flagged_display["chainage"].round(0).astype(int)
                flagged_display["grade_pct"] = flagged_display["grade_pct"].round(1)
                flagged_display = flagged_display.rename(
                    columns={"chainage": "CH (m)", "z_dtm": "Elev (m)", "grade_pct": "Grade %", "flags": "Flag"})
                flagged_display.insert(0, "Peta", "Goto")
                st.caption("Klik baris tabel untuk menyorot lokasi di peta")
                event_flag = st.dataframe(
                    flagged_display, use_container_width=True, height=180,
                    on_select="rerun", selection_mode="single-row", key="df_flagged"
                )
            else:
                st.success("Semua segmen sudah di grade ideal (<8%)")

        with tab_esg:
            if len(flagged) > 0:
                st.markdown("**Rincian BBM per segmen 20m:**")
                seg_rows = []
                for _, row in flagged.iterrows():
                    g = row["grade_pct"]; ch = int(row["chainage"])
                    rt = calc_round_trip(truck, grade_pct=g, distance_m=20)
                    rt8 = calc_round_trip(truck, grade_pct=8, distance_m=20)
                    waste = rt["fuel_round_L"] - rt8["fuel_round_L"]
                    cost_yr = waste * trips_yr * fuel_price
                    pct = (waste / rt["fuel_round_L"]) * 100 if rt["fuel_round_L"] > 0 else 0
                    seg_rows.append({
                        "CH (m)": ch, "Grade %": round(g, 1),
                        "Round-Trip (L)": rt["fuel_round_L"],
                        "Waste L/trip": round(waste, 3),
                        "Waste": f"{pct:.0f}%",
                        "Cost Rp/thn": int(cost_yr),
                    })
                df_esg_seg = pd.DataFrame(seg_rows)
                df_esg_seg.insert(0, "Peta", "Goto")
                st.caption("Klik baris tabel untuk menyorot lokasi di peta")
                event_esg = st.dataframe(
                    df_esg_seg, use_container_width=True, height=180,
                    on_select="rerun", selection_mode="single-row", key="df_esg",
                    column_config={"Cost Rp/thn": st.column_config.NumberColumn(format="Rp %d")}
                )

                st.markdown("**Potensi saving per 1% penurunan grade:**")
                saving_rows = []
                for _, row in flagged.iterrows():
                    g = row["grade_pct"]; ch = int(row["chainage"])
                    rt_g = calc_round_trip(truck, grade_pct=g, distance_m=20)["fuel_round_L"]
                    saves = {}
                    for s in [1, 2, 3]:
                        if g - s >= 8:
                            rt_t = calc_round_trip(truck, grade_pct=g - s, distance_m=20)["fuel_round_L"]
                            cost = (rt_g - rt_t) * trips_yr * fuel_price
                            saves[f"Turun {s}%"] = f"Rp {int(cost):,}"
                    if saves:
                        saving_rows.append({"CH (m)": ch, "Grade %": round(g, 1), **saves})
                if saving_rows:
                    st.dataframe(pd.DataFrame(saving_rows), use_container_width=True, height=180)

                st.markdown("**Simulasi konsumsi per grade (panjang rata-rata):**")
                avg_len = valid["chainage"].diff().dropna().median()
                avg_len = max(20, round(avg_len / 10) * 10) if not np.isnan(avg_len) else 20
                base_8 = calc_round_trip(truck, grade_pct=8, distance_m=avg_len)
                sim_rows = []
                for g in range(8, 17):
                    r_g = calc_round_trip(truck, grade_pct=g, distance_m=avg_len)
                    waste = r_g["fuel_round_L"] - base_8["fuel_round_L"]
                    pct = (waste / r_g["fuel_round_L"]) * 100 if r_g["fuel_round_L"] > 0 else 0
                    sim_rows.append({
                        "Grade": f"{g}%",
                        f"Fuel L/{avg_len:.0f}m (pp)": r_g["fuel_round_L"],
                        "Waste L/trip": round(waste, 2),
                        "Waste": f"{pct:.0f}%",
                        "Waste L/thn": int(waste * trips_yr),
                        "Cost Rp/thn": int(waste * trips_yr * fuel_price),
                    })
                st.caption(f"Panjang segmen rata-rata: {avg_len:.0f} m")
                st.dataframe(pd.DataFrame(sim_rows), use_container_width=True, height=180,
                             column_config={"Cost Rp/thn": st.column_config.NumberColumn(format="Rp %d")})
            else:
                st.success("Semua segmen sudah di grade ideal (<8%)")

        with tab_brkt:
            brackets = []
            for g in range(8, 16):
                seg_g = valid[(valid["grade_pct"] > g) & (valid["grade_pct"] <= g + 1)]
                if len(seg_g) == 0: continue
                total_len = len(seg_g) * 20
                waste = 0
                for _, row in seg_g.iterrows():
                    r_a = calc_round_trip(truck, grade_pct=row["grade_pct"], distance_m=20)
                    r_8 = calc_round_trip(truck, grade_pct=8, distance_m=20)
                    waste += r_a["fuel_round_L"] - r_8["fuel_round_L"]
                total_fuel = sum(calc_round_trip(truck, grade_pct=rt["grade_pct"], distance_m=20)["fuel_round_L"] for _, rt in seg_g.iterrows())
                cost_yr = waste * trips_yr * fuel_price
                pct = (waste / total_fuel) * 100 if total_fuel > 0 else 0
                brackets.append({
                    "Grade Range": f"{g}% – {g+1}%",
                    "Segmen": len(seg_g),
                    "Panjang (m)": total_len,
                    "Waste L/thn": int(waste * trips_yr),
                    "Waste": f"{pct:.0f}%",
                    "Cost Rp/thn": int(cost_yr),
                })
            df_bracket = pd.DataFrame(brackets) if brackets else pd.DataFrame()
            if len(df_bracket) > 0:
                st.dataframe(df_bracket, use_container_width=True, height=220,
                             column_config={"Cost Rp/thn": st.column_config.NumberColumn(format="Rp %d")})
            else:
                st.success("Tidak ada segmen >8%")

with col_map:
    fig = go.Figure()

    if not st.session_state.processed:
        # Show map of Indonesia before processing
        cx, cy = 118.0, -2.5
        zoom = 4.4
        
        fig.add_trace(go.Scattermapbox(
            lon=[118.0], lat=[-2.5],
            mode="markers",
            marker=dict(size=1, color="rgba(0,0,0,0)"),
            hoverinfo="none", showlegend=False
        ))
        
        st.markdown(
            """
            <div style="position: absolute; top: 15px; left: 15px; z-index: 1000; 
                        background: rgba(255, 255, 255, 0.95); padding: 12px 18px; 
                        border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                        font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #1d3557;
                        border-left: 4px solid #e63946; font-weight: 600;">
                Silakan lengkapi input di sebelah kiri, lalu klik <b>Process Data</b> untuk memulai analisis haul road.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Build coordinates
        all_lons, all_lats = [], []
        for _, row in df.iterrows():
            if pd.notna(row["grade_pct"]):
                lon, lat = to_latlon.transform(row["x_dxf"], row["y_dxf"])
                all_lons.append(lon)
                all_lats.append(lat)

        fg_lons, fg_lats, fg_grades, fg_texts, fg_chs = [], [], [], [], []
        for _, row in sub_df.iterrows():
            g = row["grade_pct"]
            if pd.isna(g): continue
            lon, lat = to_latlon.transform(row["x_dxf"], row["y_dxf"])
            fg_lons.append(lon); fg_lats.append(lat); fg_grades.append(g)
            fg_chs.append(int(row["chainage"]))
            fg_texts.append(f"CH {row['chainage']:.0f}m<br>Grade {g:.1f}%<br>Elev {row['z_dtm']:.0f}m")

        highlight_idx = None
        if st.session_state.selected_ch is not None and len(fg_chs) > 0:
            distances = [abs(ch - st.session_state.selected_ch) for ch in fg_chs]
            highlight_idx = distances.index(min(distances))

        # Center/Zoom
        if highlight_idx is not None and len(fg_lons) > highlight_idx:
            cx, cy = fg_lons[highlight_idx], fg_lats[highlight_idx]
            zoom = 17
        elif len(fg_lons) > 0:
            min_lon, max_lon = min(fg_lons), max(fg_lons)
            min_lat, max_lat = min(fg_lats), max(fg_lats)
            cx = (min_lon + max_lon) / 2
            cy = (min_lat + max_lat) / 2
            lon_diff = max_lon - min_lon
            lat_diff = max_lat - min_lat
            max_diff = max(lon_diff, lat_diff)
            if max_diff > 0:
                zoom = max(10, min(18, int(np.log2(360 / max_diff)) - 1))
            else:
                zoom = 14
        else:
            cx, cy = 118.0, -2.5
            zoom = 4.4

        # Full network
        fig.add_trace(go.Scattermapbox(
            lon=all_lons, lat=all_lats,
            mode="markers+lines",
            line=dict(width=1.0, color="lightgray"),
            marker=dict(size=3, color="lightgray", opacity=0.4),
            hoverinfo="none", showlegend=False,
        ))

        # Selected road
        fig.add_trace(go.Scattermapbox(
            lon=fg_lons, lat=fg_lats,
            mode="markers+lines",
            line=dict(width=4, color="black"),
            marker=dict(size=11, color=[color_for_grade(g) for g in fg_grades], opacity=0.95),
            text=fg_texts, hoverinfo="text",
            hoverlabel=dict(bgcolor="black", font=dict(color="white", size=13)),
            showlegend=False,
        ))

        # Highlight CH
        if highlight_idx is not None:
            fig.add_trace(go.Scattermapbox(
                lon=[fg_lons[highlight_idx]], lat=[fg_lats[highlight_idx]],
                mode="markers",
                marker=dict(size=24, color="yellow", opacity=0.9, symbol="circle"),
                hoverinfo="none", showlegend=False,
            ))

        # Legend
        for label, color in [("Grade >10%", "red"), ("Grade 8-10%", "orange"),
                             ("Grade <8%", "green"), ("No data", "gray")]:
            fig.add_trace(go.Scattermapbox(
                lon=[0], lat=[-90], mode="markers", showlegend=True,
                marker=dict(size=8, color=color, opacity=0.8), name=label, hoverinfo="none"))

    fig.update_layout(
        mapbox=dict(style="open-street-map", center=dict(lat=cy, lon=cx), zoom=zoom),
        margin=dict(l=0, r=0, t=0, b=0), height=1000,
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            y=0.01,
            x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
