# Mini IP Fabric Python SDK

## IP Fabric

[IP Fabric](https://ipfabric.io) is a vendor-neutral network assurance platform that automates the 
holistic discovery, verification, visualization, and documentation of 
large-scale enterprise networks, reducing the associated costs and required 
resources whilst improving security and efficiency.

It supports your engineering and operations teams, underpinning migration and 
transformation projects. IP Fabric will revolutionize how you approach network 
visibility and assurance, security assurance, automation, multi-cloud 
networking, and trouble resolution.

**Integrations or scripts should not be installed directly on the IP Fabric VM unless directly communicated from the
IP Fabric Support or Solution Architect teams.  Any action on the Command-Line Interface (CLI) using the root, osadmin,
or autoboss account may cause irreversible, detrimental changes to the product and can render the system unusable.**
networking, and trouble resolution.

## Project Description

Minimal Python Client for querying IP Fabric Table or Intent Summary using `requests`.

For full feature client please see [ipfabric](https://pypi.org/project/ipfabric/).

## Versioning

`Major.Minor.Patch`: For best results please match the `Major.Minor` to your IP Fabric installation.

## Installation

```commandline
pip install mini_ipfabric
```

## Configuration/Usage

```python
import os
from mini_ipfabric import IPFClient

ipf = IPFClient(base_url=os.getenv('IPF_URL'), auth=os.getenv('IPF_TOKEN'), verify=True)

print(ipf.technology.keys())
print(ipf.inventory.keys())

data = ipf.fetch_all(endpoint='/inventory/devices', reports=False, filters=None, columns=None)
# endpoint can be API or Web endpoint.

intents = ipf.get_intents()

```

## Support

Please open a ticket on GitLab.

