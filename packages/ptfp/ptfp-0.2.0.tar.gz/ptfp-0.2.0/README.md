# Overview

A set of plotting tools which assist in making high quality plots for gravitational wave data, especially as it applies to parameter estimation. These are mostly building on bilby, though some only interact directly with gwpy. 

This code aims to atomize functions to the greatest degree possible, so that individual components may be interchanged as easily as possible. Furthermore, it will aim to support independent choices of various matplotlib settings, so that users can decide this for itself, though very high level functions may set defaults. 

