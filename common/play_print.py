import sys
from time import sleep

if __name__ == '__main__':
    for i in range(5):
        sys.stdout.write('\rPrint {0} Print {0} Print {0}'.format(i))
        # sys.stdout.write('Print {}\n'.format(i))
        # sys.stdout.write('Print {}\n'.format(i))
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write('\n')
