# conftest.py

import pytest
import os
import platform

def find_ebm_library():
    """
    Return True if the EBM library is found somewhere in the expected paths.
    This can mimic the search logic from your _native.py if you wish, or 
    you can do a simpler check for 'libebm_mac_arm.dylib' on Apple Silicon, etc.
    """
    potential_paths = [
        "root/bld/lib/libebm_mac_arm.dylib",  # Apple Silicon
        "root/bld/lib/libebm_mac_x64.dylib",  # Intel mac
        "root/bld/lib/libebm_linux_x64.so",   # Linux x64
        # Add other file names/paths here if needed
    ]
    for p in potential_paths:
        if os.path.isfile(p):
            return True
    return False

ebm_present = find_ebm_library()

def pytest_collection_modifyitems(config, items):
    """
    Automatically skip EBM tests if the library isn't installed.
    This runs during test collection, skipping tests marked with @pytest.mark.ebm 
    or tests from certain files/dirs if you prefer.
    """
    if not ebm_present:
        skip_ebm = pytest.mark.skip(reason="Skipping EBM tests (libebm missing)")
        for item in items:
            # Option A: Skip by marker
            if "ebm" in item.keywords:
                item.add_marker(skip_ebm)
