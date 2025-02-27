# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

from io import StringIO
from time import sleep
import unittest

import requests

from tqdmpromproxy.proxy import TqdmPrometheusProxy


class ProxyIntegrationTest(unittest.TestCase):
    def test_export(self):
        try:
            proxy = TqdmPrometheusProxy()
            proxy.start()

            instances = [proxy.tqdm(i, desc=f'Item#{i}', total=100, position=i)
                         for i in range(10)]

            counter = 0
            for i in instances:
                i.update(counter*10)
                counter += 1

            def test():
                _buf = StringIO()
                proxy.http_server.bucketer.export(_buf)
                buf = _buf.getvalue()

                return 'Item#0' in buf, f"Wanted Item#0 in '{buf}'"

            self._retryable_assertion(test)
        finally:
            proxy.stop()

    def test_long_task_not_duplicated(self):
        try:
            proxy = TqdmPrometheusProxy()
            proxy.start()

            duration_s = 30
            total = 100

            for _ in proxy.tqdm(range(total), desc='LongItem'):
                sleep(duration_s/float(total))

            _buf = StringIO()
            proxy.http_server.bucketer.export(_buf)
            buf = _buf.getvalue()

            self.assertIn('LongItem_active_count 1', buf,
                          f"Wanted single instance in \n---\n'{buf}'\n---")
        finally:
            proxy.stop()

    def _retryable_assertion(self, test: callable, max_wait=10.0):
        delay = 0.2
        assertion = False
        while not assertion:
            assertion, message = test()
            if not assertion:
                delay *= 2
                if delay > max_wait:
                    break

                print(
                    f"Assertion failed. Recieved: {message}")
                sleep(delay)

        return self.assertTrue(assertion, message)

    def test_state_serialisation_manipulation(self):
        p = TqdmPrometheusProxy()
        p.start()

        self.assertIsNotNone(p.http_server)
        self.assertIsNotNone(p.monitors)

        serialised_data = p.__getstate__()
        # ensure state which gets picked doesnt include excluded properties
        self.assertNotIn('http_server', serialised_data)
        self.assertNotIn('monitors', serialised_data)

        p.__setstate__(serialised_data)

        self.assertIsNone(p.http_server)
        self.assertListEqual(p.monitors, [])

    def test_homepage(self):
        p = TqdmPrometheusProxy(http_host='localhost', http_port=3001)
        p.start()

        self.assertTrue(p.http_server.is_alive())  # ensure port is not in use

        try:
            response = requests.get(
                f'http://{p.http_server.address}:{p.http_server.port}/', timeout=1)
            self.assertEqual(response.status_code, 200)
        finally:
            p.stop()

    def test_debug_poll(self):
        p = TqdmPrometheusProxy(http_host='localhost', http_port=3002)
        p.start()

        self.assertTrue(p.http_server.is_alive())  # ensure port is not in use

        try:
            response = requests.get(
                f'http://{p.http_server.address}:{p.http_server.port}/debug', timeout=1)
            self.assertEqual(response.status_code, 200)
        finally:
            p.stop()

    def test_metrics_poll(self):
        p = TqdmPrometheusProxy(http_host='localhost', http_port=3003)
        p.start()

        self.assertTrue(p.http_server.is_alive())  # ensure port is not in use

        try:
            response = requests.get(
                f'http://{p.http_server.address}:{p.http_server.port}/metrics', timeout=1)
            self.assertEqual(response.status_code, 200)
        finally:
            p.stop()
