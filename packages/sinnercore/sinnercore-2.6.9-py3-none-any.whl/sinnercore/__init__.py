import importlib.util
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

pyc_path = os.path.join(script_dir, "__SinnerMurphy__.pyc")

if not os.path.exists(pyc_path):
    raise FileNotFoundError(f"❌ No compiled `__SinnerMurphy__.pyc` found in {script_dir}!")

spec = importlib.util.spec_from_file_location("__SinnerMurphy__", pyc_path)
SinnerMurphy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SinnerMurphy)

SinnerFreeSelfbot = SinnerMurphy.SinnerFreeSelfbot

# Module Metadata
__version__ = "2.6.9"
__release_date__ = "2025-02-27"
__author__ = "Sinner Murphy"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 Sinner Murphy"