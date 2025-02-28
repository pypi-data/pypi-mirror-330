#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 07:53:46 2020

@author: nick
"""
import setuptools
import sys, os
import configparser

app = 'atlas_dev'

exec(open(os.path.join('./',app,'version.py')).read())
ver = __version__

setuptools.setup(

    # Version number (initial):
    version=ver,
)
