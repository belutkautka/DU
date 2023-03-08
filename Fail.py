import datetime
from pathlib import Path
import win32security
from sys import platform
import os


class Fail:
    def __init__(self, path: Path, level):
        self.path = path
        self.ext = path.suffix
        self.level = level
        self._size = 0
        try:
            self.time = datetime.datetime.fromtimestamp(path.stat().st_mtime).date()
        except:
            self.time = None

        self.owner = self.find_owner()

    def size(self):
        try:
            with open(self.path, "rb") as f:
                self._size = len(f.read())
        except:
            self._size = self.path.stat().st_size
        return self._size

    def find_owner(self):
        if platform == "win32":
            try:
                sd = win32security.GetFileSecurity(str(self.path), win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                owner, domain, type = win32security.LookupAccountSid(None, owner_sid)
                return owner
            except:
                return ""
        return ""
