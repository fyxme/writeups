> admin panel - Points: 150 - (Solves: 519)
> We captured some traffic logging into the admin panel, can you find the password?

We open the pcap file using wireshark.
Since it capture a password to an admin panel, we can safely assume it will be transferred unencrypted through HTTP.

We can filter by `http and http.request.method == "POST"'

The first packet contains:
```
HTML Form URL Encoded: application/x-www-form-urlencoded
    Form item: "user" = "jimmy"
    Form item: "password" = "p4ssw0rd"
```

This appears to be the flag but it actually isn't.

Looking at the hex values and their ascii equivalent in the second packet we can see 2 request parameters:
```
user=admin
password=picoCTF{n0ts3cur3_13597b43}
```

Flag: `picoCTF{n0ts3cur3_13597b43}`
