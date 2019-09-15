> Buttons - Points: 250 - (Solves: 1241)
> There is a website running at http://2018shell1.picoctf.com:7949 (link). Try to see if you can push their buttons.

The first button is a post request while the second is a link (aka GET request). If we send a POST request to the link of the second button we get the flag back.
```
% curl -X POST http://2018shell1.picoctf.com:7949/button2.php
Well done, your flag is: picoCTF{button_button_whose_got_the_button_3e5652dd}
```

Flag: `picoCTF{button_button_whose_got_the_button_3e5652dd}`
