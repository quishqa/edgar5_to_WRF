#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

wrf = xr.open_dataset("./wrfinput_d01")
edg4 = xr.open_dataset("./EDGAR_HTAP_emi_PM2.5_2010.0.1x0.1.nc")
edg5 = xr.open_dataset("./v50_PM2.5_2015.0.1x0.1.nc")

htap_oc = xr.open_dataset("./EDGAR_HTAP_emi_OC_2010.0.1x0.1.nc")
htap_bc = xr.open_dataset("./EDGAR_HTAP_emi_BC_2010.0.1x0.1.nc")
edgar5_oc = xr.open_dataset("./v50_OC_2015.0.1x0.1.nc")
edgar5_bc = xr.open_dataset("./v50_BC_2015.0.1x0.1.nc")

sp_lat = -23.5
sp_lon = -46.5


pm25_edg4 = edg4.sel(lat=sp_lat, lon=sp_lon % 360, method="nearest")
pm25_edg5 = edg5.sel(lat=sp_lat, lon=sp_lon % 360, method="nearest")


def clip_edgar_wrf(edgar, wrfinput):
    lat_min = wrfinput.XLAT.min()
    lat_max = wrfinput.XLAT.max()
    lon_min = wrfinput.XLONG.min()
    lon_max = wrfinput.XLONG.max()

    edgar_dom = edgar.sel(
            lat=slice(lat_min, lat_max),
            lon=slice(lon_min % 360, lon_max % 360)
            )
    return edgar_dom


pm25_edg4_dom = clip_edgar_wrf(edg4, wrf)
pm25_edg5_dom = clip_edgar_wrf(edg5, wrf)

htap_oc_dom = clip_edgar_wrf(htap_oc, wrf)
edg5_oc_dom = clip_edgar_wrf(edgar5_oc, wrf)
htap_bc_dom = clip_edgar_wrf(htap_bc, wrf)
edg5_bc_dom = clip_edgar_wrf(edgar5_bc, wrf)

def plot_htap_vs_edgar5(htap, edgar5, wrf, pol, t=5):
    vmax = max([htap.emis_tot.max(),
                edgar5.emis_tot.max()])
    lat_min = wrf.XLAT.min()
    lat_max = wrf.XLAT.max()
    lon_min = wrf.XLONG.min()
    lon_max = wrf.XLONG.max()

    fig, axes = plt.subplots(1, 2,
                             subplot_kw={"projection": ccrs.PlateCarree()})
    htap.isel(time=t).emis_tot.plot(ax=axes[0], vmax=vmax, vmin=0,
                                    add_colorbar=False, cmap="inferno_r")
    im = edgar5.isel(time=t).emis_tot.plot(ax=axes[1], vmax=vmax, vmin=0,
                                           add_colorbar=False, cmap="inferno_r")
    for ax, title in zip(axes.flat, ["HTAP", "EDGAR5"]):
        ax.set_extent([lon_min, lon_max, lat_min, lat_max])
        ax.add_feature(cfeature.OCEAN, zorder=100, edgecolor="k", 
                       facecolor="white", linewidth=0.75)
        ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.5)
        ax.set_title(title)
    cb = fig.colorbar(im, ax=axes.ravel().tolist(), pad=0.05, 
                      shrink=0.45, orientation="horizontal")
    cb.set_label(pol + " $(Kg \; m^{-2} \; s^{-1})$")
    plt.savefig(pol + "_htap_vs_edgar5.png", dpi=300, bbox_inches="tight")

plot_htap_vs_edgar5(pm25_edg4_dom, pm25_edg5_dom, wrf, "PM2.5")
plot_htap_vs_edgar5(htap_oc_dom, edg5_oc_dom, wrf, "OC")
plot_htap_vs_edgar5(htap_bc_dom, edg5_bc_dom, wrf, "BC")



