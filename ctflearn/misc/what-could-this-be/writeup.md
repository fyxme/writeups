>

This looks like encoded javascript similar to "brainfuck js".

By using node we can decode the javascript and get the flag.

```
% node ~/Downloads/what_can_this_be.txt                   ~/Desktop/sec/ctf/ctflearn/misc
undefined:2
alert("flag{5uch_j4v4_5crip7_much_w0w}")
^

ReferenceError: alert is not defined
    at eval (eval at <anonymous> (/Users/louis/Downloads/what_can_this_be.txt:1:890), <anonymous>:2:1)
    at Object.<anonymous> (/Users/louis/Downloads/what_can_this_be.txt:1:50325)
    at Module._compile (module.js:643:30)
    at Object.Module._extensions..js (module.js:654:10)
    at Module.load (module.js:556:32)
    at tryModuleLoad (module.js:499:12)
    at Function.Module._load (module.js:491:3)
    at Function.Module.runMain (module.js:684:10)
    at startup (bootstrap_node.js:187:16)
    at bootstrap_node.js:608:3
```


Flag: `flag{5uch_j4v4_5crip7_much_w0w}`
