# COMP6843 Break 2

REDACTED (z0000000) and REDACTED (z0000000)

## drive.bing.ns.agency
### Flags
The flags found were:
#### `BREAK2{891c3cd7-a607-4fa9-8c1c-95a6e860dcdf} also /staff/secret/1gbdfte/swagger`
This was found by initially observing the source code for anything abnormal or that stood out. This revealed two javascript files referenced:
** `app.fa5f9aad.js`
** `chunk-vendors.1368f516.js`
Both of these were not legible so the contents were put through a javascript linter to make them readable. Scanning through `app.fa5f9aad.js`, reveals the following code snippet:
```
[n("h1", [e._v(" Prism Help Page ")]), n("p", [e._v("
Welcome to bing drive valued NSA agents! This is the
set up page for new agents who want to access bing
drive files")]), n("h2", [e._v(" Set up ")]), n("p",
[e._v(" We used to have jim down on level 4 confirm all
new agents but due to donald trump hiring his own son\n
to take over that office we've shifted to just having a
unauthenticated end point you can hit to get staff
access\n  ")]), n("p", [e._v(" We've found it's more
secure, simply execute")]), n("code",
[e._v("/api/secret/no/really/give_staff_access?
username=test")]), n("p", [e._v("but replace "),
n("code", [e._v("test")]), e._v(" with your own
username ")]), n("h2", [e._v(" Api ")]), n("p", [e._v("
As a staff member you'll now have elevated access :)
")])])
```
This indicates that there is an api call that would let us elevate our account to a staff member. So we created an arbitrary user, and then invoked the `/api/secret/no/really/give_staff_access?username=` with our arbitrary user. Logging on now revealed a file called `staff_api_a456h7dvra` and viewing the contents of that file gave us the flag above along with a path for further exploration (`/staff/secret/1gbdfte/swagger`).

#### `BREAK2{26fedf86-1d4d-4363-9aa8-189a64bd3935}, Note to self, delete /admin`
This flag was found by exploring `/staff/secret/1gbdfte/swagger` as hinted from the previous flag. This link gave us a page which had two primary functions:
** Peek User - This allows us to view all the files authored by a specified user. It provides the author name, file id and file name.
** Peek File - This allows us to view the contents of a file based on a supplied file id.

Testing if a user called `admin` exists, we use the peek user functionality to test that out revealing a file called `flag` at file id equal to 1. Then using the peek file functionality, we reveal the contents of file id 1 which revealed the above flag as well as hinting at another location called `/admin`.

#### `BREAK2{ae5192a5-9c69-4d1f-97f8-cdce05979219}`
This flag was found by following the location hinted by the previous flag, `/admin`, which presented us with an input that required a four digit pin to gain access. There appeared to be no lockout etc, and there are only 4 digits with an alphabet of the 10 digits making it easy to bruteforce.

This was exploited by running a script which loops from the numbers `0` (formatted to `0000`) to `9999` to see which one produces the result. This reveals pin `2941` which when used to login gives us the flag.

### Other Exploits/issues

#### SQL injection on file_id
On the path `/staff/secret/1gbdfte/swagger/`, the `/peek/file` path API call is vulnerable to SQL injection which was ascertained by testing the input file_id field with the following string <code>'";<lol/>../--#`` `ls` ``</code>. This caused an error leading to a SQL injection vulnerability. Testing it out further reveals that it's matching an integer hence a leading `'` is not needed.

This allows us to enter a payload such as the following:
```
-1 UNION SELECT NULL, NULL, NULL, table_name
FROM information_schema.tables LIMIT 1
```
This allows us to query the metadata on the database which is quite severe as it allows us to view all the data (users, files, etc) in the database and dump it out if needed.

Additionally, it is possible to read files by querying the database as such: `0x1 and 1=0 UNION SELECT NULL, NULL, NULL, load_file('/etc/passwd')`. This will return the file requested in `load_file` and could be used to leak files on the server such as passwd file and application source code.

#### Unauthenticated file access

It is possible to access any file as long as you know the filename and the author's name. The files are protected by a url parameter `r` which is the simply url encoded string of the file author. This means with only a person's username we could bruteforce potential private documents such as "passport.pdf".

#### XSS

It is possible to create files with a simple XSS payload such as `<script>alert(1)</script>` as the contents and when the file display page is visited, it will execute the javascript. Combining it with the "Unauthentiated file access" issue, this means we can XSS other users as well by creating a file with an XXS payload and sending the url to any user.

This vulnerability allows us to steal's a user's cookie and run any malicious JS code in their browser.

#### User enumeration

Using the register feature, we can enumerate the usernames by attempting to create a user with the username to test. If the username is already taken an error message will display "Username already taken!" meaning a user with this username already exists.  If the user is using a weak password or reusing one of his old passwords leaked in a data breach, we can bruteforce the password to gain access to his account. This could be an even more serious issue if the user is an admin.

## pastebing.ns.agency

We were unable to find any flags here here but we were able to discover that the site is vulnerable to IDOR (Insecure Direct Object Reference) exploitation. Whenever a user creates a paste, it gets a unique path under the `raw` subdirectory to that paste. e.g. `http://pastebing.ns.agency/raw/9Q1ACynoThz`. These paths are insecure and can be referenced from anyone.

To exploit this, all we need to do is replace the path after `/raw/` with the path of another paste. Naturally, it would be good to know upfront of a target path e.g. we know a path contains the flag. Another option would be to brute force the path.

This is a severe vulnerability, especially if there is sensitive content, as it allows us to view anyone's pastes.

### User enumeration

Using the register feature, we can enumerate the usernames by attempting to create a user with the username to test. If the username is already taken an error message will display "Username already taken!" meaning a user with this username already exists.  If the user is using a weak password or reusing one of his old passwords leaked in a data breach, we can bruteforce the password to gain access to his account. This could be an even more serious issue if the user is an admin.
