#/usr/bin/python
import re
import subprocess
import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def parse(line):
    pattern = "(^\w+)\s+\d+\s+(.*)$"
    m = re.search(pattern, line)
    return (m.group(1),m.group(2))

def list_folders(id):
    cmd = ["/usr/bin/python","/home/ramblurr/src/mfcli/mfcli.py", "-o", "list", "-t", "folders",  "-i", id]
    output = subprocess.check_output(cmd).strip()
    return output.split('\n')

def list_files(id):
    uri = 'http://mediafire.com/folder/%s' % (id)
    cmd = '/usr/bin/plowlist -q %s > files.lst' % (uri)
    os.system(cmd)


def visit_dir(id, name, n):
    print(" "*n*2 + "%s (%s)" % (name, id))
    mkdir_p(name)
    os.chdir(name)
    list_files(id)
    for line in list_folders(id):
        if len(line) == 0:
            continue
        id, name = parse(line)
        visit_dir(id,name, n+1)
    os.chdir(os.pardir)


primary_id = "k7qnhuh1fd2c4"
visit_dir(primary_id, "RPGs", 0)

