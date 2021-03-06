# nikon_sensor_check_v2
Checks Nikon camera sensor for the dead and bad pixels

It uses 3 RAW (Nikon raw image has *.NEF extension) photos: 
1. Black image: it should be taken with high exposure with closed (by a cap) lens or without lens (with closed by a cap bayonet mount), with maximum F number (maximum closed aperture) and ISO ~200
2. White image: it should be taken with high exposure with open lens (remove a cap from the lens), with maximum F number (maximum closed aperture) and ISO ~200
3. Test image: just  a normal shot that you can use to see an influence of broken pixels on the regular picture

Dead pixels are pixels that don't respond to the light. Such pixels return low RGB values even for the long exposure shot(they will be detected when processing White image)
Bad (Hot) pixels are pixels that return constant non-zero RGB values regardless exposure time or pixels that return incorrect RGB values (they will be detected when processing Black image).


You can change RGB values thresholds using corresponding sliders.
Usually it's ok to use RGB values less than 100 to check for bad pixels and RGB values more than 220 to check for dead pixels
As each pixel has 3 independent (in theory) channels, you can found that search for the broken pixels performs on 3 channels independently.
When processing, app calculates total amounts and coordinates of pixels that have R/G/B value MORE than threshold for the Black image and LESS than threshold for the White image.
All this pixels are surrounded by a circles whose colors correspond to the channel (R/G/B color) whose threshold has been reached

You can see highlighted bad pixels on the regular image by choosing Test image and then perform 'Apply mask' operation

Probably this app can be used for other than Nikon cameras too (it was tested only with Nikon cameras), but you should change QFileDialog filter in files_loader.py to be able to load other than .NEF files


to run the app just run main_window.py:
`python main_window.py`
