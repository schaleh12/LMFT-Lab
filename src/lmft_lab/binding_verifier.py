"""Private fixture registry adapter. Never returns registry contents to the learner.

The operator, not an inbox sender, owns this registry. Its records are produced by
the external trusted device fixture. Hashes pin bytes; they do not authenticate a
sender. This process boundary is not an OS sandbox against local malicious code.
"""
import json
from pathlib import Path
import subprocess
import sys

from . import binding_contract as contract
from .local_models import strict_json

RULE = 'binding-registry-verifier-1'


def registry(path):
    raw = Path(path).read_bytes()
    data = strict_json(raw.decode('utf-8'))
    if (type(data) is not dict or set(data) != {'version', 'identity', 'nonce', 'records'}
            or data['version'] != RULE or type(data['identity']) is not str
            or len(data['identity']) != 32 or type(data['nonce']) is not str
            or len(data['nonce']) != 64 or type(data['records']) is not dict):
        raise ValueError('invalid private registry')
    import hashlib
    pin = {'version': RULE, 'identity': data['identity'], 'sha256': hashlib.sha256(raw).hexdigest()}
    return data, pin


class Adapter:
    def __init__(self, path):
        self._path = str(Path(path).resolve())
        self.pin = self._call({'operation': 'identify'})['pin']

    def _call(self, request):
        try:
            result = subprocess.run([sys.executable, '-m', 'lmft_lab.binding_verifier', self._path],
                input=json.dumps(request), capture_output=True, text=True, timeout=15,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        except subprocess.TimeoutExpired as exc:
            raise ValueError('private binding verifier timed out') from exc
        if result.returncode:
            raise ValueError('private binding verifier unavailable or invalid')
        answer = strict_json(result.stdout)
        if hasattr(self, 'pin') and answer.get('pin') != self.pin:
            raise ValueError('private binding verifier changed')
        return answer

    def verify(self, record):
        answer = self._call({'operation': 'verify', 'record': record})
        return answer.get('record') if answer.get('verified') is True else None


def main():
    data, pin = registry(sys.argv[1])
    request = strict_json(sys.stdin.read())
    if request == {'operation': 'identify'}:
        answer = {'pin': pin}
    elif type(request) is dict and set(request) == {'operation', 'record'} and request['operation'] == 'verify':
        record = request['record']
        registered = data['records'].get(record.get('id')) if type(record) is dict else None
        # Canonical JSON distinguishes true from 1, unlike Python dict equality.
        valid = registered is not None and contract.digest(record) == contract.digest(registered)
        answer = {'pin': pin, 'verified': valid, 'record': registered if valid else None}
    else:
        raise ValueError('unsupported private verifier request')
    print(json.dumps(answer))


if __name__ == '__main__':
    main()
