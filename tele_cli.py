import sys
from service.utils import make_interface
from subprocess import Popen, PIPE, STDOUT

def run_command(cmd):
    iface = make_interface()

    p = Popen(cmd, stderr=STDOUT, shell=True)
    iface.add_process(p.pid, cmd)
    output, errors = p.communicate()
    iface.update_process(p.pid, p.returncode)


def main():
    if sys.argv[1:] == ['--exit-service']:
        iface.Exit()
    run_command(' '.join(sys.argv[1:]))


if __name__ == '__main__':
    main()
