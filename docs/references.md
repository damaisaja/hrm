# Referensi Dump Truck & Formula Efisiensi Road Slope

## Daftar Isi

1. [Research Papers](#1-research-papers)
2. [Official Handbooks](#2-official-handbooks)
3. [Formulasi Perhitungan](#3-formulasi-perhitungan)
4. [Fleet Database](#4-fleet-database)
5. [Fuel Impact Factors](#5-fuel-impact-factors)

---

## 1. Research Papers

### [1] SAE Technical Paper 2022-01-5030
**Title:** The Effect of Road Grade on Dump Truck Fuel Consumption
**Authors:** Harjuni Hasan (Mulawarman University), Realingga Octariando (Peers, Indonesia)
**Published:** April 20, 2022
**DOI:** https://doi.org/10.4271/2022-01-5030

**Key Findings (Laden Condition):**
| Dump Truck | Engine RPM Increase | HP Increase | Fuel Consumption Increase |
|------------|:------------------:|:-----------:|:-------------------------:|
| CAT 773D   | 0.482-0.515%       | 2.79%       | **21.95% per 1% grade**  |
| HD 465-7   | —                  | —           | **23.64% per 1% grade**  |
| Volvo A40E | —                  | —           | **13.29% per 1% grade**  |

**Recommendation:** Maximum road grade 8% for fuel efficiency.

### [2] E3S Web of Conferences (2024)
**Title:** Effect of Transport Road Slope on Fuel Consumption of Coal Mine Transport Truck
**Authors:** Saptarini, Hidayatullah, Marul, Suprianto (Politeknik Negeri Banjarmasin)
**DOI:** https://doi.org/10.1051/e3sconf/202450303006

**Case Study:** Komatsu HD 785-7 at PT Kalimantan Prima Persada (South Kalimantan)
- Setiap penambahan 1% road slope → **+4,820 liter** (laden), **+2,071 liter** (unladen)
- Total power required for 1.47 km at grade: 6.47 MW
- Fuel consumption per trip: 19.25 liters
- Fuel costs = 22% of total mining cost, can reach 30-40% in coal mining

### [3] Mining3 — University of Queensland
**Title:** Rolling Resistance Plays a Critical Role in Fuel Consumption of Mining Haul Trucks
**Authors:** Soofastaei, Adair, Aminossadati, Kizil, Knights
**Key Parameters Affecting Rolling Resistance (ranked):**
1. Road maintenance frequency
2. Tire pressure
3. Truck speed
4. Road surface material
5. Temperature

### [4] Transportation Research Part D (2025)
**Title:** Road Grade and Truck Weight Matter: Investigating Link-Level Energy Consumption Uncertainty
**DOI:** https://doi.org/10.1016/j.trd.2025.104900
- Menggunakan average speed saja untuk segmen 5 km → **25% error**
- Error turun ke **11%** ketika road grade, truck weight, dan acceleration diikutsertakan

---

## 2. Official Handbooks

### Caterpillar Performance Handbook — Edition 29
- Chapter 9: Construction & Mining Trucks
- Chapter 16: Owning & Operating Costs (fuel consumption tables)
- Tabel fuel consumption per model berdasarkan kondisi operasi (Low/Medium/High)

### Komatsu Performance Handbook
- Fuel consumption tables untuk setiap seri HD
- K-ATOMiCS transmission fuel efficiency data

### Komatsu HD785-7 Official Specs
- Engine: SAA12V140E-3, 895 kW (1,200 HP)
- Payload: 91.7 tonnes
- GVW: 163.8 tonnes
- Top speed: 65 km/h

---

## 3. Formulasi Perhitungan

### 3.1 Grade Resistance

```
GR = G × sinθ

dimana:
  GR = Grade resistance (N)
  G  = GVW (kg) × 9.81 (N)
  θ  = arc tan(grade%/100)
```

### 3.2 Rolling Resistance

```
RR = R × G × cosθ

dimana:
  RR = Rolling resistance (N)
  R  = Koefisien rolling resistance
       - 0.015 : Road surface excellent
       - 0.025 : Haul road terawat (default)
       - 0.035 : Road surface average
       - 0.050 : Road surface buruk / muddy
  G  = GVW (kg) × 9.81 (N)
```

### 3.3 Total Resistance

```
TR = GR + RR

Grade Resistance: 10 kg/ton per 1% grade
Rolling Resistance: 20 kg/ton (typical haul road) — setara dengan grade 2%
```

### 3.4 Power Required

```
P = TR × v / 1000

dimana:
  P = Power at wheels (kW)
  TR = Total tractive force (N)
  v  = Speed (m/s)
```

### 3.5 Fuel Consumption

```
Fuel rate = P / (η × E_diesel)

dimana:
  η         = Engine efficiency (~0.35)
  E_diesel  = 38.6 MJ/L
```

### 3.6 Fuel Consumption per Trip

```
Total = Fuel_rate × (Distance / Speed)
```

### 3.7 CO₂ Emission

```
CO₂ = Fuel_total × 2.68

dimana:
  2.68 = kg CO₂ per liter diesel (IPCC default)
```

### 3.8 Financial Impact

```
Fuel Cost      = Fuel_total × Harga_solar
Carbon Cost    = CO₂_ton × Harga_karbon
Total Saving   = Fuel Cost Saving + Carbon Cost Saving
```

**Assumptions:**
- Harga solar industri: Rp 12.000/liter
- Harga karbon: Rp 336.000/ton CO₂ (estimasi pasar karbon Indonesia)
- 1 ton CO₂ = 1 carbon credit

---

## 4. Fleet Database

### Rigid Frame Trucks (40-400+ ton)

| Model | Power (kW) | Payload (t) | GVW (t) | Fuel (L/hr) |
|-------|:----------:|:-----------:|:-------:|:-----------:|
| Komatsu HD325-8 | 383 | 36.5 | 66.5 | 22-30 |
| Komatsu HD405-8 | 383 | 40.0 | 72.0 | 24-32 |
| CAT 773D | 485 | 43.7 | 99.3 | 38-48 |
| CAT 773G | 615 | 56.0 | 102.7 | 32-42 |
| Komatsu HD465-7 | 551 | 55.0 | 99.7 | 35-48 |
| Komatsu HD785-7 | 895 | 91.7 | 163.8 | 55-75 |
| Hitachi EH3500 | 1,491 | 181.0 | 322.0 | 120-160 |
| Liebherr T282B | 2,720 | 363.0 | 592.0 | 200-280 |

### Articulated Dump Trucks (ADTs) — 10-40 ton

| Model | Power (kW) | Payload (t) | GVW (t) | Fuel (L/hr) |
|-------|:----------:|:-----------:|:-------:|:-----------:|
| CAT 725 | 257 | 24.0 | 46.7 | 14-20 |
| Volvo A25G | 237 | 25.0 | 47.7 | 14-19 |
| CAT 730 | 242 | 28.0 | 50.9 | 16-22 |
| Volvo A30G | 265 | 28.0 | 52.0 | 15-20 |
| Komatsu HM300-5 | 248 | 28.0 | 53.4 | 16-24 |
| Doosan DA30-5 | 276 | 28.0 | 52.0 | 16-22 |
| CAT 735 | 316 | 32.0 | 61.8 | 20-28 |
| Volvo A35G | 336 | 33.5 | 62.7 | 22-30 |
| Scania P460 | 338 | 35.0 | 60.0 | 15-25 |
| Bell B40E | 320 | 36.5 | 63.2 | 20-28 |
| Volvo A40G | 336 | 39.0 | 69.7 | 24-32 |
| CAT 740 | 336 | 39.5 | 71.9 | 24-34 |
| Komatsu HM400-5 | 353 | 40.0 | 75.1 | 22-30 |

---

## 5. Fuel Impact Factors

### Berdasarkan [1] Hasan (2022) — setiap 1% kenaikan grade:

| Model | Faktor (laden) | Faktor (unladen) |
|-------|:--------------:|:----------------:|
| CAT 773D | **+21.95%** fuel | +7.64% fuel |
| HD465-7 | **+23.64%** fuel | +20.60% fuel |
| Volvo A40E | **+13.29%** fuel | +23.75% fuel |

**Interpretasi:** Pada CAT 773D laden, grade 8% → fuel = 1 + (8 × 0.2195) = **2.756×** fuel dibanding grade 0%.

### Berdasarkan [2] Saptarini (2024) — HD785-7:

| Kondisi | Tambahan Fuel per 1% slope |
|---------|:--------------------------:|
| Laden (muatan) | +4,820 liter |
| Unladen (kosong) | +2,071 liter |

---

## 6. Recommended Road Grade Standards

| Source | Max Grade | Notes |
|--------|:---------:|-------|
| Hasan (2022) [1] | **8%** | Fuel efficiency optimum |
| Caterpillar Handbook [4] | **8-10%** | Bergantung pada truck spesifik |
| AASHTO (Green Book) | **6-8%** | Highway standards adapted for mine |
| Indonesian Mine Standard | **8%** | Standard tambang Indonesia |

### Grade Classification untuk Mine Road:

| Grade (%) | Klasifikasi | Dampak Fuel |
|:---------:|-------------|:-----------:|
| 0-4 | Low | Baseline |
| 4-6 | Moderate | +20-40% |
| 6-8 | High | +40-80% |
| 8-10 | Very High | +80-120% |
| >10 | Extreme | >+120% |

---

## Code Implementation

Semua formula di atas sudah diimplementasikan di:

```
src/fuel_optimizer/engine.py      → Perhitungan fuel, grade impact, CO₂
src/utils/fleet_db.py             → Database spesifikasi dump truck
src/esg_calculator/               → ESG & carbon cost calculator
```

## Tools Komersial Pembanding

| Software | Fitur | Keterbatasan |
|----------|-------|-------------|
| **TALPAC** (Runge) | Cycle time & fuel analysis | Mahal, closed-source |
| **Cat MineStar** | Fleet monitoring + fuel | Hanya untuk CAT |
| **Komatsu KOMTRAX** | Telematics + fuel | Hanya untuk Komatsu |
| **Alteia** | Drone + haul road analysis | Platform as a Service |
| **Softree RoadEng** | Road design optimization | Civil engineering focus |
| **HAULLING** (ini) | Drone → Fuel Saving → ESG | Open, multi-OEM |
