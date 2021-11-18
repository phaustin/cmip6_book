## Dashboard Rundown
![Dash Landing Page](docs/CMIP_6_heatmap_numbered.png)
![Dash Comaprison Hist Page](docs/CMIP_6_probability_density_comparison_nums.png)
![Dash Member_Comparisons](docs/CMIP_6_member_comparison_nums.png)

1. The header. 
2. The tabs. Selecting climate map displays the heatmap, selecting compare displays the model amd member comaprisons.
3. Scenario dropdown. Allows for selecting the given json case specification or Developer Mode in which all fetching of data happens live (useful for testing out dashboard features / new combos but very slow as of now). Selecting a scenario changes the available models, experiments, and variables and switches to reading from prewritten netCDF files for subsets of the globe (much much faster).
5. Model variable dropdown. Specifies variable to plot. This is the model plotted in all three displays.
5. Model dropdown. Specifies main model to plot. This is the model plotted in all three displays.
6. Model comparison. Speciifies which model the main model should be compared to specifically in the comparison hists.
7. Date selection. This date input specified in YYYY/MM format determines which month of data from which year should be plotted in the comparison histograms and the heatmap. It is ignored by the member comparison line chart which simply plots the members behaviour across the whole time span of the scenario or defaults to a year and a half in dev mode. Inputing a date not in the range of the selected experiment will result in the graphs not updating and an error being logged. The value is set to the start of the scenario when a new scenario is selected.
8. Experiment dropdown. This input specifies which experiment is selected. Currently not all that useful for "case mode" since each case can only have one experiment, but nice to have for developer mode or if multiple experiments per case is implemented in the future.
9. The heatmap. This plot displays a heatmap of the model run for the given year and month, variable, and experiment.
10. Comparison histogram: this plot shows a probability distribution of variable values for two models for the same month of a specified year in a given experimental run. 
11. Typo- if you're seeing this I ran out of time writing the docs. Sorry!
12. The mean climatology member comparison plot. This plot takes the mean of the variable for each month and year across the specified area of the case and plots it for each member downloaded for the model in the case. Currently disregards date as previously described, although the base plotly interactivity means you can zoom into a particular date range should you feel so inclined.
13. Mean card- this card displays the mean of the area selected on the heatmap. Note that the selection and zoom tools look fairly similar, so make sure you are using "box select" or "lasso select" (names available on the toolbar if you hover) if you can't get this feature to work.
14. Std dev card- same as above, but for standard deviation.