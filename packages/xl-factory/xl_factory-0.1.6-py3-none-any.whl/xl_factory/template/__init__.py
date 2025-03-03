import os 
import copier


def copy(dst_path, data=None):
    copier.run_copy(os.path.dirname(os.path.abspath(__file__)), dst_path, data)

def copy_module(dst_path, data=None):
    copy(os.path.join(dst_path, 'module'), data)

def copy_resource(dst_path, data=None):
    copy(os.path.join(dst_path, 'resource'), data)

def copy_project(dst_path, data=None):
    copy(os.path.join(dst_path, 'project'), data)
