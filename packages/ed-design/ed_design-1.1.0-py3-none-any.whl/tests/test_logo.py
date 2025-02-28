# -*- coding: utf-8 -*-

from ed_design import logo
import numpy as np

# %%
def test_ed_logo_print():
    ed_logo = logo('print')
    assert isinstance(ed_logo, np.ndarray)
    assert ed_logo.sum() == 43028432
    
def test_ed_logo_web():
    ed_logo = logo('web')
    assert isinstance(ed_logo, np.ndarray)
    assert ed_logo.sum() == 6784625.0

def test_ed_logo_base():
    ed_logo = logo()
    assert isinstance(ed_logo, np.ndarray)
    assert ed_logo.sum() == 43028432
    
    