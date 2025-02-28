# Plotting Tools for PE

Plotting tools for PE (`ptfp`) is a compilation of useful tools which makes it easier to produce attractive plots from `bilby` results.
Largely these scripts are wrappers of other, lower level scripts, or refactoring of plotting scripts in bilby.
The aim is to make them more flexible and easier to invoke, to reduce the amount of copying and pasting that must happen when producing various plots. 

This package is maintained separately from `bilby` on the assumption that these scripts are out of scope for the core package.
In particular, extra dependencies (namely pycbc) are added to accomplish certain plotting tasks.
If it is desirable to merge any component into the main `bilby` library, doing so is welcomed.

## Parts of this Documentation 

In the [Examples](./Plotting Tools for PE Examples/) section, there are examples of how to use `ptfp` for two common tasks: making a spectrogram and plotting the time frequency track, and plotting the whitened time domain data and time domain waveform reconstruction.

In the [API](./API) section, docstrings from the source code are automatically rendered.
`ptfp` aims to keep 100% docstring coverage, and so this section should be the go-to reference for detailed usage of this package.


## License

Copyright 2024 Rhiannon Udall

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
