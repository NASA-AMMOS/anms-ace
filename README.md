<!--
Copyright (c) 2023 The Johns Hopkins University Applied Physics
Laboratory LLC.

This file is part of the Asynchronous Network Managment System (ANMS).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This work was performed for the Jet Propulsion Laboratory, California
Institute of Technology, sponsored by the United States Government under
the prime contract 80NM0018D0004 between the Caltech and NASA under
subcontract 1658085.
-->

> [!IMPORTANT]
> This library has been relocated to [JHUAPL-DTNMA/dtnma-ace](https://github.com/JHUAPL-DTNMA/dtnma-ace) under a different Github organization.
> Future maintenance and upkeep of the library will be managed outside of the ANMS project and the AMMOS organization.
> Please use that forked project for any new developent and for bug or enhancement reports.

# ACE Tools
This is the AMM CODEC Engine (ACE) for the DTN Management Architecture (DTNMA).
It is part of the larger Asynchronous Network Managment System (ANMS) managed for [NASA AMMOS](https://ammos.nasa.gov/).

This library is based on [draft-birrane-dtn-adm-03](https://datatracker.ietf.org/doc/html/draft-birrane-dtn-adm-03) for data models and ARI processing.

It is a library to manage the information in DTNMA Application Data Models (ADMs) and use that information to encode and decode DTNMA Application Resource Identifiers (ARIs) in:
 * Text form based on [URI encoding](https://www.rfc-editor.org/rfc/rfc3986.html)
 * Binary form based on [CBOR encoding](https://www.rfc-editor.org/rfc/rfc9052.html)

It also includes an `ace_ari` command line interface (CLI) for translating between the two ARI forms.

## Development

To install development and test dependencies for this project, run from the root directory (possibly under sudo if installing to the system path):
```sh
pip3 install -r <(python-m library is based on * [draft-birrane-dtn-adm-03](https://datatracker.ietf.org/doc/html/draft-birrane-dtn-adm-03) for data models and ARI processing.
```

To install the project itself from source run:
```
pip3 install .
```

An example of using the ARI transcoder, from the source tree, to convert from text to binary form is:
```
echo 'ari:/IANA:ion_admin/CTRL.node_contact_add(UVAST.1685728970,UVAST.1685729269,UINT.2,UINT.2,UVAST.25000,UVAST.1)' | PYTHONPATH=./src ADM_PATH=./tests/adms python3 -m ace.library is based on * [draft-birrane-dtn-adm-03]ttps://datatracker.ietf.org/doc/html/draft-birrane-dtn-adm-03) for data models and ARI processing.inform=text --outform=cborhex
```
which will produce a hexadecimal output:
```
0xC1188D410605061616141416161A647A2ECA1A647A2FF502041961A801
```

## Contributing

To contribute to this project, through issue reporting or change requests, see the [CONTRIBUTING](CONTRIBUTING.md) document.
