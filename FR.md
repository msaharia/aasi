# Uncertainty partition 

A primer for partioning uncertainty in flood frequency estimates arising from three sources: forcing, parameters, and model structures.

## Target
* Precip growth curve distribution (?)
* Perturbed initial conditions 
* Model structures (10)
* Parameter sets (100 calibrated sets)
* ANOVA

## Multi-model structures
10 FUSE model structures are finalized.

![Configurations](./modelconfigs.png)

## Calibration (100 ens, 10 models):

* New set-up is here: `/glade/work/manab/ff/1_calib`
* Job list and submission creation script: `0_createjobs.py`
    * Needs to be changed to `calib_sce` and then to `run_best` 
* Job submission: `1_qsubmit.sh` 

## Calibration results
* FDCs, yearly maxes, KGE distributions, and time series plots: [Notebook](6_multimodel_calibresults.ipynb)
* Parameter distribution for different models: [Notebook](7_plotParameters.ipynb)

## Parameter list
This is a list of all parameters in FUSE and temporary names used by scripts to perturb them

|Parameter Name | Alias   |
|---------------|---------|
| RFERR_ADD     |         |
| RFERR_MLT     |TEMPRFMLT|
| RFH1_MEAN     |         |
| RFH2_SDEV     |         |
| RH1P_MEAN     |         |
| RH1P_SDEV     |         |
| RH2P_MEAN     |         |
| RH2P_SDEV     |         |
| MAXWATR_1     |TEMPMAXW1|
| MAXWATR_2     |TEMPMAXW2|
| FRACTEN       |TEMPFRACT|
| FRCHZNE       |TEMPFRCHZ|
| FPRIMQB       |TEMPFPRIM|
| RTFRAC1       |TEMPFRAC1|
| PERCRTE       |TEMPPERCR|
| PERCEXP       |TEMPPERCE|
| SACPMLT       |TEMPSACPM|
| SACPEXP       |TEMPSACEX|
| PERCFRAC      |TEMPPERCF|
| FRACLOWZ      |TEMPFRACL|
| IFLWRTE       |TEMPIFLWR|
| BASERTE       |TEMPBASER|
| QB_POWR       |TEMPQBPOW|
| QB_PRMS       |TEMPQPRMS|
| QBRATE_2A     |TEMPQBR2A|
| QBRATE_2B     |TEMPQBR2B|
| SAREAMAX      |TEMPSAMAX|
| AXV_BEXP      |TEMPAXVBE|
| LOGLAMB       |TEMPLOGLA|
| TISHAPE       |TEMPTISHA|
| TIMEDELAY     |TEMPTIMED|
| MBASE         |TEMPMBASE|
| MFMAX         |TEMPMFMAX|
| MFMIN         |TEMPMFMIN|
| PXTEMP        |TEMPPTEMP|
| OPG           |TEMPOPGRA|
| LAPSE         |TEMPLAPSE|

### Number of parameters per model
|Model number   | Params  |
|---------------|---------|
|       1       |  15     |
|       2       |  17     |
|       3       |  19     |
|       4       |  17     |
|       5       |  15     |
|       6       |  20     |
|       7       |  19     |
|       8       |  18     |
|       9       |  19     |
|      10       |  16     |

## Parameter perturbation (Not reqd. currently)
* Using IQR ranges of the calibrated parameter sets, the values in the templates are replaced: `/glade/work/manab/ff/2_paramperturb/paramranges`
* The parameter file templates are here: `/glade/work/manab/ff/2_paramperturb/templates`
* The perturbation parameters are noted in the namelist: `namelist.sens.R`
* The parameter sets are generated using this `1_creates_paramsets_model1.R`
    * The complete parameter archive is stored here: `/gpfs/fs1/work/manab/ff/2_paramperturb/paramarchive`
    * The generated parameter files which will be used in further simulations are here: `/glade/work/manab/ff/2_paramperturb/paramfiles`
* *NOTE* Run all the param generation scripts using `./2_create_paramsets_allmodels.sh`

## Analysis of Variance (ANOVA)

