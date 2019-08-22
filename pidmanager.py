import os, sys, psutil, logging, fcntl

'''
This class implemenets a lightweight PID file constructor/destructor for
programs that already have build-in signalling for graceful startup and
shutdown.

All of the ones I looked at before writing this want to use a with.... to open
the file and then place the entire program inside it. Yuk. I wanted to add
this to a really robust program that already understood graceful shutdown.

While it's written as OO, it's really intended to be used once per program.

Calling the class constructor with a pidfile name 'pidname' without .pid at
the end and a path, without a trailing / -- like this:

    mypid = PID_MANAGER(name='myprog', path='/var/run')

will cause '/var/run/myprog.pid' to be created. Note you have to make a
reference to the class isntance beause you'll need it to kill the PID file
later on, which you'd do like this:

    mypid.remove()

This implementation does some neat things on starup. First it looks for a
file with the correct path/name. If it finds one, it checkes the PID inside
and then tests to see if such a PID actually exists on the system. If it does
not, then it assumes that it's a stale file, deletes it, and continues.

Likewise if it finds a file but cannot convert the contents into an integer,
the program assumes somethign not right happened, deletes is, and continues.

So maybe not the best overall solution, but works well for my particular needs.

'''

class PID_MANAGER(object):
    __slots__ = ('pid', 'filepath', 'pidname', 'pidpath', 'logger', 'file')

    def __init__(self, name='python', path='.'):
        self.filepath = path + '/' + name + '.pid'
        self.logger = logging.getLogger('PID_MANAGER')
        self.pid = os.getpid()
        self.file = None
        
    def create(self):
        self.check()
        
        try:
            self.file = open(self.filepath, 'w')
        except PermissionError:
            self.logger.error('PID file exists and we cannot modify it (permission error()')
            sys.exit('Permission Error accessing PID file')
            
        self.file.write(str(self.pid))
        self.file.flush()
        fcntl.lockf(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.logger.warning('PID file created and locked for process ID {} at \"{}\"'.format(self.pid,self.filepath))
            
        
    def check(self):
        if os.path.isfile(self.filepath):
            try:
                with open(self.filepath, 'r') as file:
                    try:
                        old_pid = int(file.read())
                        valid = psutil.pid_exists(old_pid)
                    
                        if old_pid and valid:
                            self.logger.error('TERMINATING: Valid Process ID (PID) {} exists in the configured PID File \"{}\". If this is an error, remove it manually!'.format(old_pid, self.filepath))
                            sys.exit('Valid Process ID (PID) {} exists in the configured PID File \"{}\". If this is an error, remove it manually!'.format(old_pid, self.filepath))
                    
                        if old_pid and not valid:
                            self.logger.warning('PID file already exists but no match found for PID {}; assuming it\'s safe to delete'.format(old_pid))
                            os.remove(self.filepath)
                
                    except ValueError:
                        self.logger.warning('PID file exists, but does not contain PID data; assuming it\'s safe to delete')
                        os.remove(self.filepath)
            except PermissionError:
                self.logger.error('PID file exists and we cannot modify it (permission error()')
                sys.exit('Permission Error accessing PID file')
        else:
            self.logger.debug('no PID file found with the given name and path, assume we are good to go')
            return False
        
    def remove(self):
        self.logger.info('PID file unlocked and deleted for process ID {} at \"{}\"'.format(self.pid,self.filepath))
        fcntl.lockf(self.file, fcntl.LOCK_UN)
        os.remove(self.filepath)


if __name__ == '__main__': 
    from time import sleep
    logging.basicConfig(level=logging.DEBUG)
    
    pidfile = PID_MANAGER(name='pythonic', path='/tmp')
    pidfile.create()
    sleep(10)
    pidfile.remove()
