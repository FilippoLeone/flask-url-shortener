# Flask URL Shortener

### Packages used
- Flask & Flask restful
- Validator collection
- Sqlite3
- Request (for future tests)

### How to use the url shortener
- `app.py` Is the Python file you should call.

```
usage: app.py [-h] [--fresh-start FRESH_START]
              [--create-api-key CREATE_API_KEY]
              [--create-shortlink CREATE_SHORTLINK]
              [--server-start SERVER_START]

optional arguments:
  -h, --help            show this help message and exit
  --fresh-start FRESH_START
                        Runs DB fresh start creating the relative tables.
  --create-api-key CREATE_API_KEY
                        Creates and returns an API key, please provide your
                        email as argument.
  --create-shortlink CREATE_SHORTLINK
                        Creates a shortlink alias via commandline, provide a
                        full URL as argument.
  --server-start SERVER_START
                        Starts the server.

- Example usage for your first start after cloning the repository:
python app.py --fresh-start=1 --create-api-key=mybusinessemail@company.com --server-start=1
```


- Hit `/create` with a PUT request, having `x-api-key : ABC1234` in your request header and `{'full_url' : 'url_that_I_want_to_shorten.com/?my_query_params=yes'}` as body the API will return you the shortlink alias for that URL.

### Things to keep in mind
- Want to contribute? Submit a pull request.
- Code is ugly, refactoring will come in the future if the scope expands.

