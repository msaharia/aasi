
# coding: utf-8

# In[166]:


import os, shutil
import subprocess
import glob


# In[2]:


# Directories
masterdir = '/glade/p/work/manab/ff/islandpark/'
logdname = 'log'
jobdname = 'joblists'
pbsdname = 'pbsscripts'

#FUSE
fuseexe = '/glade/p/work/manab/ff/newfuse/fuse/bin/fuse.exe'
configtpl = '/glade/p/work/manab/ff/islandpark/fm_sacsma.txt' #Main Config template
inputInfoTpl = '/glade/p/work/manab/ff/islandpark/settings/template_input_info.txt'  #Input info template
forcdir = '/glade/p/work/manab/ff/islandpark/inputnew'
fusemode = 'run_def'   #Options
simstarttime = '2017'
simendtime = '2017'
evalstarttime = '2017'
evalendtime = '2017'


# In[3]:


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

#def configFile(file):
#    '''
#    Writes config files for each ensemble run
#    '''
#    with open(file, "rt") as fin:
#        with open('/glade/p/work/manab/ff/islandpark/fm_template2.txt', "wt") as fout:
#            for line in fin:
#                print(line)
#                fout.write(line.replace('SIMSTART', simstarttime)
 
def forcingFiles(folder):
    '''
    Find all forcing files for each input
    '''
    files = glob.glob(folder + '/*nc')
    files = [x for x in files if "elev_bands" not in x]
    return(files)


# In[169]:


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
        outfile = os.path.join(os.path.split(inputInfoTpl)[0], outfilename2 + '_input_info.txt') 
        out1.append(outfilename1)
        out2.append(outfilename2)
        out3.append(outfile)
        
        runcomx = [fuseexe, configtpl, outfilename2, '001', fusemode]
        runcomx = " ".join(runcomx)
        
        runcoms.append(runcomx)

        with open('/glade/p/work/manab/ff/islandpark/settings/template_input_info.txt', "rt") as fin:
            with open(outfile, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('FORCTEMP', outfilename1))
    
        #Create joblist
        
        
        for x,y in enumerate(range(0, len(runcoms), 36)):
            jobchunk = runcoms[y : y + 36]
    
            with open(os.path.join(jobdir, str(x)), "wt") as fout:
                for item in jobchunk:
                    fout.write("{}\n".format(item))


# In[191]:




