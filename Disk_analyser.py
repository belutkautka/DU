from progress.bar import IncrementalBar
from pathlib import Path
from Fail import Fail
from threading import Thread,Lock


class Disk_analyser:
    def __init__(self, path: Path, level, ext, print, dates, unread, owners):
        self.path = path
        self.lock = Lock()
        self.deep = []
        self.dates = dates
        self.extensions = ext
        self.mass = 0
        self.level = level
        self.files = []
        self.unread = unread
        self.unread_dir = []
        self.print = print
        self.owners = owners
        self.analyse(path, 1)



    def analyse_quit(self, path: Path, level):
        if not path.is_dir():
            print(f"Введите директорию, а не {path}")
            exit()
        try:
            fails = list(path.iterdir())
        except:
            self.unread_dir.append(path)
            return
        for fail in fails:
            f = Path(str(path), fail)
            if f.is_dir():
                if level < self.level:
                    self.analyse_quit(f, level + 1)
            else:
                fl = Fail(f, level)
                if self.is_right_ext(f) and self.is_right_time(fl) and self.is_right_owner(fl):
                    self.files.append(fl)



    def is_right_ext(self, f):
        if self.extensions != None:
            if f.suffix in self.extensions:
                return True
            return False
        else:
            return True

    def is_right_time(self, f):
        if self.dates != None:
            if f.time in self.dates:
                return True
            return False
        else:
            return True

    def is_right_owner(self, f):
        if self.owners != None:
            if f.owner in self.owners:
                return True
            return False
        else:
            return True

    def analyse(self, path, level):
        self.analyse_quit(path, level)
        bar = IncrementalBar('Analyse', max=len(self.files))
        threads=[]
        for item in self.files:
                thread=Thread(target=self.size,args=(item,bar))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
        bar.finish()
    def size(self,fail,bar):
        fail.size()
        self.lock.acquire()
        bar.next()
        self.mass += fail._size
        self.lock.release()


    def print_results(self):
        if self.print:
            for file in self.files:
                print(file._size, file.path, file.time)

        if len(self.unread_dir) > 0:
            print("Некоторые директории не удалось посчитать")
        if self.unread:
            for file in self.unread_dir:
                print(file)
        print(f"Total: {self.mass} bytes")