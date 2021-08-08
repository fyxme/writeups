https://fbctf.com/challenges

Products manager:
- https://stackoverflow.com/questions/11714534/mysql-database-with-unique-fields-ignored-ending-spaces?

- Prepared statements are correct and therefore no SQLi
- MySQL ignores trailing spaces in comparaisons

To exploit:
1. Create a user with name `facebook` and some trailing spaces like `facebook   `. And add a secret you will remember like `asdfasdfasdfA1`
2. View the user named `facebook` with secret `asdfasdfasdfA1`
3. You get the flag.


```
- facebook
- Facebook, Inc. is an American online social media and social networking service company based in Menlo Park, California. Very cool! Here is a flag for you: fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}
```

Flag: `fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}`