# TMGA EXTENDED MULTI-DIMENSIONAL SIMULATION
# Reference simulation for Section 8.9 of the manuscript.
# 7 Critical Dimensions: 1.8, 2.8, 2.11, 3.7, 3.8, CBP, NHCP

import numpy as np
import random
import json
from collections import Counter

CRITICAL_DIMENSIONS = ["1.8", "2.8", "2.11", "3.7", "3.8", "CBP",
