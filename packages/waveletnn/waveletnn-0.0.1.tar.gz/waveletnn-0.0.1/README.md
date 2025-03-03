# Wavelet Neural Networks

Implementation of orthonormal and biorthogonal wavelet transforms via convolutions. Multibatch single-channel one- and -two-dimensional data is supported. For analysis kernels of even length are supported, while for inverse transform kernels are required to have length `4k + 2`. 

Package provides loss functions for wavelet's kernels regularizations to preserve features of both orthonormal and biorthogonal wavelets. 