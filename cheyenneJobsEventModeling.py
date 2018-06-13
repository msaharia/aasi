#!/usr/bin/env python
# change the modelmode
import os, shutil
import subprocess
import glob

# Change these
modelmode = '444' #PRMS -111, HECHMS-222, VIC-333, SACSMA-444
configtpl = '/glade/p/work/manab/ff/islandpark/em_sacsma.txt' #Main Config template

# Directories
masterdir = '/glade/p/work/manab/ff/islandpark/'
logdname = 'log10K'
jobdname = 'job10K'
pbsdname = 'pbs10K'
pbstemplate = 'template_pbs.txt'
inputinfoout = 'forcing10Kinfo'

#FUSE
fuseexe = '/glade/p/work/manab/ff/newfuse/fuse/bin/fuse.exe'
inputInfoTpl = '/glade/p/work/manab/ff/islandpark/settings/template_input_info.txt'  #Input info template
forcdir = '/glade/p/work/manab/ff/islandpark/precip_event_forcing'
fusemode = 'run_def'   #Options: run_def for simulation and calib_sce for ALL simulations


def concatDir(dir, subdir):
    '''
    Concatenates Master dir and another dname (directory name)
    '''
    newdir = dir + subdir
    return(newdir)

def purgeDir(folder):
    '''
    Purges contents of a directory
    '''

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def forcingFiles(folder):
    '''
    Find all forcing files for each input
    '''
    files = glob.glob(folder + '/*nc')
    files = [x for x in files if "elev_bands" not in x]
    return(files)

if __name__ == '__main__':
    logdir = concatDir(masterdir, logdname)
    jobdir = concatDir(masterdir, jobdname)
    pbsdir = concatDir(masterdir, pbsdname)
    
    purgeDir(logdir)      #Empty, if not.
    purgeDir(jobdir)
    purgeDir(pbsdir)
    
    forcfiles = sorted(forcingFiles(forcdir))
    
    #Create input info files
    out1 = []
    out2 = []
    out3 = []
    runcoms = []
    for count, value in enumerate(forcfiles):
        outfilename1 = os.path.basename(value)     #001.nc
        outfilename2 = outfilename1.split('.')[0]   #001    
        outfile = os.path.join(os.path.split(inputInfoTpl)[0], inputinfoout, outfilename2 + '_input_info.txt') 
        out1.append(outfilename1)
        out2.append(outfilename2)
        out3.append(outfile)
        
        runcomx = [fuseexe, configtpl, outfilename2, modelmode, fusemode]
        runcomx = " ".join(runcomx)
        
        runcoms.append(runcomx)
        
       # Create input info files
       # with open(inputInfoTpl, "rt") as fin:
       #     with open(outfile, "wt") as fout:
       #         for line in fin:
       #             fout.write(line.replace('FORCTEMP', outfilename1))
    
    #Create joblist
    for x,y in enumerate(range(0, len(runcoms), 36)):
        jobchunk = runcoms[y : y + 36]
        with open(os.path.join(jobdir, str(x)), "wt") as fout:
            for item in jobchunk:
                fout.write("{}\n".format(item))

    #Create pbs scripts
    jobx = sorted(os.listdir(jobdir), key=int)
    for ajob in jobx:
        job_file_path = os.path.join(jobdir, ajob)
        pbsoutname = os.path.join(pbsdir, ajob + '.sh')
        print(pbsoutname)
        print(job_file_path)

        with open(pbstemplate, "rt") as fin:
            with open(pbsoutname, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('LOGNUMBER', str(ajob)).
                            replace('JOBLIST', job_file_path))




