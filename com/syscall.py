import os
import sys

import log


def syscall(command='', Async=False):
    if Async == False:
        return os.popen(command).readlines()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(syscall(sys.argv[1]))
