# CyCAT.org API services

## Back-end

- [back-end](./backend) - software to run your own CyCAT.org API service. This software runs the official API for CyCAT.org available at [api.cycat.org](https://api.cycat.org/).

## Documentation

- CyCAT - The Cybersecurity Resource Catalogue public API services document is available as [OpenAPI 2.0 swagger file](https://api.cycat.org/swagger.json).
- [PDF](https://www.cycat.org/assets/docs/api-documentation-3.pdf) of the CyCAT API.

## API Usage and Examples

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

### Fetch item by UUID

~~~
curl -X 'GET' \
  'https://api.cycat.org/lookup/4cd29327-685a-460e-9dac-c3ab96e549dc' \
  -H 'accept: application/json'
~~~

~~~json
{
  "description": "Detects Execution via SyncInvoke in CL_Invocation.ps1 module",
  "raw": "author: oscd.community, Natalia Shornikova\ndate: 2020/10/14\ndescription: Detects Execution via SyncInvoke in CL_Invocation.ps1 module\ndetection:\n  condition: selection\n  selection:\n    EventID: 4104\n    ScriptBlockText|contains|all:\n    - CL_Invocation.ps1\n    - SyncInvoke\nfalsepositives:\n- Unknown\nid: 4cd29327-685a-460e-9dac-c3ab96e549dc\nlevel: high\nlogsource:\n  product: windows\n  service: powershell\nmodified: 2021/05/21\nreferences:\n- https://github.com/LOLBAS-Project/LOLBAS/blob/master/yml/OSScripts/Cl_invocation.yml\n- https://twitter.com/bohops/status/948061991012327424\nstatus: experimental\ntags:\n- attack.defense_evasion\n- attack.t1216\ntitle: Execution via CL_Invocation.ps1\n",
  "sigma:id": "4cd29327-685a-460e-9dac-c3ab96e549dc",
  "title": "Execution via CL_Invocation.ps1",
  "_cycat_type": "Item"
}
~~~

### Fetch relationships of an UUID

~~~
curl -X 'GET' \
  'https://api.cycat.org/relationships/fbd29c89-18ba-4c2d-b792-51c0adee049f' \
  -H 'accept: application/json'
~~~

~~~json
[
  "24bfaeba-cb0d-4525-b3dc-507c77ecec41",
  "b21c3b2d-02e6-45b1-980b-e69051040839",
  "e6919abc-99f9-4c6c-95a5-14761e7b2add",
  "cb69b20d-56d0-41ab-8440-4a4b251614d4",
  "2dc2b567-8821-49f9-9045-8740f3d0b958",
  "692074ae-bb62-4a5e-a735-02cb6bde458c",
  "b3d682b6-98f2-4fb0-aa3b-b4df007ca70a",
  "837f9164-50af-4ac0-8219-379d8a74cefc",
  "df8b2a25-8bdf-4856-953c-a04372b1c161",
  "8d7bd4f5-3a89-4453-9c82-2c8894d5655e",
  "e85cae1a-bce3-4ac4-b36b-b00acac0567b",
  "005a06c6-14bf-4118-afa0-ebcd8aebb0c9",
  "58a3e6aa-4453-4cc8-a51f-4befe80b31a8",
  "fb8d023d-45be-47e9-bc51-f56bcae6435b",
  "b76b2d94-60e4-4107-a903-4a3a7622fb3b",
  "3433a9e8-1c47-4320-b9bf-ed449061d1c3",
  "910906dd-8c0a-475a-9cc1-5e029e2fad58",
  "cf23bf4a-e003-4116-bbae-1ea6c558d565",
  "13cd9151-83b7-410d-9f98-25d0f0d1d80d",
  "afc079f3-c0ea-4096-b75d-3f05338b7f60",
  "ef67e13e-5598-4adc-bdb2-998225874fa9",
  "2b742742-28c3-4e1b-bab7-8350d6300fa7",
  "be2dcee9-a7a7-4e38-afd6-21b31ecc3d63",
  "9efb1ea7-c37b-4595-9640-b7680cd84279",
  "c5e3cdbc-0387-4be9-8f83-ff5c0865f377",
  "03342581-f790-4f03-ba41-e82e67392e23",
  "4b57c098-f043-4da2-83ef-7588a6d426bc",
  "db1355a7-e5c9-4e2c-8da7-eccf2ae9bf5c",
  "232b7f21-adf9-4b42-b936-b9d6f7df856e",
  "2a70812b-f1ef-44db-8578-a496a227aef2",
  "6add2ab5-2711-4e9d-87c8-7a0be8531530",
  "f5352566-1a64-49ac-8f7f-97e1d1a03300",
  "b17a1a56-e99c-403c-8948-561df0cffe81",
  "3fc9b85a-2862-4363-a64d-d692e3ffbee0",
  "1ecfdab8-7d59-4c98-95d4-dc41970f57fc",
  "00f90846-cbd1-4fc5-9233-df5c2bf2a662",
  "3257eb21-f9a7-4430-8de1-d8b6e288f529",
  "04fd5427-79c7-44ea-ae13-11b24778ff1c",
  "65f2d882-3f41-4d48-8a06-29af77ec9f90",
  "970a3432-3237-47ad-bcca-7d8cbb217736",
  "b18eae87-b469-4e14-b454-b171b416bc18",
  "dfd7cc1d-e1d8-4394-a198-97c4cab8aa67",
  "b4d80f8b-d2b9-4448-8844-4bef777ed676",
  "c848fcf7-6b62-4bde-8216-b6c157d48da0",
  "648f995e-9c3a-41e4-aeee-98bb41037426",
  "90ac9266-68ce-46f2-b24f-5eb3b2a8ea38",
  "8dbadf80-468c-4a62-b817-4e4d8b606887",
  "f232fa7a-025c-4d43-abc7-318e81a73d65",
  "2e34237d-8574-43f6-aace-ae2915de8597"
]
~~~

### Full-text search on CyCAT backend

~~~
curl -X 'GET' \
  'https://api.cycat.org/search/APT33' \
  -H 'accept: application/json'
~~~

Will return all the UUIDs matching the keyword queried (in this case `APT33`). Then the returned UUIDs can be used to find relationships and corresponding items.

~~~
[
  "db1355a7-e5c9-4e2c-8da7-eccf2ae9bf5c",
  "fbd29c89-18ba-4c2d-b792-51c0adee049f",
  "4f69ec6d-cb6b-42af-b8e2-920a2aa4be10",
  "2a70812b-f1ef-44db-8578-a496a227aef2",
  "2a70812b-f1ef-44db-8578-a496a227aef2",
  "8dbadf80-468c-4a62-b817-4e4d8b606887",
  "fab34d66-5668-460a-bc0f-250b9417cdbf",
  "e85cae1a-bce3-4ac4-b36b-b00acac0567b",
  "5de6335d-e128-4bc0-87e2-4db4950d210f",
  "08d5b8a4-e752-48f3-ac6d-944807146ce7",
  "15dd8386-f11a-485a-b719-440c0a47dee6",
  "ab603f29-9c10-4fb0-9fa3-e123fad11a31",
  "cfdb02f2-a767-4abb-b04c-333a02cdd7e2",
  "0c5bc5c8-5136-413a-bc5a-e13333271f49",
  "f9aa9004-8811-4091-a471-38f81dbcadc4",
  "5086a6e0-53b2-4d96-9eb3-a0237da2e591",
  "8a789016-5f8d-4cd9-ba96-ba253db42fd8",
  "f29b7c5e-2439-42ad-a86f-9f8984fafae3",
  "1acd0c6c-7aff-462e-94ff-7544b1692740",
  "accd848b-b8f4-46ba-a408-9063b35cfbf2",
  "2894aee2-e0ec-417a-811e-74a68ab967b2",
  "05252643-093b-4070-b62f-d5836683a9fa",
  "b18eae87-b469-4e14-b454-b171b416bc18",
  "588fb91d-59c6-4667-b299-94676d48b17b",
  "036bd099-fe80-46c2-9c4c-e5c6df8dcdee",
  "d29eb927-d53d-4af2-b6ce-17b3a1b34fe7"
]
~~~

## Crawlers available to feed the CyCAT back-end

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

