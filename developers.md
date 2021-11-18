## For Developers

This section of the readme provides some guidance for adding new features or fixing bugs.

### git commit hooks

If you are running into issues with the git hooks, ensure that black and flake8 aren't disagreeing on something. Flake8 issues can be introduced by the black linter. Its typically easier to change flake8's preferences rather than black's. See .flake8 in the root directory for an example how to deal with this issue.

### Repository Structure

There are a few oddities in the structure of this repo. The tests currently live in the main directory, as well as the script for creating cases. This was done so the imports of utils.py for the tests and make_case functions would play nicely together but probably should be changed at some point.

### Tests

There are tests for some of the case_util functions and some of the wrangling functions. Regression testing for the visuals and integration testing
with something like selenium for the actual dashboard code has not been implemented. You can invoke existing tests by calling: `pytest` from the main directory. I have found that TDD for any case functions or wrangling functions has saved me time hunting for bugs in the long run and would encourage expanding on these tests as you work on the codebase.

They take about 3-5 minutes to run and are far from exhaustive but are worth running if you are making changes to the wrangling or the cases code.

### A note about cases vs. developer mode

Design choices were mostly made with the idea that the dashboard would be used by students in "case" mode. The intention is that the option developer mode would be removed when the class actually uses the tool and as such the dashboard is rather brittle in developer mode. Better error handling and restricting available options to prevent incompatible input will probably required if the dashboard is to be run in production in developer mode.

### I want to...

Here are some pointers on what code to look at specifically for adding features.

#### Add support for a new model / variable / experiment:

Adding support for more of the wide and wonderful world of CMIP-6 should be fairly straight forward. A few gotchas to lookout for are dates and gridding. The plotting code in the dashboard has only been tested with the gridding used in the Lmon and Amon tables- SImon, for example, causes issues. It is worth noting that "level" for most atomospheric variables is currently ignored. Different scenarios, of course, have different dates but piControl rather charmingly does not always have the same dates between different models which can cause issues. For example, one model in our subset ran it's piControl scenario starting at year 1 and another chose to use year 6000. Most of the project code ignores the date input and just takes the last year from piControl and that has worked reasonably well so far.

Getting a new variable, model, or experiment to show up as an option in "Developer Mode" mode and to be available for a case can achieved by adding to the corresponding dict returned by either get_var_key(), get_model_key(), or get_experiment_key() along with the corresponding information.

#### Add support for a new dashboard feature:

Graphics are currently created by functions in src/plotting_utils.py and called in app.py. Dasboard features are defined as variables with descriptive names and then put together in the app initilization call to avoid very long lines. Dash is built to work natively with the python plotly library, so if it is at all possible to create the figure you are interestred in in plotly that usually makes life easier down the line. 

#### Change how cases are structured

Currently, cases can take an arbitrary number of variables and models, but are constrained to one experiment that must be valid for all models and variables. Two sets of dates may become necessary if this changes. The case creating functions live in src/case_utils.py.

#### Code directory appendix

The numbers here refer to the pictures above and provide starting points in the code base if you want to add/ modify/ debug any of the elements therein. 

Some notes on terminology: each element in dash is specified in the app. I call this code "location" here. All the interactivity happens through callbacks, which are functions that reference the id of various elements to either change what they should display or get information about user selections from them. That's what the "callback" link points to.  
1. https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L174-189
2. Dash structure code: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L193, Callback that controls interactivity: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L492
3. Scenario dropdown. Scanning cases folder for available cases happens here: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L34
5. Model variable dropdown. 
5. Model dropdown. 
6. Model comparison. 
7. Date selection.
8. Experiment dropdown. All above specified here: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L114-159. Update on model select defined in this callback: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L396
9. The heatmap. Location code: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L43, Interactivity callback: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L220. Actual plotting code specified in plot_utils.py by plot_year_plotly(): https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/src/plot_utils.py#L26
10. Comparison histogram: location: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L72 callback:https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L323 plot_utils specs: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/src/plot_utils.py#L124
11. Typo- if you're seeing this I ran out of time writing the docs. Sorry!
12. The mean climatology member comparison plot location: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L88 callback: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L279 plot_utils specs: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/src/plot_utils.py#L177
13. Mean card loaction: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L147 callback: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L443
14. Std dev card- same as above, but for standard deviation. https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L150 callback: https://github.com/JacobMcFarlane/cmpi_6_dash/blob/master/app.py#L468

