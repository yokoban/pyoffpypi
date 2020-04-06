import json
import re

import requests

PYPI_PACKAGE_JSON_URL = "https://pypi.org/pypi/"
PYPI_PROJECT_URL = "https://pypi.org/project/"


def parse_package(target):
    pattern = re.compile("([a-zA-Z0-9_\-]+)(?:\s+|)(?:(\([^\)]+\)|))")

    if target.find("extra") > 0:
        return "", ""

    res = re.findall(pattern, target)[0]

    return res[0], res[1]


def get_requires_dist(target):
    url = f"{PYPI_PACKAGE_JSON_URL}{target}/json"
    res = requests.get(url)
    requires = json.loads(res.text)["info"]["requires_dist"]

    return requires


def main(target, requires={}):
    if target == "":
        return

    packages = get_requires_dist(target)

    if packages is not None:
        for package in packages:
            name, ver = parse_package(package)
            if name != "" and name not in requires:
                print(name)
                main(name, requires)

                requires[name] = (ver, f"{PYPI_PROJECT_URL}{name}")

    return requires


def max_length(target):
    max_len = -1
    for row in target:
        if max_len < len(row):
            max_len = len(row)

    return max_len


if __name__ == "__main__":
    require_packages = main("tensorflow")

    name_len = max_length(require_packages.keys())
    var_len = max_length([value for value, _ in require_packages.values()])

    for name, (ver, url) in require_packages.items():
        print(f"name: {name:{name_len}s}  ver: {ver:{var_len}s}  url: {url}")
