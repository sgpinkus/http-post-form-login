# http-post-form-login
THC Hydra http-post-form doesn't work with CSRF form tokens AFAIK. This script does. Given a URL and a form template, for each login attempt first the page is requested (GET), then values in the form template are resolved then the form is submitted (POST) to the URL (TODO: support different URLs).

**Form template**: is given in JSON, and fields a converted to url-encoded form data for submission. The JSON may not be nested and all values are converted to strings. Two special key/value pairs are interpreted and transformed:

    - $word: <file>; Take values from file which is expected to a wordlist file.
    - @word: <pattern>; Take the value by querying <pattern> on the pre-fetch page.

# Usage

```
./main.py "http://192.168.3.3/DVWA/login.php" --form-file=./test-form.json --fail-test="Login failed" --log-level=DEBUG
```
