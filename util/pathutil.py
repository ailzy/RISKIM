
import os

def init_dir(path):
    if os.path.exists(path):
        return False
        # os.system('rm -rf %s/*' % path)
    else:
        os.mkdir(path)
        return True