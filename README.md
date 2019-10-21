# Flask URL Shortener

### Packages used
- Flask & Flask restful
- Validator collection
- Sqlite3
- Request (for future tests)

### How to use the url shortener
- Api keys are created accessing the machine where the code is hosted and calling the queryutil class.
- Hit `/create` with a PUT request, having `api-key : ABC1234` in your request header and `{'full_url' : 'url_that_I_want_to_shorten.com/?my_query_params=yes'}` as body the API will return you the shortlink alias for that URL.

### Things to keep in mind
- Why wasn't this developed by a real dev team? Because currently those teams don't have capacity for other projects. 
- Want to contribute? Submit a pull request.
- Code is ugly, refactoring will come in the future if the scope expands.
- Currently there is no authorization process in place as there is no need to it but if the scope of the tools expands I will write that part.
- Why SQLite and not something more "production-ready"? SQLite for this use-case works just fine, we don't need to perform many write operations. 

