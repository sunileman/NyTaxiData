#!/usr/bin/env python

import os
import sys

children = {}
maxjobs = 8                 # maximum number of concurrent jobs
jobs = []                   # current list of queued jobs

# Default wget options to use for downloading each URL
wget = ["wget", "-q", "-nd", "-np", "-c", "-r"]

# Spawn a new child from jobs[] and record it in children{} using
# its PID as a key.
def spawn(cmd, *args):
    argv = [cmd] + list(args)
    pid = None
    try:
        pid = os.spawnlp(os.P_NOWAIT, cmd, *argv)
        children[pid] = {'pid': pid, 'cmd': argv}
    except Exception, inst:
        print "'%s': %s" % ("\x20".join(argv), str(inst))
    print "spawned pid %d of nproc=%d njobs=%d for '%s'" % \
        (pid, len(children), len(jobs), "\x20".join(argv))
    return pid

if __name__ == "__main__":
    # Build a list of wget jobs, one for each URL in our input file(s).
    for fname in sys.argv[1:]:
        try:
            for u in file(fname).readlines():
                cmd = wget + [u.strip('\r\n')]
                jobs.append(cmd)
        except IOError:
            pass
    print "%d wget jobs queued" % len(jobs)

    # Spawn at most maxjobs in parallel.
    while len(jobs) > 0 and len(children) < maxjobs:
        cmd = jobs[0]
        if spawn(*cmd):
            del jobs[0]
    print "%d jobs spawned" % len(children)

    # Watch for dying children and keep spawning new jobs while
    # we have them, in an effort to keep <= maxjobs children active.
    while len(jobs) > 0 or len(children):
        (pid, status) = os.wait()
        print "pid %d exited. status=%d, nproc=%d, njobs=%d, cmd=%s" % \
            (pid, status, len(children) - 1, len(jobs), \
             "\x20".join(children[pid]['cmd']))
        del children[pid]
        if len(children) < maxjobs and len(jobs):
            cmd = jobs[0]
            if spawn(*cmd):
                del jobs[0]
