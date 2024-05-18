
import fcntl
import os




class FileLock():

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.file = None
        self.is_locked = False
        

    def __enter__(self, *args, **kwargs):
        self.file = open(self.path, 'w')
        self.acquire()
        self.is_locked = True
        return True


    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.file.flush()
        os.fsync(self.file.fileno() )
        self.release()
        self.is_locked = False
        self.file.close()
        self.file = None
        if exc_type != None:
            return False
        return True  


    def acquire(self):
        if self.file.writable():
            fcntl.lockf(self.file, fcntl.LOCK_EX)


    def release(self):
        if self.file.writable():
            fcntl.lockf(self.file, fcntl.LOCK_UN)


    def is_locked(self):
        return self.is_locked