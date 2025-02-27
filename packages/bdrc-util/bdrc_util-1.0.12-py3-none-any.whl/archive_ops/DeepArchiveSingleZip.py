"""
Builds a bdrc bag from a list of file paths, assumed to be under a parent path.
"""
import os
import shutil
import tempfile
import bdrc_bag.bag_ops as bag_ops


def zip_loose_deep_archive(files, parent, zipname):

    # Bdrc bag only works on complete directories. Make a temporary
    # directory for the bag source
    with tempfile.TemporaryDirectory() as tmpdir:
        for f in files:
            shutil.copy(os.path.join(parent, f), tmpdir)
        bag_ops.bag(tmpdir)

    with zipfile.ZipFile(zipname, 'w') as z:
        for f in files:
            z.write(os.path.join(parent, f), f)
