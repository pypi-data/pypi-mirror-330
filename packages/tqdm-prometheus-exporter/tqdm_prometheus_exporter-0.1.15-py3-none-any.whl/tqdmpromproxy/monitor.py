'''
Periodically they will publish the snapshots to a shared queue
Monitors are individual async processes that watch a tqdm instance.
'''
import logging

from queue import Queue
from threading import Thread, Event
from time import sleep, time

from tqdm import tqdm

from tqdmpromproxy.snapshot import TqdmSnapshot

# pylint: disable=missing-function-docstring


class TqdmMonitor:
    '''
    Oversee a single tqdm instance and emit updates.
        Monitors run within the same process/thread as the tqdm instance they are monitoring
    '''

    def __init__(self, collector: Queue):
        # known tqdm instances 'top level' instances
        self.discovered: list[tqdm] = []  # individual bars

        self.collector = collector

        self.worker = Thread(target=self._poll, daemon=True,
                             name=f"{__class__.__name__}.worker")
        self._stop_event = Event()
        self.poll_delay = 0.5

        self.logger = logging.getLogger(__name__)

    def start(self):
        '''Start the monitor'''
        self.worker.start()

    def stop(self):
        '''Stop the monitor'''
        self._stop_event.set()

    def _poll(self):
        '''Poll the tqdm instances for updates and emit them to the collector'''

        while not self._stop_event.is_set():
            try:
                snapshots = self._collect()

                if len(snapshots) == 0:
                    self.stop()

                for snap in snapshots:
                    self.collector.put(snap)

            except KeyboardInterrupt:
                self.logger.info("Polling interrupted")
                break

            finally:  # purposefully continue
                self.logger.info("Polling complete")
                sleep(self.poll_delay)

            sleep(self.poll_delay)

    def add(self, tqdm_instance: tqdm):
        '''Add a new tqdm instance to the monitor'''
        self.discovered.append(tqdm_instance)

    def _collect(self) -> list[TqdmSnapshot]:
        '''Collect the current state of all known tqdm instances'''
        snapshots = []

        for known_instance in self.discovered:
            if known_instance.disable or \
                    known_instance.last_print_t < (time() - 30.0) or \
                    known_instance.total == known_instance.n:
                continue

            snapshot = TqdmSnapshot.from_bar(known_instance)
            self.logger.info("Snapshotted bar %s", snapshot)
            snapshots.append(snapshot)

        return snapshots
