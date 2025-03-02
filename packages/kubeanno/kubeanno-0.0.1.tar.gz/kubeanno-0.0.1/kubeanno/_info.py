import os

_TOKEN_PATH = '/run/secrets/kubernetes.io/serviceaccount/token'
_HOST_PATH = '/etc/hostname'
_KUBECTL_PATH = '/usr/local/bin/kubectl'
_CA_PATH = '/run/secrets/kubernetes.io/serviceaccount/ca.crt'

_kubeinfo = None

def kubeinfo():
    global _kubeinfo
    if _kubeinfo is None:
        if os.path.exists(_TOKEN_PATH) and os.path.exists(_HOST_PATH) and os.path.exists(_KUBECTL_PATH) and os.path.exists(_CA_PATH):
            _kubeinfo = {
                'is_active': True,
                'token': open(_TOKEN_PATH).read().strip(),
                'hostname': open(_HOST_PATH).read().strip(),
                'ca': _CA_PATH,
                'kubectl': _KUBECTL_PATH,
            }
        else:
            _kubeinfo = {
                'is_active': False,
            }
    return _kubeinfo


def is_active():
    return kubeinfo().get('is_active')
