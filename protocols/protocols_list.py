from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os

from protocols.apx import apx
from protocols.binaryswap import binaryswap
from protocols.cubiswap import cubiswap
from protocols.debank import debank
from protocols.derpdex import derpdex
from protocols.myshell import myshell
from protocols.pancake_perpetual_v2 import pancake
from protocols.thena import thena



def protocols_types():
    attribute = st.radio("Select Protocols", ["Myshell", "DeBank", "APX", "PancakeSwap_Perpetual", 'Thena', "Cubiswap", "Binaryswap", "DerpDex"], horizontal=True)

    if attribute == 'Myshell':
        myshell()
    elif attribute == 'DeBank':
        debank()
    elif attribute == 'APX':
        apx()
    elif attribute == 'PancakeSwap_Perpetual':
        pancake()
    elif attribute == 'Thena':
        thena()
    elif attribute == 'Cubiswap':
        cubiswap()
    elif attribute == 'Binaryswap':
        binaryswap()
    elif attribute == 'DerpDex':
        derpdex()