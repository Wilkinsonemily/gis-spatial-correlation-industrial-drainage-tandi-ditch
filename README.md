# GIS-Based Spatial Correlation Analysis of Industrial Areas and Drainage Networks in the Tandi Ditch, Dahan River Watershed

Case study: industrial areas of Xinzhuang District, New Taipei City, Taiwan.

This repository contains the QGIS file, scripts, figures and manuscript for a multi-criteria **Pollution Susceptibility Index (PSI)** that ranks 65 industrial areas by how likely they are to contaminate the Dahan River through the urban drainage network.

> **Status:** unpublished preprint manuscript, not peer reviewed.

## Summary

Most river monitoring measures water quality after pollution has already entered the main river. This study instead links land-based sources to the drainage channels that carry them. An industrial area is treated as susceptible only when three conditions coincide: it is close to drainage, the terrain routes runoff toward that drainage, and nearby measured water quality is already degraded.

## Method

Four evidence layers are normalized to a 0–1 score in QGIS and combined by weighted overlay:

| Layer | Method | Weight |
|---|---|---|
| Proximity | 100 / 300 / 500 m buffers and nearest-neighbor spatial join; `P = 1 − (d / 1200)` | 0.25 |
| Flow connectivity | Mean elevation per area (Zonal Statistics, 20 m DTM); inverted normalized elevation × normalized proximity (slope-and-distance proxy) | 0.30 |
| Sensor water quality | Dissolved oxygen and ammonia-nitrogen from 7 MoENV Dahan River stations, joined to the nearest station | 0.30 |
| Source intensity | Uniform weight (0.6), because OSM polygons have no reliable sub-type | 0.15 |

```
PSI = 0.25 × Proximity + 0.30 × Flow connectivity + 0.30 × Sensor WQ + 0.15 × Source intensity
```

PSI is classified into High / Moderate / Low by natural breaks (Jenks), with cut points at 0.614 and 0.737.

## Key results

- PSI ranges from 0.354 to 0.936 (mean 0.622) across 65 industrial areas.
- 12 High (18%), 17 Moderate (26%) and 36 Low (55%) areas.
- High-class areas lie 76 m from drainage on average and form a significant spatial cluster (average nearest-neighbor R = 0.51, z = −3.24, p < 0.01).
- Proximity, flow connectivity and sensor score each correlate with the PSI at r ≈ 0.5 (0.52, 0.51, 0.49).
- Downstream zone (Xinhai Bridge) has a higher mean PSI than upstream (0.71 vs 0.56).

## Data sources

| Dataset | Source |
|---|---|
| Drainage network, industrial areas (65) | OpenStreetMap contributors (`waterway`, `landuse=industrial`) |
| Terrain | NLSC Taiwan DTM 20 m |
| Boundary | NLSC township shapefile |
| Water quality (7 Dahan River stations) | Ministry of Environment (MoENV) river water-quality open data |

Station coordinates use TWD97 (EPSG:3826). Data © OpenStreetMap contributors, available under the ODbL. MoENV and NLSC data remain subject to their own open-data terms; see their websites.

## Repository structure

```
├── README.md
├── 01_raw_data/   OSM/NLSC source layers, station metadata, and the cleaning script
│                  (raw MoENV monthly exports are excluded — see Reproducing below)
├── 02_working/    intermediate GIS products (reprojected/clipped layers, buffers, rasters)
├── 03_outputs/    exported figures, maps and the QGIS project (.qgz)
└── .gitignore
```

## Reproducing the analysis

**Requirements:** QGIS 3.x; Python 3 with `pandas`.

1. Download the MoENV monthly water-quality exports (not included here — see Data sources) into `01_raw_data/`.
2. Run `01_raw_data/data_processing.py` to merge the monthly MoENV exports, keep records for 大漢溪, and take the latest value of each parameter per station. This produces `01_raw_data/sensors.csv`, which is included in this repo.
3. Open `03_outputs/figure1_studyarea.qgz` in QGIS. Most layers use paths relative to the project; two layers (a temp-folder raster and a file outside this project) will show as missing — remove or re-link them via *Layer → Data Source Manager*, or re-run the raster step that produced them from the files in `02_working/`.
4. Reproject to EPSG:3826, clip to Xinzhuang and filter industrial areas.
5. Compute the four layers and the PSI with the Field Calculator using the formula above, then classify by natural breaks.

## Limitations

Flow connectivity is a DEM-based proxy rather than a full flow-accumulation model; source intensity is uniform because industrial sub-type data were unavailable; the sensor score depends on a small number of stations. Future work: more stations, a full flow model, industrial sub-types, validation with laboratory grab samples, and a public web-GIS dashboard.

## Citation

Huang, L.-J. and Wilkinson, E. (2026). *A GIS-Based Spatial Correlation Analysis of Industrial Areas and Drainage Networks in the Tandi Ditch, Dahan River Watershed.* Unpublished preprint manuscript.

## Authors

Huang Ling-Jin (黃鈴斤) · Emily Wilkinson

Contact: [Wilkinsonemily](https://github.com/Wilkinsonemily)

## License

All rights reserved. No license is granted for reuse of the code, data, figures or manuscript in this repository. Third-party data (OpenStreetMap, MoENV, NLSC) remains subject to its own original terms, noted above.
