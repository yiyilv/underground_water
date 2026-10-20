# Satellite Altimetry Control-Point Workflows

Research notebooks and GIS utilities for **ICESat-2 ATL08 quality filtering and elevation control-point preparation**, with additional GEDI and GF-7 processing experiments.

The repository retains its original name, `underground_water`. Its current code primarily demonstrates altimetry extraction, rule-based screening, coordinate preparation, and mapping; a validated groundwater estimation model is not included.

## Workflow

1. Read ATL08 beam-level land-segment attributes from HDF5.
2. Restrict points to the study polygon, including a Poyang Lake boundary in the original analysis.
3. Build quality masks from elevation differences, terrain/urban/cloud flags, slope, and terrain-photon counts.
4. Compare eight combinations of those masks and export per-file point tables and rule summaries.
5. Map selected points and prepare coordinate-transformed or spatially sampled tables for subsequent processing.

## Repository guide

| File or directory | Purpose |
|---|---|
| `select_para.ipynb` | Main ATL08 extraction, polygon masking, quality-rule comparison, and CSV export |
| `plot_rules_maps.py` | Plot per-rule point distributions and a combined map |
| `GF7_step/` | Table merging, coordinate transformation, and representative-point selection notebooks |
| `GEDI/` | GEDI processing notebook |
| `controlpoints_out/` | Existing point exports and summary tables |
| `controlpoints_out_副本/` | Additional historical exports; not a separate validated experiment |
| `overlayer_image.ipynb` / `qgis.qgz` | Exploratory overlay and GIS materials |

`select_example.py` is a historical example with a source attribution embedded in the file. It contains formatting/text that needs repair before direct execution; use the main notebook as the starting point.

## Environment and inputs

Use Python with JupyterLab, NumPy, pandas, h5py, GeoPandas, Shapely, Matplotlib, xarray, Dask, and scikit-learn. Some exploratory notebooks may require additional dataset-specific tools. This is an initial dependency list inferred from the code, not a locked or fully tested environment.

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install jupyterlab numpy pandas h5py geopandas shapely matplotlib xarray "dask[dataframe]" scikit-learn
jupyter lab
```

Before running `select_para.ipynb`:

- Download the matching ATL08 HDF5 inputs separately.
- Replace the original absolute paths in `fname`, `files`, and the polygon-loading cell.
- Supply a study boundary with a known CRS; the notebook converts it to EPSG:4326.
- Review the quality-rule thresholds, output directories, and field names for your data version.
- Run the notebook from the top and inspect per-file and aggregate summaries.

The raw satellite inputs and all original external processing materials are not bundled. The notebooks retain exploratory cells and saved outputs, so a fresh end-to-end reproduction has not yet been established.

## Rule comparison

The main notebook defines masks `a` through `i`, then combines them as follows:

| Rule | Required masks |
|---|---|
| Rule1 | a, b |
| Rule2 | a, b, c |
| Rule3 | a, b, c, d |
| Rule4 | a, b, c, d, e |
| Rule5 | a, b, c, d, e, f |
| Rule6 | a, b, c, d, e, f, g |
| Rule7 | h, i |
| Rule8 | a, b, c, d, e, f, g, h, i |

The notebook records passing-point counts and rates. Those describe screening behaviour, not independent elevation accuracy or groundwater-retrieval performance. Thresholds are specific analysis settings and should be re-evaluated for each application.

## Contribution and related work

This repository records my research workflow development in ATL08 extraction, quality-mask comparison, control-point export, and GIS visualisation. Preserve the attribution on adapted examples and the terms of all external data and tools.

For a reusable package and CLI that generalises ATL08 extraction, quality filtering, beam handling, spatial masks, and export, see [ATL08KIT](https://github.com/yiyilv/ATL08KIT).

## Licence and data provenance

The repository includes an [MIT licence](LICENSE) for code covered by that licence. This does not establish a blanket licence for external examples, boundary archives, imagery, or derived datasets. The origins and redistribution terms of the existing `boundary.zip`, `lack.zip`, and historical data exports still need a source-by-source record before they can be recommended as reusable datasets.

