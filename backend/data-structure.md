# CyCAT data structure

The data structure is based on a Redis-compatible data store. [kvrocks](https://github.com/bitleak/kvrocks) is the Redis-compatible data store used for CyCAT
but any compatible Redis data store can be used.

# UUID k/v

Each UUID inserted in CyCAT has at least an entry in the backend with the following format:

- `u:<UUID>` -> `value type`

## Value type available

|value|type|
|-----|-----------------------------------------|
| 1   | Publisher                               |
| 2   | Project                                 |

# UUID hash table

Each UUID inserted might have a corresponding hash table

- `<type>:<UUID>` -> keys associated with the hash table type

# type sorted set

Each type got a sorted set (with a score of one) to easily paginate over the various types

- `t:<type>` -> `<UUID>`

# Statistics

## Automatic API statistics

Prefix of API statistic is `stats:f:` followed by the function name called.

- `stats:f:generateuuid` : number of calls to the UUID generator API
