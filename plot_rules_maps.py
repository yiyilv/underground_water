
import os
from typing import Dict, Tuple, List

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt


def _make_points_gdf(csv_path: str,
                     lon_col: str = "lon",
                     lat_col: str = "lat",
                     crs_points: str = "EPSG:4326") -> gpd.GeoDataFrame:
    df = pd.read_csv(csv_path)
    if lon_col not in df.columns or lat_col not in df.columns:
        raise ValueError(f"CSV {csv_path} must contain '{lon_col}' and '{lat_col}' columns.")
    gdf = gpd.GeoDataFrame(
        df,
        geometry=[Point(xy) for xy in zip(df[lon_col], df[lat_col])],
        crs=crs_points
    )
    return gdf


def _add_north_arrow(ax, size: float = 0.1, pad: float = 0.02):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    dx = x1 - x0
    dy = y1 - y0
    x_anchor = x1 - dx * pad
    y_anchor = y1 - dy * pad
    L = dy * size
    ax.annotate("", xy=(x_anchor, y_anchor - L), xytext=(x_anchor, y_anchor),
                arrowprops=dict(arrowstyle="simple", linewidth=1.2))
    ax.text(x_anchor, y_anchor, "N", ha="center", va="bottom", fontsize=10, weight="bold")


def plot_rules_maps(shapefile_path: str,
                    rule_csvs: Dict[str, str],
                    out_dir: str,
                    lon_col: str = "lon",
                    lat_col: str = "lat",
                    crs_points: str = "EPSG:4326",
                    figsize_single: Tuple[float, float] = (6, 8),
                    point_size: float = 4.0,
                    point_alpha: float = 0.9,
                    point_color: str = "#8A0D0D",
                    edge_color: str = "black",
                    edge_lw: float = 0.5,
                    mosaic_cols: int = 3,
                    dpi: int = 300,
                    tight: bool = True) -> List[str]:

    os.makedirs(out_dir, exist_ok=True)

    base_gdf = gpd.read_file(shapefile_path)
    if base_gdf.empty:
        raise ValueError("Shapefile has no features.")
    base_crs = base_gdf.crs

    rules_gdfs = {}
    for label, csv_path in rule_csvs.items():
        gdf_pts = _make_points_gdf(csv_path, lon_col, lat_col, crs_points)
        if base_crs is not None:
            gdf_pts = gdf_pts.to_crs(base_crs)
        rules_gdfs[label] = gdf_pts

    xmin, ymin, xmax, ymax = base_gdf.total_bounds

    saved_paths = []

    for label, gdf_pts in rules_gdfs.items():
        fig, ax = plt.subplots(figsize=figsize_single, dpi=dpi)
        base_gdf.plot(ax=ax, edgecolor=edge_color, facecolor="none", linewidth=edge_lw)
        if not gdf_pts.empty:
            gdf_pts.plot(ax=ax, markersize=point_size, color=point_color, alpha=point_alpha)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_axis_off()
        ax.set_title(str(label), fontsize=16, weight="bold", pad=8)
        _add_north_arrow(ax)
        out_path = os.path.join(out_dir, f"{label}.png")
        if tight:
            plt.tight_layout()
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)
        saved_paths.append(out_path)

    if len(rules_gdfs) > 1:
        n = len(rules_gdfs)
        cols = mosaic_cols
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(cols * figsize_single[0], rows * figsize_single[1]), dpi=dpi)
        # Normalize axes to 2D list
        if rows == 1 and cols == 1:
            axes = [[axes]]
        elif rows == 1:
            axes = [axes]
        elif cols == 1:
            axes = [[ax] for ax in axes]

        labels = list(rules_gdfs.keys())
        for i in range(rows * cols):
            r, c = divmod(i, cols)
            ax = axes[r][c]
            if i < n:
                label = labels[i]
                gdf_pts = rules_gdfs[label]
                base_gdf.plot(ax=ax, edgecolor=edge_color, facecolor="none", linewidth=edge_lw)
                if not gdf_pts.empty:
                    gdf_pts.plot(ax=ax, markersize=point_size, color=point_color, alpha=point_alpha)
                ax.set_xlim(xmin, xmax)
                ax.set_ylim(ymin, ymax)
                ax.set_axis_off()
                ax.set_title(str(label), fontsize=16, weight="bold", pad=8)
                _add_north_arrow(ax)
            else:
                ax.set_axis_off()

        mosaic_path = os.path.join(out_dir, "mosaic.png")
        if tight:
            plt.tight_layout()
        fig.savefig(mosaic_path, dpi=dpi, bbox_inches="tight", pad_inches=0.05)
        plt.close(fig)
        saved_paths.append(mosaic_path)

    return saved_paths
