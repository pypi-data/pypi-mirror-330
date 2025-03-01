# Pixel Art Scaling - Scale2x, Scale3x, Scale2xSFX and Scale3xSFX in pure Python

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scalenx) ![PyPI - Version](https://img.shields.io/pypi/v/scalenx)

## Overview

[**Scale2x** and **Scale3x**](https://github.com/amadvance/scale2x) (aka **AdvMAME2x** and **AdvMAME3x**) algorithms were developed by [Andrea Mazzoleni](https://www.scale2x.it/) for the sole purpose of scaling up small graphics like icons and game sprites.

Later on versions called [**Scale2xSFX** and **Scale3xSFX**](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) were introduced for the same purpose, providing better diagonals rendering and less artifacts on some patterns.

Being initially created for tiny game sprite images, these algorithms appeared to be useful for some completely different tasks, *e.g.* scaling up text scans with low resolution before OCR, to improve OCR quality, or upscaling old low quality gravure and line art prints.

Therefore, current general purpose pure Python implementation of algorithms above was developed. Current implementation does not use any import, neither Python standard nor third party, and therefore is quite cross-platform and next to onmicompatible.

Note that current package is intended for developers, and therefore include ScaleNx core module only. For example of practical program utilizing this module, with GUI, multiprocessing *etc.*, please visit [ScaleNx at Github](https://github.com/Dnyarri/PixelArtScaling). PNG support in this example program is based on [PyPNG](https://gitlab.com/drj11/pypng), and PPM and PGM support - on [PyPNM](https://pypi.org/project/PyPNM/), both of the above being pure Python modules as well.

## Installation

`pip install ScaleNx`, then `from scalenx import scalenx, scalenxsfx`.

## Usage

Example for Scale3xSFX:

    scaled_image = scalenxsfx.scale3x(source_image)

where both images are of 3D nested list (image) of lists (rows) of lists (pixels) of int (channel values) type.

Note that functions names in scalenx and scalenxsfx match, making it easy to switch external software from older scalenx to scalenxsfx or *vs.* by changing one import line. When creating new software, one may easily make it reconfigurable with reassigning functions names, like

    if use_sfx:
        chosen_scaler = scalenxsfx.scale2x
    else:
        chosen_scaler = scalenx.scale2x

    scaled_image = chosen_scaler(source_image)

## Copyright and redistribution

Current implementation was written by [Ilya Razmanov](https://dnyarri.github.io/) and may be freely used, copied and improved. In case of making substantial improvements it's almost obligatory to share your work with the developer and lesser species.

## References

1. [Scale2x and Scale3x](https://www.scale2x.it/algorithm) algorithms description by the inventor, Andrea Mazzoleni.

2. [Scale2xSFX and Scale3xSFX](https://web.archive.org/web/20160527015550/https://libretro.com/forums/archive/index.php?t-1655.html) algorithms description at forums archive.

3. [Pixel-art scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms) review at Wikipedia.

4. [ScaleNx at Github](https://github.com/Dnyarri/PixelArtScaling/) - current ScaleNx home at Github, containing main program for single and batch image processing.
