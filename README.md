# nikon_sensor_check_v2
Checks Nikon camera sensor for the dead and bad pixels

It uses 2 RAW (for Nion raw image has *.NEF extension) photos: 
1. Black image: it should be taken with high exposure with closed (by a cap) lens or without lens (with closed by a cap bayonet mount)
2. White image: it should be taken with high exposure with open lens (remove a cap from the lens)

Dead pixels are pixels that don't respond to the light. Such pixels return low RGB values even for the long exposure shot(they will be detected when processing White image)
Bad pixels are pixels that return constant non-zero RGB values regardless exposure time ot pixels that return incorrect RGB values (they will be detected when processing Black image).


You can change RGB values thresholds using corresponding sliders.
Usually it's ok to use RGB values more than 200 to check for bad pixels and RGB values less than 30 to check for dead pixels
As each pixel has 3 independent (in theory) channels, you can found that search for the broken pixels performs on 3 channels independently.

Probably this app can be used for other than Nikon cameras too (it was tested only with Nikon cameras), but you should change QFileDialog filter in files_loader.py to be able to load other than .NEF files