"""Check draft examples only; neither an authorization nor a migration."""
import json
from .contracts_v2 import check_examples
from .lock import ROOT,load
if __name__=='__main__':print(json.dumps(check_examples(load(ROOT/'integration-lock-v2.json')),sort_keys=True))
