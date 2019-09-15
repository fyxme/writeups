> Client Side is Still Bad - Points: 150 - (Solves: 1105)
> I forgot my password again, but this time there doesn't seem to be a reset, can you help me? http://2018shell1.picoctf.com:55790 (link)

We start by inspecting the page and realise there is a `verify` function in it which seems to contain the flag.
```

  function verify() {
    checkpass = document.getElementById("pass").value;
    split = 4;
    if (checkpass.substring(split*7, split*8) == '}') {
      if (checkpass.substring(split*6, split*7) == 'd366') {
        if (checkpass.substring(split*5, split*6) == 'd_3b') {
         if (checkpass.substring(split*4, split*5) == 's_ba') {
          if (checkpass.substring(split*3, split*4) == 'nt_i') {
            if (checkpass.substring(split*2, split*3) == 'clie') {
              if (checkpass.substring(split, split*2) == 'CTF{') {
                if (checkpass.substring(0,split) == 'pico') {
                  alert("You got the flag!")
                  }
                }
              }
      
            }
          }
        }
      }
    }
    else {
      alert("Incorrect password");
    }
  }
```

By taking each part of the check we get the flag.

Flag: `picoCTF{client_is_bad_3bd366}`

