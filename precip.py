from pathlib import Path

import json
import fsspec
import intake
import xarray as xr
import matplotlib.pyplot as plt
import pooch
from pathlib import Path
import pandas as pd
import numpy as np


#surface air temp for one timestep: august, 20 years after

#get esm datastore
odie = pooch.create(
    # Use the default cache folder for the operating system
    path="./.cache",
    base_url="https://storage.googleapis.com/cmip6/",
    # The registry specifies the files that can be fetched
    registry={
        "pangeo-cmip6.csv": "e319cd2bf1daf9b5aa531f92c022d5322ee6bce0b566ac81dfae31dbae203fd9",
    },
)

file_path = odie.fetch("pangeo-cmip6.csv")
df = pd.read_csv(file_path)


#make sure to reload the df data from the first cell before running this
#scenario variability

#comparing the average of all runs from multiple scenarios..?


def get_precip_df(df, var_id, mod_id, exp_id, members, monthly_table):
    df = df[(df["variable_id"] == var_id)]
    df = df[(df["experiment_id"] == exp_id)]
    df = df[(df["source_id"] == mod_id)]
    df = df[(df["table_id"] == monthly_table)]
    
    dstore_filename = df["zstore"].values[0]
    xarray_dset = xr.open_zarr(fsspec.get_mapper(dstore_filename), consolidated=True)
    spatial_mean = xarray_dset.mean(dim=["lat", "lon"])
    times = spatial_mean.indexes["time"].to_datetimeindex()

    avg_df = pd.DataFrame(index=times)

    
    for i in range(members):
        dstore_filename = df["zstore"].values[i]
        xarray_dset = xr.open_zarr(fsspec.get_mapper(dstore_filename), consolidated=True)
        spatial_mean = xarray_dset.mean(dim=["lat", "lon"])

        times = spatial_mean.indexes["time"].to_datetimeindex()
        precip = spatial_mean["pr"].values
        avg_df["pr" + str(i)] = precip

    avg_df['mean'] = avg_df.mean(axis=1)
    
    return avg_df



var_id = "pr" #precipitation, (kg m-2 s-1)
mod_id = "CanESM5"
exp_id = ["ssp585", "ssp245"] #compare a couple scenarios
members = 25 #there are 50 models for each of these scenarios
monthly_table = "Amon" #monthly atmospheric data
#2015-01 -> 2100-12


avg_df_ssp585 = get_precip_df(df, var_id, mod_id, exp_id[0], members, monthly_table)
avg_df_ssp245 = get_precip_df(df, var_id, mod_id, exp_id[1], members, monthly_table)

plt.rcParams['figure.figsize'] = (10,5)


'''
#plotting the individual runs looks messy with multiple scenarios, but could make error bars maybe or something
for i in range(members):
    plt.plot(avg_df_ssp585.index[:100], avg_df_ssp585['pr' + str(i)][:100], color="blue", alpha=0.2)
    plt.plot(avg_df_ssp245.index[:100], avg_df_ssp245['pr' + str(i)][:100], color="red", alpha=0.2)
'''

plt.plot(avg_df_ssp585.index[:100], avg_df_ssp585['mean'][:100], color="blue")
plt.plot(avg_df_ssp245.index[:100], avg_df_ssp245['mean'][:100], color="red")
plt.ylabel("precipitation (kg m-2 s-1)")
plt.title("CanESM5, ssp585 vs. ssp245, precip, "+ str(members) + " runs averaged")
plt.legend(["ssp585", "ssp245"])
plt.savefig('./plot_dir/1model-2exp-25runsavg.png')
plt.show()