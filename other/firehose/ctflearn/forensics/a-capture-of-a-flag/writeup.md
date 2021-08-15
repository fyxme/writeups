1. Open the file with wireshark
2. Search for http
3. find the request to epimetheus.feralhosting.com where the GET request has a `msg` argument
4. Take the value and convert from base64. You get the flag: `flag{AFlagInPCAP}`
