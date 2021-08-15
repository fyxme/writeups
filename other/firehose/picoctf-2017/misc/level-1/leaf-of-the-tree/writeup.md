We cd into the give folder:

`/problems/a47d10dd80018fc6e7e1c5094c1ca323`

Instead of going down the tree manually we use find to find the location of the flag file (we hope one exists)

By doing `find . -name flag` we get : "./trunk/trunkbe9c/trunk8ec3/trunk708d/trunk664c/trunk430b/trunk122c/trunkc000/flag"

Using cat we check the contents of the file:

`cat ./trunk/trunkbe9c/trunk8ec3/trunk708d/trunk664c/trunk430b/trunk122c/trunkc000/flag`

And we get the flag.

Flag: `5e3d48f32a6d6e17a8102d3cbae36283`
