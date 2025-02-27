import socket
import json
import logging
import time

log = logging.getLogger(__name__)

class AutoProfilingEntrypoint():
    def __init__(self, sock_path = None):
        self.sock_path = sock_path

        if self.sock_path is not None:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                self.sock.connect(self.sock_path)
            except ConnectionRefusedError:
                raise Exception("Could not connect to agent")
        else:
            self.sock = None
        
        self.profiling_range = self.ProfilingRange(self.profiling_start, self.profiling_stop)
        
        self.profile_start_time = None
        self.profiled_duration = 0
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock is not None:
            self.sock.close()
    
    def profiling_start(self):
        log.info("Starting profiling")
        
        if self.sock is None:
            log.warning("Running in standalone mode, skipping profiling start request.")
            return
        
        try:
            self.sock.sendall(b"start\n")
        except Exception as e:
            raise Exception("Failed to communicate with agent", e)
        
        self.profile_start_time = time.time()

    def profiling_stop(self):
        log.info("Stopping profiling")        
        
        if self.sock is None:
            log.warning("Running in standalone mode, skipping profiling stop request.")
            return
        
        try:
            self.sock.sendall(b"stop\n")
        except Exception as e:
            raise Exception("Failed to communicate with agent", e)
        
        self.profiled_duration += time.time() - self.profile_start_time
    
    class ProfilingRange():
        
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop
        
        def __enter__(self):
            self.start()
        
        def __exit__(self, exc_type, exc_value, traceback):
            self.stop()

    # User defined entrypoint for profiling
    def profile(self, **kwargs):
        pass
    
    def run(self, **kwargs):
        pass
    
