Another network challenge.

We open the data.pcap file with wireshark.

Filtering by `http and http.user_agent` gives us all the http request which have a user-agent header set.

Looking through all of the packets, we find only 1 with a unique user agent.

The user agent in question is: `Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36`

We extract the browser name and version from the user agent which gives us the flag.

Flag: `Chrome 36.0.1985.67`
