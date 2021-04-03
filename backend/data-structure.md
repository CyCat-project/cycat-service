# CyCAT data structure

The data structure is based on a Redis-compatible data store. [kvrocks](https://github.com/bitleak/kvrocks) is the Redis-compatible data store used for CyCAT
but any compatible Redis data store can be used.

# Statistics

## Automatic API statistics

Prefix of API statistic is `stats:f:` followed by the function name called.

- `stats:f:generateuuid` : number of calls to the UUID generator API
