import shutil
import glob
import os
import pathlib
from ...template import root_exclude
from .base import DataMediumBase
from ...errors import Abort

class Local(DataMediumBase):

    def __init__(self, root):
        self.root = self.get_absolute_as_Path(root)

    @staticmethod
    def exists(path):
        return path.exists()

    @staticmethod
    def joinpath(path1, *pathN):
        return path1.joinpath(*pathN)

    @staticmethod
    def mkdir(target):
        target.mkdir(parents=True)
        #os.makedirs(str(target_path))

    @staticmethod
    def write_text(target, content):
        target.write_text(content)

    @staticmethod
    def write_bytes(target, content):
        target.write_bytes(content)

    @staticmethod
    def read_text(source):
        return source.read_text()

    @staticmethod
    def read_bytes(source):
        return source.read_bytes()

    @staticmethod
    def copy(source, target):
        shutil.copy(source, target)

    def acquire(self):
        pass # TODO: make sure filesystem is mounted

    def release(self):
        pass # TODO:
        # make sure filesystem is unmounted if it was not already
        # mounted

    def ensure_source(self):
        if not self.root.is_dir():
            raise Abort("Source %s does not exists" % self.root)

    def ensure_target(self):
        if self.root.is_dir():
            raise Abort("Target %s already exists" % self.root)

    @staticmethod
    def iter_filenames(source):
        """
            Walk through all files and yield one of the following:

            * (1, rootdir, dirname, None)
            * (2, rootdir, dirname, filename)

            Usage:

            .. code-block:: python

                for action, root, dn, fn in iter_filenames(some_dir):
                    if action == 1:
                        print("I am {root}/{dn}, the directory)
                    elif action == 2:
                        print("I am not")
        """

        root_index = len(str(source)) + 1

        exclude = []
        for exc in root_exclude:
            exclude.extend(glob.glob(str(source.joinpath(exc))))

        for full_root, _dirs, files in os.walk(str(source)):
            root = full_root[root_index:]
            skip = False
            for exc in exclude:
                if full_root.startswith(exc):
                    skip = True
            if not skip:
                yield 1, root, None
                for fn in files:
                    yield 2, root, fn