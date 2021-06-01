# CyCAT.org API services

## Back-end

- [back-end](./backend) - software to run your own CyCAT.org API service. This software runs the official API for CyCAT.org available at [api.cycat.org](https://api.cycat.org/).

## Documentation

- CyCAT - The Cybersecurity Resource Catalogue public API services document is available as [OpenAPI 2.0 swagger file](https://api.cycat.org/swagger.json).
- [PDF](https://www.cycat.org/assets/docs/api-documentation-3.pdf) of the CyCAT API.

## API Usage Example

### Search by namespace topic

~~~
curl -X 'GET' \
  'https://api.cycat.org/namespace/finduuid/mitre-attack-id/T1216' \
  -H 'accept: application/json'
~~~

Searching for all the known items in CyCAT about the MITRE ATT&CK T1216 returns the following UUIDs

~~~json
[
  "a0459f02-ac51-4c09-b511-b8c9203fc429",
  "f588e69b-0750-46bb-8f87-0e9320d57536",
  "39776c99-1c7b-4ba0-b5aa-641525eee1a4",
  "59e938ff-0d6d-4dc3-b13f-36cc28734d4e",
  "6609c444-9670-4eab-9636-fe4755a851ce",
  "51048ba0-a5aa-41e7-bf5d-993cd217dfb2",
  "9df0dd3a-1a5c-47e3-a2bc-30ed177646a0",
  "4cd29327-685a-460e-9dac-c3ab96e549dc",
  "99465c8f-f102-4157-b11c-b0cddd53b79a",
  "074e0ded-6ced-4ebd-8b4d-53f55908119d",
  "f6fe9070-7a65-49ea-ae72-76292f42cebe",
  "c363385c-f75d-4753-a108-c1a8e28bdbda"
]
~~~


## Crawler

- [GitHub](./crawler/github/)
- [MISP Feeds](./crawler/misp-feeds/)
- [MISP Galaxy](./crawler/misp-galaxy/)
- [MITRE CTI - ATT&CK](./crawler/mitre-cti)
- [Sigma](./crawler/sigma/)

# License

CyCAT.org back-end software is released under the AGPL version 3.

~~~
Copyright (c) 2021 Alexandre Dulaunoy
Copyright (c) 2021 CyCAT.org project
~~~

