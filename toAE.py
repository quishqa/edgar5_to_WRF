#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xarray as xr
import numpy as np
import os
from pathlib import Path

POLS = ["BC", "CO", "NMVOC", "NOx", "NH3",
        "OC", "PM2.5", "PM10", "SO2"]

SECTORS = ["AGS", "AWB", "CHE", "ENE", "FFF",
           "FOO_PAP", "IND", "IRO", "NFE", "NEU",
           "MNM", "NMM", "PRUS_SOL", "PRO", "RCO",
           "REF_TRF", "SWD_INC", "SWD_LDF", "TNR_Aviation_CDS", "TNR_Aviation_CRS",
           "TNR_Aviation_LTO", "TNR_Aviation_SPS", "TNR_Other", "TNR_Ship", "TRO_RES",
           "TRO_noRES", "WWT"]



def add_date_datesec(edgar_file, year=2015):
    '''
    Add the 'date' and 'datesec' variables into
    edgar emission file

    Parameters
    ----------
    edgar_file : str
        edgar monthly emission file.
    year : int, optional
        year of the emission file. The default is 2015

    Returns
    -------
    edgar_date: xarray Dataset
        emission file with 'date' and 'datesec' variable
    '''
    month = int(edgar_file.split("2015_")[1].split("_")[0])
    time = np.array([month - 1])
    date = np.array([year * 10000 + month * 100 + 1])

    edgar_date = xr.open_dataset(edgar_file)
    var_name = list(edgar_date.data_vars)[0]
    edgar_date = edgar_date.rename({var_name:"emis_tot"})

    edgar_date["time"] = time
    edgar_date["date"] = xr.DataArray(date, dims=["time"])
    edgar_date["datesec"] = xr.DataArray(np.array([0]), dims=["time"])
    return edgar_date

def concat_sector_by_month(sector_path):
    '''
    Load and concat monthly emission into one netcdf

    Parameters
    ----------
    sector_path : str
        path of pollutant emission sector folder

    Returns
    -------
    year_emiss: xarray Dataset
        montly emission into one dataset

    '''
    sector = Path(sector_path)
    sector_files = [str(file) for file in list(sector.glob("*.nc"))]
    ds = {int(f.split("2015_")[1].split("_")[0]): add_date_datesec(f) 
            for f in sector_files}
    ds_sorted = dict(sorted(ds.items()))
    year_emiss = xr.concat(list(ds_sorted.values()), dim="time")
    return year_emiss

def join_pol_by_sector(pol_path, total=False):
    '''
    Read sector emissions and save them in one dict. If total = True
    it returns the total emission

    Parameters
    ----------
    pol_path : str
        Polutant emissions folder where sectors are
    total : Bool, optional
        sum all the sector emission. The default is False
    
    Returns
    -------
    pol_emi : xarray Dataset
       Total emission (sum of all sources)
    pol_by_sector: dictionary
        Dictionary with sectors monthtly emission in one dataset
    '''
    pol_folder = Path(pol_path)
    pol_sectors = [str(folder) for folder in pol_folder.glob("*/")]
    pol_by_sector = {sector.split("/")[-1]: concat_sector_by_month(sector) 
                     for sector in pol_sectors}
    if total:
        pol_emi = sum(pol_by_sector.values())
        pol_emi["date"] = pol_by_sector[list(pol_by_sector.keys())[1]].date
        return pol_emi
    else:
        return pol_by_sector

def group_sectors(pol_by_sector, sectors):
    '''
    Group emissions sector in a single group (i.e. IPCC 96)

    Parameters
    ----------
    pol_by_sector : dict
        Dictionary with sectors monthly emission in onde dataset
    sectors : list
        List of sectors to merge
    '''
    group = {sector: pol_by_sector[sector] for sector in sectors 
             if sector in pol_by_sector.keys()}
    group_total = sum(group.values())
    group_total["date"] = pol_by_sector[list(pol_by_sector.keys())[1]].date
    return group_total
    
# Group sectors 
energy = ["ENE", "REF_TRF", "TNR_Aviation_CDS", "TNR_Aviation_CRS",
          "TNR_Aviation_LTO", "TNR_Aviation_SPS", "TRO_RES", "TRO_noRES",
          "TNR_Other", "TNR_Ship", "RCO", "PRO"]
industrial = ["NMM", "CHE", "IRO", "NFE", "NEU", "FOO_PAP"]
solvents = ["PRU_SOL"]
agriculture = ["MNM", "AWB", "AGS"]
waste = ["SWD_LDF", "SWD_INC", "WWT"]

# Other groups
road_transport = ["TRO_noRES", "TRO_RES"]
energy_no_road = [pol for pol in energy if pol not in road_transport]

AGS_path = "/scr2/mgavidia/wrf_utils/edgar5_monthly/AGS"
pm25_ags = concat_sector_by_month(AGS_path)


pol_path = "/scr2/mgavidia/wrf_utils/edgar5_monthly/"

pm25_sec = join_pol_by_sector(pol_path)
pm25 = join_pol_by_sector(pol_path, total=True)

pm25.to_netcdf("v50_PM2.5_test_year_total.nc")

trans_pm25 = group_sectors(pm25_sec, road_transport)















