
# This file was generated by 'versioneer.py' (0.15) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json
# import sys

version_json = '''
{
 "dirty": false,
 "error": null,
 "full-revisionid": "712716ab0cdebbec9fabb25eea3bf40e4354749d",
 "version": "0.9.2"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

# 增加一个version版本
__version__ = "0.9.2"