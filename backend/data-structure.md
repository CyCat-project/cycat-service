# CyCAT data structure

The data structure is based on a Redis-compatible data store. [kvrocks](https://github.com/bitleak/kvrocks) is the Redis-compatible data store used for CyCAT
but any compatible Redis data store can be used.

# u:<UUID>

Each UUID inserted in CyCAT has at least an entry in the backend with the following format:

- `u:<UUID>` -> `value type`

## Value type available

|value|type|
|-----|-----------------------------------------|
| 1   | Publisher                               |
| 2   | Project                                 |
| 3   | Item                                    |

# <TYPE INT>:<UUID> (hash table) metadata

Each UUID inserted might have a corresponding hash table

- `<type>:<UUID>` -> keys associated with the hash table type

## Reserved keys

- `raw` - raw data for the specific item
- `cycat-oid` - UUID of the publisher or project CyCAT
- `link` - URL reference of the publisher, project or item
- `timestamp` - Last update of the UUID metadata
- `short-name`
- `name`
- `maintainer` - maintainer of the metadata (e.g. cycat)
- `description`
- `_cycat_type`
  
Other field should be prefixed by the origin of the metadata with a format `<namespace>:<fieldname>`.

# t:<TYPE INT> (sorted set)

Each type got a sorted set (with a score of one) to easily paginate over the various types

- `t:<type>` -> `<UUID>`

# parent:<UUID> (set)

The parent(s) UUID of the UUID.

- `parent:<UUID>` -> {`UUID`, `UUID`}

# child:<UUID> (set)

The child(ren) UUID of the UUID.

- `child:<UUID>` -> {`UUID`, `UUID`}

# r:<UUID> (set)

The list of relationships from a specific UUID.

- `r:<UUID>` -> {`UUID`, `UUID`}

# rd:<UUID>:<UUID> (set)

The relationship data from an UUID tuple.

- `rd:<source UUID>:<destination UUID>` -> {`value`, `value`}

# id:<NAMESPACE>:<NAMESPACE_ID> (set)

A namespace id referenced in an UUID

- `id:<NAMESPACE>:<NAMESPACE_ID>` -> {`UUID`, `UUID`}

# idk:<NAMESPACE> (set)

Known id per namespace

- `idk:<NAMESPACE>' -> {`NAMESPACE_ID`, `NAMESPACE_ID`}

# Statistics

## Automatic API statistics

Prefix of API statistic is `stats:f:` followed by the function name called.

- `stats:f:generateuuid` : number of calls to the UUID generator API

# Fixed UUIDs for UUIDv5 generation

|value|description|
|-----|-----------|
|690b3b43-d689-481c-aa61-5351963a36f2|Used to generate the UUID of a GitHub url - concatenation key is `publisher:project`|
|39d6e10c-dac7-40e2-8e99-1ab1cefea6f4|Used to generate CyCAT OID for publisher and project|
