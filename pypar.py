#===============================================================================
## \file pypar.py
# \brief
# Examples of parallel Python
# \author
# Marc Joos <marc.joos@gmail.com>
# \copyright
# Copyrights 2015, Marc Joos.
# This file is distributed under the CeCILL-A & GNU/GPL licenses, see
# <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html> and
# <http://www.gnu.org/licenses/>
# \date
# \b created: 02-19-2015
# \b last \b modified: 02-19-2015
#===============================================================================
#!/usr/bin/env python
import os
import argparse
import multiprocessing as mp
from mpi4py import MPI

# Simple example
#===============================================================================
def doSomething(wdir='./'):
    print('working on process: %d' %os.getpid())
    print(os.listdir(wdir))
    

def launchSimple(listdir=('./', '../',)):
    for wdir in listdir:
        # Create processes
        p = mp.Process(target=doSomething, args=(wdir,))
        # Launch processes
        p.start()
        # Wait until processes terminate
        p.join()

# Example with queues
#===============================================================================
def doItInQueue(q, wdir='./'):
    print('working on process: %d' %os.getpid())
    q.put(os.listdir(wdir))
    
def launchQueue(listdir=('./', '../',)):
    # Create queue
    q = mp.Queue()
    result = []
    for wdir in listdir:
        # Create processes
        p = mp.Process(target=doItInQueue, args=(q, wdir))
        # Launch processes
        p.start()
        # Wait until processes terminate
        p.join()
        # Get results
        result.append(q.get())
    return result

# Example with pools
#===============================================================================
def doItInPool(wdir='./'):
    print('working on process: %d' %os.getpid())
    return os.listdir(wdir)

def launchPool(listdir=['./', '../']):
    # Get number of CPU available and define the number of processes
    nproc  = mp.cpu_count()*2
    # Create pool
    pool   = mp.Pool(processes=nproc)
    # Distribute the work among processes
    result = pool.map(doItInPool, listdir)
    return result

# Example with workers
#===============================================================================
def dotItWithWorker(tasks, results):
    for i, task in iter(tasks.get, 'STOP'):
        results.put((i, os.getpid(), os.listdir(task)))
    
def launchWorker(listdir=['./', '../']):
    # Get number of CPU available and define the number of processes
    nproc   = mp.cpu_count()*2
    # Create queues
    tasks   = mp.Queue()
    results = mp.Queue()

    # Create list of tasks
    for i, out in enumerate(listdir):
        tasks.put((i, out))

    # Distribute the work among processes
    for i in xrange(nproc-1):
        p = mp.Process(target=doItWithWorker, args=(tasks, results))
        p.start()

    # Tell processes to stop when they are done
    for i in xrange(nproc-1):
        tasks.put('STOP')
    
    # Gather results
    result = []
    for i in xrange(len(listdir)):
        j, pid, res = results.get()
        print('Task #%02d was done on process #%d' %(j,pid))
        result.append(res)

    return result

# Example with MPI
#===============================================================================
def launchMPI(listdir=['./', '../']):
    # Initialize MPI creating COMM_WORLD communicator
    comm = MPI.COMM_WORLD
    # Get size of the MPI domain and rank of the process
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # Distribute work among MPI processes
    nfp = len(listdir)/size
    for i in xrange(nfp+1):
        idx = i*size + rank
        print('working on process: %d with PID: %d' %(rank,os.getpid()))
        if idx < len(listdir):
            print(os.listdir(listdir[idx]))
        else:
            print('Nothing to be done.')

# Main program
#===============================================================================
def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--with-mpi', '-m', dest='mpi', action='store_true' \
                            , help='to launch MPI test')
    args = parser.parse_args()

    mpi = args.mpi
    if mpi: launchMPI()

if __name__ == '__main__':
    main()
