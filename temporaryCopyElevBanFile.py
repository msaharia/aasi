# Temporarily creates copies of elevation band files. Will be subsumed in main file and deleted eventually.

import glob, os
from shutil import copyfile

forcdir = '/glade/p/work/manab/ff/islandpark/inputnew'
forcfiles = glob.glob(forcdir + '/*nc')
forcfiles = [x for x in forcfiles if "elev_bands" not in x]
forcfiles = sorted(forcfiles)
elevfile = '/glade/p/work/manab/ff/islandpark/inputnew/islandpark_elev_bands.nc'

for count, value in enumerate(forcfiles):
    outfile = os.path.join(forcdir, os.path.basename(value).split('.')[0] + '_elev_bands.nc')
    copyfile(elevfile, outfile)
