"""
Functions for working with PBS files

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

    # current directory variable
    txt.append('CURRENT=%s/releases/current' % settings.REMOTE_PATH)

    # result dir
    txt.append('mkdir -p ${TMPDIR}/results')

    # start email
    txt.append('summary=$(abed status)')
    txt.append('echo -e "Job $PBS_JOBID started at `date`\\n\\n${summary}"'
            ' | mail $USER -s "Job $PBS_JOBID started"')

    # load modules
    for module in settings.PBS_MODULES:
        txt.append('module load %s' % module)

    # copy files to nodes
    cp_line = 'mpicopy ' + ' '.join(['${CURRENT}/' + x for x in 
        settings.PBS_MPICOPY])
    txt.append(cp_line)

    # reduce time to run
    txt.append('(( timetorun = ${SARA_BATCH_WALLTIME} - %i ))' % 
            settings.PBS_TIME_REDUCE)

    # run line
    txt.append('timeout ${timetorun} mpiexec abed run')

    # zip tasks
    txt.append('mkdir -p ${CURRENT}/bzips')
    txt.append('cd ${TMPDIR}/results')
    txt.append('for dset in `ls`')
    txt.append('do')
    txt.append('packtime=$(date +%Y_%m_%d_H_%M_%S)')
    txt.append('tar -c ${dset} | '
            'pbzip2 -vc -p14 -m1000 > ${packtime}_results_${dset}.tar.bz2')
    txt.append('cp ${packtime}_results_${dset}.tar.bz2 ${CURRENT}/bzips/')
    txt.append('done')

    # end email
    txt.append('echo "Job $PBS_JOBID finished at `date`" | mail $USER -s '
            '"Job $PBS_JOBID finished"')
    return '\n'.join(txt)
