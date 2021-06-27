#!/bin/bash
# 
# Script to download monthly emission from EDGAR 4.0
# for different pollutants and sectors
#
# AGS: Agricultural soils*
# AWB: Agricultural waste burning
# CHE: Chemical processes
# ENE: Power industry
# FFF: Fossil fuel fires
# FOO_PAP: Food and paper
# IND: Combustion for manufactoring
# IRO: Iron and steel production
# NFE: Non-ferrous metals production
# NEU: Non energy use of fuels (only for PM10)
# NMM: Non-metallic minerals production 
# MNM: Manure management*
# PRO: Fuel exploitation
# PRU_SOL: Solvents and products use*
# RCO: Energy for buildings
# REF_TRF: Oil refineries and Transformation industry
# SWD_INC: Solid waste incineration
# SWD_LDF: Solid waste landfills*
# TNR_Aviation_CDS: Aviation climbing&descent
# TNR_Aviation_CRS: Aviation Cruise
# TNR_Aviation_LTO: Aviation landing&takeoff
# TNR_Aviation_SPS: Aviation supersonic
# TNR_Other: Railways, pipelines, off-road transport
# TNR_Ship: Shipping
# TRO_RES: Road transportation resuspension
# TRO_noRES: Road transportation no resuspension
# WWT: Waste water handling*

POLS=("BC" "CO" "NH3" "NMVOC" "NOx" "OC" "PM2.5" "PM10" "SO2")

SECTORS=("AGS" "AWB" "CHE" "ENE" "FFF" 
         "FOO_PAP" "IND" "IRO" "NFE" "NEU"
         "MNM" "NMM" "PRUS_SOL" "PRO" "RCO" "REF_TRF"
         "SWD_INC" "SWD_LDF" "TNR_Aviation_CDS" "TNR_Aviation_CRS" "TNR_Aviation_LTO"
         "TNR_Aviation_SPS" "TNR_Other" "TNR_Ship" "TRO_RES" "TRO_noRES" "WWT")

YEARS=$(seq 2015 2015)

for pol in ${POLS[@]}; do
    for sec in ${SECTORS[@]}; do
        for yr in ${YEARS[@]}; do
            wget "http://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v50_AP/"${pol}"/"${sec}"/v50_"${pol}"_"${yr}"_monthly_"${sec}"_nc.zip"
        done
    done
done


