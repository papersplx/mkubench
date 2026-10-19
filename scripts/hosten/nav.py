#!/usr/bin/env python3
"""Navigate a gateway tab to a URL via the debug route."""
import sys
import urllib.parse
import urllib.request

model = sys.argv[1]
dest = sys.argv[2]
url = f"http://localhost:8079/debug/navigate?model={model}&url={urllib.parse.quote(dest)}"
try:
    r = urllib.request.urlopen(url, timeout=120).read().decode()
    print(r)
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}")
except Exception as e:  # noqa: BLE001
    print(f"ERR {type(e).__name__}: {e}")
