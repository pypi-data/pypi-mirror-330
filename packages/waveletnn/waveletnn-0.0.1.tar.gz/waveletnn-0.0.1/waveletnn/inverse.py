import torch
import torch.nn as nn
import torch.nn.functional as F

from waveletnn import PadSequence


class InverseWaveletBlock1D(nn.Module):
    """Block for one-dimensional inverse discrete wavelet transform.

    Kernel size is required to have size `4k + 2`. Kernels can be provided on module init or on inference. 

    Args:
        kernel_size (int): Length of kernels
        levels (int, default=1): Number of transform levels
        padding_mode (str, default="antireflect"): The padding scheme, "constant", "circular", "replicate", "reflect" or "antireflect"
        static_filters (bool, default=True): Whether kernels are provided on init
        h (torch.Tensor, default=None): Scaling filter
        g (torch.Tensor, default=None): Wavelet filter
    """

    def __init__(self, kernel_size: int, levels: int = 1, padding_mode: str = "antireflect", static_filters: bool = True, h = None, g = None):
        assert (kernel_size - 2) % 4 == 0
        super(InverseWaveletBlock1D, self).__init__()

        self.levels = levels
        self.kernel_size = kernel_size
        self.padding = (kernel_size - 2) // 4
        self.padding_mode = padding_mode
        self.pad = PadSequence(self.padding, self.padding, padding_mode)

        if static_filters:
            assert h is not None and g is not None, "`h` and `g` must be specified"
            assert len(h) == self.kernel_size and len(g) == self.kernel_size

            self.scaling_kernel = torch.flip(
                h.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1)

            self.wavelet_kernel = torch.flip(
                g.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1)
        self.static_filters = static_filters


    def forward(self, signal, details, h = None, g = None):
        """Forward pass of InverseWaveletBlock1D.
        
        Args:
            signal (torch.Tensor): The last approximation
            details (List[torch.Tensor]): The list of details on different levels, len(details) == self.levels
            h (torch.Tensor, default=None): Scaling filter if self.static_filters == False
            g (torch.Tensor, default=None): Wavelet filter if self.static_filters == False
        
        Output:
            torch.Tensor: reconstructed signal
        """
        
        if len(signal) == self.levels:
            signal = signal[-1]
        c = signal.shape[0]

        if self.static_filters:
            h = self.scaling_kernel
            g = self.wavelet_kernel
        else:
            assert h is not None and g is not None, "`h` and `g` must be specified"
            assert len(h) == self.kernel_size and len(g) == self.kernel_size

            h = torch.flip(
                h.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1)

            g = torch.flip(
                g.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1)

        for i in range(self.levels-1, -1, -1):
            # pad signal and details
            signal = self.pad(signal)
            detail = self.pad(details[i])
            # convolve and riffle
            signal = F.conv1d(signal, h, stride=1).permute(0,2,1).reshape(c,1,-1)
            detail = F.conv1d(detail, g, stride=1).permute(0,2,1).reshape(c,1,-1)
            # add up
            signal = torch.add(signal, detail)

        return signal
    

class InverseWaveletBlock2D(nn.Module):
    """Block for two-dimensional inverse discrete wavelet transform.

    Kernel size is required to have size `4k + 2`. Kernels can be provided on module init or on inference. 

    Args:
        kernel_size (int): Length of kernels
        levels (int, default=1): Number of transform levels
        padding_mode (str, default="antireflect"): The padding scheme, "constant", "circular", "replicate", "reflect" or "antireflect"
        static_filters (bool, default=True): Whether kernels are provided on init
        h (torch.Tensor, default=None): Scaling filter
        g (torch.Tensor, default=None): Wavelet filter
    """

    def __init__(self, kernel_size: int, levels: int = 1, padding_mode: str = "antireflect", static_filters: bool = True, h = None, g = None):
        assert (kernel_size - 2) % 4 == 0
        super(InverseWaveletBlock2D, self).__init__()

        self.levels = levels
        self.kernel_size = kernel_size
        self.padding = (kernel_size - 2) // 4
        self.padding_mode = padding_mode
        self.pad = PadSequence(self.padding, self.padding, padding_mode)

        if static_filters:
            assert h is not None and g is not None, "`h` and `g` must be specified"
            assert len(h) == self.kernel_size and len(g) == self.kernel_size

            self.scaling_kernel = torch.flip(
                h.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1).unsqueeze(1)

            self.wavelet_kernel = torch.flip(
                g.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1).unsqueeze(1)
        self.static_filters = static_filters


    def forward(self, ss, sd, ds, dd, h = None, g = None):
        """Forward pass of InverseWaveletBlock2D.
        
        Args:
            ss (torch.Tensor): The last approximation
            sd, ds, dd (List[torch.Tensor]): The list of details on different levels, len(sd) == len(ds) == len(dd) == self.levels
            h (torch.Tensor, default=None): Scaling filter if self.static_filters == False
            g (torch.Tensor, default=None): Wavelet filter if self.static_filters == False
        
        Output:
            torch.Tensor: reconstructed signal
        """
        
        # number of batches
        b = ss.shape[0]

        if self.static_filters:
            h = self.scaling_kernel
            g = self.wavelet_kernel
        else:
            assert h is not None and g is not None, "`h` and `g` must be specified"
            assert len(h) == self.kernel_size and len(g) == self.kernel_size

            h = torch.flip(
                h.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1).unsqueeze(1)

            g = torch.flip(
                g.reshape(-1,2).permute(1,0), (1,)
            ).unsqueeze(1).unsqueeze(1)

        for i in range(self.levels-1, -1, -1):
            # compute convolution kernels for channel processing
            c = ss.shape[2]
            H = h.repeat(c, 1, 1, 1)
            G = g.repeat(c, 1, 1, 1)


            # synthesize approximation
            signal = self.pad(ss.mT.permute(0,2,1,3))
            detail = self.pad(sd[i].mT.permute(0,2,1,3))
            s = torch.add(
                F.conv2d(signal, H, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1),
                F.conv2d(detail, G, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1)
            ).permute(0,2,1,3).mT.permute(0,2,1,3)

            # synthesise details
            signal = self.pad(ds[i].mT.permute(0,2,1,3))
            detail = self.pad(dd[i].mT.permute(0,2,1,3))
            d = torch.add(
                F.conv2d(signal, H, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1),
                F.conv2d(detail, G, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1)
            ).permute(0,2,1,3).mT.permute(0,2,1,3)

            # compute convolution kernels for channel processing
            c = s.shape[1]
            H = h.repeat(c, 1, 1, 1)
            G = g.repeat(c, 1, 1, 1)

            # synthesize signal
            ss = torch.add(
                F.conv2d(self.pad(s), H, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1),
                F.conv2d(self.pad(d), G, stride=1, groups=c).reshape(b, c, 2, -1).permute(0,1,3,2).reshape(b,c,1,-1)
            ).permute(0,2,1,3)

        return ss