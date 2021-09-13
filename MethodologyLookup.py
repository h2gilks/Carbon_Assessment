#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 18:48:29 2021

@author: henry
"""

import pandas as pd

from datetime import datetime

excel1 = 'Methodologies.xlsx'

# File2Match = pd.read_excel (excel3, sheet_name='Collated')

df1 = pd.read_excel (excel1, sheet_name='Full Methodology List')
df1 = pd.read_excel (excel1, sheet_name='test')

print(df1)

