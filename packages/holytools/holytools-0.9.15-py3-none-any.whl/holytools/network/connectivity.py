import datetime
import subprocess  # For executing a shell command
import time
import tabulate


# ----------------------------

class ConnectivityTester:
    def __init__(self, remote_ip_addr : str = '172.217.164.99', remote_name : str = 'google.de', package_size : int = 256):
        self.remote_ip_addr : str = remote_ip_addr
        self.remote_name : str = remote_name
        self.package_size_bytes : int = package_size

    def check_connectivity(self, max_duration : int = 30, verbose : bool = False):
        hosts = [self.remote_ip_addr, self.remote_name]
        ping_timeout = 1
        poll_duration = ping_timeout*len(hosts)

        ping_results = {}
        latencies = {}
        for h in hosts:
            ping_results[h] = []
            latencies[h] = []

        print(f'Launching connectivity tests for {self.remote_name} = {self.remote_ip_addr}. '
              f'\n  - Duration = {max_duration}s'
              f'\n  - Timeout = {ping_timeout}s'
              f'\n  - Package size = {self.package_size_bytes} bytes\n')
        start_time = time.time()
        while time.time() - start_time < max_duration:
            for h in hosts:
                is_reachable = self.is_ping_reachable(ping_timeout, host=h)
                remaining_time = ping_timeout - (time.time() - start_time) % ping_timeout

                ping_results[h].append(is_reachable)
                latencies[h].append(ping_timeout-remaining_time)
                if remaining_time > 0:
                    time.sleep(remaining_time)

            if not verbose:
                continue

            timestamp = datetime.datetime.now()
            timestamp = timestamp.replace(microsecond=0)
            result_msg = f'Success' if all(ping_results[h][-1] for h in hosts) else 'Failure'
            print(f'\nConnectivity results on {timestamp}: {result_msg}')
            for h in hosts:
                ip_reachibility, latency = ping_results[h][-1], latencies[h][-1]
                msg = f'✓ | Latency: {round(latency*1000)} ms' if ip_reachibility else f'✗ (Timeout after {ping_timeout*1000}ms)'
                print(f'    - Connection to {h:<16} {msg}')

        print(f'Summary of connectivity results:')
        table_data = []
        for h in hosts:
            polled_duration = poll_duration*len(ping_results[h])

            uptime = sum(ping_results[h])*poll_duration
            average_latency = f'{sum(latencies[h])/len(latencies[h])*1000:.2f}ms'
            row = [h, f'{uptime}/{polled_duration}s', average_latency]
            table_data.append(row)
        col_headers = ['Host', 'Uptime', 'Average latency']
        print(tabulate.tabulate(tabular_data=table_data, headers=col_headers, tablefmt='psql'))
        print()

    def is_ping_reachable(self, timeout : int, host : str) -> bool:
        if timeout < 1:
            raise ValueError('Timeout must be at least 1 second')

        command = f'ping -w {timeout} -c 1 {host} -s {self.package_size_bytes}'
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) == 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int)
    args = parser.parse_args()


    if not args.duration:
        raise ValueError('Please provide a duration for the connectivity test')

    tester0 = ConnectivityTester(remote_name='chatgpt.com', package_size=512)