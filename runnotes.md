`source activate ff` for flood frequency conda environment
***

# Current Issues
- [ ] Why isnt SAC-SMA capturing almost 20-30% runoff?
- [ ] Why is FUSE-PRMS way off-base?

# Prepare FUSE
* Compile SCE: `ifort -O2 -c -fixed sce_16plus.f`
* `mkdir bin`
* `make`

# Forcing generation
* Create a mapping file
    * Go to `/d3/msaharia/ffreq/forcinggeneration` in Hydro-c1 server
    * `python2.7 poly2poly/poly2poly.py /d3/msaharia/ffreq/forcinggeneration/pilot_basin_data/IslandPark_WatershedDelineation.gpkg Id PNW/PNW_elev_0625_poly2.gpkg id GRID map.nc`
* Create a time series file using this `mapping file`
    * Go to `/d3/msaharia/ffreq/forcinggeneration` 
    * `python2.7 poly2poly.map_timeseries.py ../islandpark.nc /d3/hydrofcst/overtheloop/data/forcing/retro/forc_nc/PNW/ens_forc.PNW.0625.1980-1989.051.nc ../testme.nc`
* Create time series polygon files for all 100 ensembles: `/d3/msaharia/ffreq/aasi/hydrometEnsGen.py`

# Forcing manipulation
* Move time series data created above to Cheyenne: `scp -r /d3/msaharia/ffreq/forcinggeneration/islandpark/* manab@cheyenne.ucar.edu:/glade/p/work/manab/ff/islandpark/rawinput/`
* Concatenates by time for each ensemble, inserts PET in each ensemble, and writes out final input files: `/d3/msaharia/ffreq/aasi/convert4fuse.ipynb`

# Elevation bands
* <del>Temporarily use this: `https://github.com/msaharia/aasi/blob/master/temporaryCopyElevBanFile.py` </del>
* Use real elevation bands provided by USBR here: `/glade/p/work/manab/ff/islandpark/ip_elev_bands_usbr.nc`

# Model Configurations
| FUSE configuration                    | PRMS                                                               | HECHMS                                                             | VIC                                                             | SACSMA                                                          |
| ------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------- | --------------------------------------------------------------- |
| rainfall error                        | multiplicative rainfall error (multiplc_e)                         | multiplicative rainfall error (multiplc_e)                         | multiplicative rainfall error (multiplc_e)                      | multiplicative rainfall error (multiplc_e)                      |
| upper-layer architecture              | tension storage sub-divided into recharge and excess (tension2_1)  | upper layer broken  into tension and free storage (tension1_1)     |  single state var (onestate_1)                                  | upper layer broken  into tension and free storage (tension1_1)  |
| lower-layer architecture and baseflow | baseflow resvr of unlimited size (0-HUGE), frac rate (unlimfrc_2)  | baseflow resvr of unlimited size (0-HUGE), frac rate (unlimfrc_2)  | baseflow reservoir of fixed size (fixedsiz_2)                   | tension reservoir plus two parallel tanks (tens2pll_2)          |
| surface runoff                        | PRMS variant (fraction of upper tension storage) (prms_varnt)      | ARNO/Xzang/VIC parameterization (arno_x_vic)                       | ARNO/Xzang/VIC parameterization (arno_x_vic)                    | PRMS variant (fraction of upper tension storage) (prms_varnt)   |
| percolation                           | water from (field cap to sat) avail for percolation (perc_f2sat)   | water from (field cap to sat) avail for percolation (perc_f2sat)   | water from (wilt pt to sat) avail for percolation (perc_w2sat)  | perc defined by moisture content in lower layer (perc_lower)    |
| evaporation                           | root weighting (rootweight)                                        | sequential evaporation model (sequential)                          | root weighting (rootweight)                                     | sequential evaporation model (sequential)                       |
| interflow                             | interflow (intflwsome)                                             | no interflow (intflwnone)                                          | no interflow (intflwnone)                                       | interflow (intflwsome)                                          |
|  time delay in runoff                 | Gamma distribution with shape parameter = 2.5 (rout_gamma)         | Gamma distribution with shape parameter = 2.5 (rout_gamma)         | Gamma distribution with shape parameter = 2.5 (rout_gamma)      | Gamma distribution with shape parameter = 2.5 (rout_gamma)      |
| snow model                            | temp_index                                                         | temp_index                                                         | temp_index                                                      | temp_index                                                      |


# Running FUSE
* `./bin/fuse.exe /glade/p/work/manab/ff/islandpark/fm_902_us.txt islandpark 123 run_def`
    * 2nd CLI arg: `dom_id`. This dictates which `input_info` file it looks for inside `/settings/`. For example, this will look for `islandpark_input_info.txt`
    * 3rd CLI arg: `FMODEL_ID`. This dictates what decision file FUSE looks for. i.e. `/glade/p/work/manab/ff/islandpark/settings/fuse_zDecisions_123.txt`
* Things I will need templates for automated runs:
    * Main config file with TIME insertions
    * Creating `x_input_info.txt` in settings file with forcing file name insertion and filename change
* Works: `./bin/fuse.exe /glade/p/work/manab/ff/islandpark/fm_template.txt islandpark 001 run_def`
* Run 100 ensembles using: and then `https://github.com/msaharia/aasi/blob/master/cheyenneJobs.ipynb`
* ./submitalljobs.sh (for now)

# 100 ensemble runs - Calibration
* Joblists: `/gpfs/fs1/work/manab/ff/islandpark/joblists`
* Config files: `/gpfs/fs1/work/manab/ff/islandpark/fm_*_kge.txt`
* Submit calib_sce runs:  `/gpfs/fs1/work/manab/ff/islandpark/submitallcalibpbsjobs.sh`
* New output stored here: `/gpfs/fs1/work/manab/ff/islandpark/allout/calib100`
* Run final with best calibrated parameter set: `/gpfs/fs1/work/manab/ff/islandpark/calib100.bash`
* The calibrated results are plotted here: `https://github.com/msaharia/aasi/blob/master/2_calibrationresults.ipynb`
* The calibrated parameter sets for all the models are plotted here: `https://github.com/msaharia/aasi/blob/master/3_plotParameters.ipynb`

# Event Modeling
* To be run with 5000 precip events (dry/past precip) and a calibrated parameter set from the prvious 100 ensemble run
* 

# DELSA

# Notes
* Here, `123` dictates what decision file FUSE looks for. i.e. `/glade/p/work/manab/ff/islandpark/settings/fuse_zDecisions_003.txt`. I think it just ignores the `'fuse_zDecisions_902.txt'        ! M_DECISIONS = definition of model decisions` in the main config file
* The new setup from Andy Newman is kept in `fusenew`



