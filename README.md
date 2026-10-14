# http-post-form-login
Posts a form to a URL after doing an GET request on it and resolving any XPath queries on the result first for inclusion in the post. Useful for automated HTML form based logins.

**Usage:**

```
cat >test-form-template.json <<EOF
{
  "username": "admin",
  "$password": "./wordlist.txt",
  "@csrf_token": "//input[@name='csrf_token']/@value",
  "extra_field": "123"
}
EOF
./main.py --form-file test-form-template.json http://127.0.0.1:8080 --success-test "Login successful" --log-level DEBUG
```

**Form Template:**
Is given in JSON. Fields a converted to url-encoded form data for submission. The JSON may not be nested and all values are converted to strings. Two special key/value pairs are interpreted and transformed:

  - `$word: <file>`; Take values from file which is expected to a wordlist file.
  - `@word: <pattern>`; Take the value by querying `<pattern>` on the pre-fetch page.

**TODOs**

  - Different GET and POST URLs
  - GET once, POST many mode.
