Simple challenge where you have to explore the page itself to find the flag.

By inspecting the source code we find the first part of the flag in a comment:
```
<!-- Cool! Look at me! This is an HTML file. It describes what each page contains in a format your browser can understand. -->
<!-- The first part of the flag (there are 3 parts) is 9daca0510ff -->
<!-- What other types of files are there in a webpage? -->
```

We also see that there are 3resources loaded in:
- a css file
- a js file
- a jpg image

Since this is an intro to web challenge we can assume that the flags will be in the css and js file.

By opening the js file we find this message at the top:
```
This is the css file. It contains information on how to graphically display
the page. It is in a seperate file so that multiple pages can all use the same 
one. This allows them all to be updated by changing just this one.
The second part of the flag is eb6c5680635 
```

And finally from the js file we get the last part of the flag:
```
/* This is a javascript file. It contains code that runs locally in your
 * browser, although it has spread to a large number of other uses.
 *
 * The final part of the flag is f1ef52d049f
*/
```

By combining the 3 parts we get the flag

Flag: 9daca0510ffeb6c5680635f1ef52d049f
