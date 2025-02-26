#!/usr/bin/env python
# -*- coding: utf-8 -*-

from magma_database import *
from magma_auth import MagmaAuth
from magma_rsam import *
from magma_converter import *
from magma_converter.plot import PlotAvailability
from magma_multigas import *
from magma_multigas.plot_availability import PlotAvailability as MultiGasPlotAvailability
from magma_indonesia.main import app

from pkg_resources import get_distribution

__version__ = get_distribution("magma-indonesia").version
__author__ = ["Martanto", "Devy Kamil Syahbana", "Syarif Abdul Manaf"]
__author_email__ = "martanto@live.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, MAGMA Indonesia"
__url__ = "https://github.com/martanto/magma-indonesia-python"

__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__copyright__",
    "__url__",
    "app",
    "MagmaAuth",
    "RSAM",
    "PlotRsam",
    "Convert",
    "PlotAvailability",
    "Volcano",
    "Station",
    "Sds",
    "WinstonSCNL",
    "RsamCSV",
    "MountsSO2",
    "MountsThermal",
    "Config",
    "config",
    "MultiGas",
    "MultiGasData",
    "Diagnose",
    "Query",
    "MultiGasPlotAvailability"
]


def main():
    print(f"✅  MAGMA Indonesia")
    print(f"🔢 Version: {__version__}")
    print(f"✒️ Authors: {', '.join(__author__)}")


if __name__ == "__main__":
    main()
