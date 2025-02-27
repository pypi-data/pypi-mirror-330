from solidipes.loaders.file import File

from .. import viewers


class PythonPickle(File):
    """Python Pickle file"""

    supported_mime_types = {"python/pickle": ["pkl"]}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.preferred_viewer = viewers.PythonPickle

    @File.loadable
    def obj(self):
        f = open(self.file_info.path, "rb")
        import pickle

        return pickle.load(f)
