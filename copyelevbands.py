import glob, os
from shutil import copyfile

forcdir = '/glade/p/work/manab/ff/islandpark/inputnew'
elevfile = '/glade/p/work/manab/ff/islandpark/ip_elev_bands_usbr.nc'

forcfiles = glob.glob(forcdir + '/*nc')
forcfiles = [x for x in forcfiles if "elev_bands" not in x]
forcfiles = sorted(forcfiles)

for count, value in enumerate(forcfiles):
    outfile = os.path.join(forcdir, os.path.basename(value).split('.')[0] + '_elev_bands.nc')
    copyfile(elevfile, outfile)
