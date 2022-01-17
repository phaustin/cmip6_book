# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from pathlib import Path

# %%
import json
import fsspec
import intake
import xarray as xr
import matplotlib.pyplot as plt
import pooch
from pathlib import Path
import pandas as pd
import numpy as np


# %% [markdown]
# surface air temp for one timestep: august, 20 years after

# %%
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

# %%
file_path = odie.fetch("pangeo-cmip6.csv")
df = pd.read_csv(file_path)


# %% [markdown]
# make sure to reload the df data from the first cell before running this
# scenario variability

# %% [markdown]
# comparing the average of all runs from multiple scenarios..?


# %%
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

# %%

# %%
var_id = "pr" #precipitation, (kg m-2 s-1)
mod_id = "CanESM5"
exp_id = ["ssp585", "ssp245"] #compare a couple scenarios
members = 25 #there are 50 models for each of these scenarios
monthly_table = "Amon" #monthly atmospheric data
#2015-01 -> 2100-12


# %%
avg_df_ssp585 = get_precip_df(df, var_id, mod_id, exp_id[0], members, monthly_table)
avg_df_ssp245 = get_precip_df(df, var_id, mod_id, exp_id[1], members, monthly_table)


# %% [markdown]
# ## add a column corresponding to the month

# %%
def find_month(row):
    the_month=row.name.month
    row['month'] = int(the_month)
    row['dates']=row.name
    return row

new_df = avg_df_ssp585.apply(find_month,axis=1)

new_df.head()


# %% [markdown]
# ## groupby on months 1-12

# %%
the_groups=new_df.groupby('month')
the_groups=dict(list(the_groups))
the_groups[1.0]

# %% [markdown]
# ## plot 5 ensemble members

# %%
fig,ax=plt.subplots(1,1,figsize=(14,10))
for model in ['pr0','pr1','pr2','pr3','pr4']:
    jan_df = the_groups[1.0]
    ax.plot('dates',model,data=jan_df,label=model)
    ax.set(title='january precip for 5 members')
    ax.legend()

# %%
plt.rcParams['figure.figsize'] = (10,5)


# %%
'''
#plotting the individual runs looks messy with multiple scenarios, but could make error bars maybe or something
for i in range(members):
    plt.plot(avg_df_ssp585.index[:100], avg_df_ssp585['pr' + str(i)][:100], color="blue", alpha=0.2)
    plt.plot(avg_df_ssp245.index[:100], avg_df_ssp245['pr' + str(i)][:100], color="red", alpha=0.2)
'''

# %%
plt.plot(avg_df_ssp585.index[:100], avg_df_ssp585['mean'][:100], color="blue")
plt.plot(avg_df_ssp245.index[:100], avg_df_ssp245['mean'][:100], color="red")
plt.ylabel("precipitation (kg m-2 s-1)")
plt.title("CanESM5, ssp585 vs. ssp245, precip, "+ str(members) + " runs averaged")
plt.legend(["ssp585", "ssp245"])
plt.savefig('./plot_dir/1model-2exp-25runsavg.png')
plt.show()
