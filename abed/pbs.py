"""
Functions for working with PBS files.

Note: this pbs file depends on the `timeout` command to be available. In some 
cases (such as on LISA) it must be loaded separately through a module. This must 
be in the configuration file then.

"""

import time

from abed import settings

def generate_pbs_text():
    txt = []

    # create pbs line
    pbs_line = '#PBS -lnodes=%i' % settings.PBS_NODES
    if not settings.PBS_CPUTYPE is None:
        pbs_line += ':%s' % settings.PBS_CPUTYPE
    if not settings.PBS_CORETYPE is None:
        pbs_line += ':%s' % settings.PBS_CORETYPE
    if not settings.PBS_PPN is None:
        if isinstance(settings.PBS_PPN, int):
            pbs_line += ':ppn=%i' % settings.PBS_PPN
        else:
            pbs_line += ':%s' % settings.PPN
    pbs_line += ' -lwalltime=%s' % time.strftime('%H:%M:%S', 
            time.gmtime(settings.PBS_WALLTIME * 60.0))
    txt.append(pbs_line)
    txt.append('')

    # export variables (before loading modules!)
    for export in settings.PBS_EXPORTS:
        txt.append('export %s' % export)
    txt.append('')

    # load modules
    for module in settings.PBS_MODULES:
        txt.append('module load %s' % module)
    txt.append('')

    # current directory variable
    txt.append('CURRENT=%s/releases/current' % settings.REMOTE_PATH)
    txt.append('')

    # result dir
    txt.append('mkdir -p ${CURRENT}/results')
    txt.append('mkdir -p ${TMPDIR}/results')
    txt.append('')

    # start email
    txt.append('summary=$(abed status)')
    txt.append('echo -e "Job $PBS_JOBID started at `date`\\n\\n${summary}"'
            ' | mail $USER -s "Job $PBS_JOBID started"')
    txt.append('')

    # copy files to nodes
    cp_line = 'mpicopy ' + ' '.join(['${CURRENT}/' + x for x in 
        settings.PBS_MPICOPY])
    txt.append(cp_line)
    txt.append('')

    # calculate reduced runtime
    ttr = settings.PBS_WALLTIME * 60 - settings.PBS_TIME_REDUCE

    # run line
    txt.append('timeout %i mpiexec abed run' % ttr)
    txt.append('')

    # zip tasks
    txt.append('mkdir -p ${CURRENT}/bzips')
    txt.append('cd ${TMPDIR}/results')
    txt.append('')
    txt.append('for dset in `ls`')
    txt.append('do')
    txt.append('\tpacktime=$(date +%Y_%m_%d_%H_%M_%S)')
    txt.append('\ttar -c ${dset} | '
            'pbzip2 -vc -p14 -m1000 > ${packtime}_results_${dset}.tar.bz2')
    txt.append('\tcp ${packtime}_results_${dset}.tar.bz2 ${CURRENT}/bzips/')
    txt.append('done')
    txt.append('')

    # end email
    txt.append('echo "Job $PBS_JOBID finished at `date`" | mail $USER -s '
            '"Job $PBS_JOBID finished"')
    return '\n'.join(txt)
