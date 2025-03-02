# Basic utility to interact with conductor, such as fetching information.

# Although most of the function are one-liners, they are provided here
# as a convenient reference. In production it is likely better to simply call
# the ciocore methods directly rather than importing this module.

# Ciocore docs:
# https://docs.conductortech.com/core/api/v8.0.1/api_client/

import json
from ciocore import api_client


def instance_types():
    instance_types = api_client.request_instance_types()
    return instance_types


def software_packages(filter_for_product=None):
    software_packages = api_client.request_software_packages()
    if filter_for_product:
        software_packages = [
            item
            for item in software_packages
            if item["product"] == filter_for_product
        ]
    return software_packages


def projects():
    api_client.request_projects()


# Temp added for quick testing/printing
if __name__ == "__main__":
    # res = instance_types()
    res = software_packages(filter_for_product="houdini")
    print(json.dumps(res, indent=2))
