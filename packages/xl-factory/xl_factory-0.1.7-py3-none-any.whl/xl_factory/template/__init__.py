import os 
import copier


def copy(folder, dst_path, data=None):
    copier.run_copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), folder), dst_path, data)

def copy_module(dst_path, data=None):
    copy('module', dst_path, data)

def copy_resource(dst_path, data=None):
    copy('resource', dst_path, data)

def copy_project(dst_path, data=None):
    copy('project', dst_path, data)
