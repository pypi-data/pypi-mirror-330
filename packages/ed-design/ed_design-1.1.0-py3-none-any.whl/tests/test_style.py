# -*- coding: utf-8 -*-

import ed_design as edd
import numpy as np
import pytest

# %%
def test_style_envidan():
    try:
        # Call the code or function you want to test here
        result = edd.style(style='envidan')
    except Exception as e:
        pytest.fail(f"Code raised an exception: {e}")

def test_style_default():
    try:
        result = edd.style(style='default')
    except Exception as e:
        pytest.fail(f"Code raised an exception: {e}")

def test_prop_cycle_normal():
    try:
        result = edd.prop_cycle(palette='normal')
    except Exception as e:
        pytest.fail(f"Code raised an exception: {e}")

def test_prop_cycle_dark():
    try:
        result = edd.prop_cycle(palette='dark')
    except Exception as e:
        pytest.fail(f"Code raised an exception: {e}")
        
        
def test_font_check():
    try:
        result = edd.font_check()
    except Exception as e:
        pytest.fail(f"Code raised an exception: {e}")

