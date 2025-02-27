'''
TQDM Prometheus Proxy, a simple proxy to expose TQDM metrics to Prometheus.
> use 
```proxy = TqdmPrometheusProxy(host, port)
proxy.start()
then use tqdm from proxy
proxy.tqdm('Item #%s', i, total=100, position=i)
```
'''

from tqdmpromproxy.snapshot import TqdmSnapshot
from tqdmpromproxy.proxy import TqdmPrometheusProxy
from logging import getLogger, NullHandler
getLogger(__name__).addHandler(NullHandler())
