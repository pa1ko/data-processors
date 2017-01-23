# data-processors
Data processing library based on pandas and numpy

### Basic rules
1. Always use vectores to speed up process
1. Input is Series (one or more)
1. Output is Series (only one?)
1. Output always have same length as input Series
1. Errors are returned as nulls
1. Processing funcs assume that data is in correct format, its user responsiblite to keep them in correct format, altghoe many modulse have func to unife data e.g. unify in pesel moduel.