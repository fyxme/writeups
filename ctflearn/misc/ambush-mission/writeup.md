> AMBUSH MISSION
> 60 points

67 solves

Miscellaneous

Medium

pian

Hi, i can't tell you my name since now i'm in a mission. In case to arrest our fugitive target, our team had been intercepted communication between the target with his fellow and found this image (https://mega.nz/#!TKZ3DabY!BEUHD7VJvq_b-M22eD4VfHv_PPBnW2m7CZUfMbveZYw). It looks like they are going to meet in specific place, but we still don't know the time yet. Can you help me?


This is a stegonography challenge.

Using Stegsolve, we can look at different planes and find an interesting one which seems to contain a base64 string. 

By Decoding this string we get:
```
% echo "bTNFdF9tZV80dF8xMl9hTQ==" | base64 --decode                           ~
m3Et_me_4t_12_aM
```

Flag: `m3Et_me_4t_12_aM`
