Running the file command already gives us a lot of information

```
file image.jpg
image.jpg: JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=8, orientation=upper-left, xresolution=110, yresolution=118, resolutionunit=2, software=Adobe Photoshop CS6 (Windows), datetime=2016:02:10 11:55:56, GPS-Data], comment: ""Your flag is flag_2_meta_4_me_<lat>_<lon>_f8ad. Now find the GPS coordinates of this image! (", progressive, precision 8, 500x500, frames 3
```

From the comment we have `Your flag is flag_2_meta_4_me_<lat>_<lon>_f8ad` and we just need to find the latitude and longitude.

Using `exiftool` we can look at the meta-data of the picture and we find the GPS coordinates from it

```
[1] % exiftool image.jpg | grep GPS
GPS Version ID                  : 2.3.0.0
GPS Latitude                    : 91 deg 0' 0.00"
GPS Longitude                   : 124 deg 0' 0.00"
Comment                         : "Your flag is flag_2_meta_4_me_<lat>_<lon>_f8ad. Now find the GPS coordinates of this image! (Degrees only please)"
GPS Position                    : 91 deg 0' 0.00", 124 deg 0' 0.00"
```

Combining the flag template with the coordinates we get our flag.

Flag: `flag_2_meta_4_me_91_124_f8ad`

