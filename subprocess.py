import subprocess
from ipaddress import ip_address, IPv4Address
from tabulate import tabulate


def host_ping(hosts):
    for host in hosts:
        try:
            ip = ip_address(host)
            result = subprocess.run(
                ['ping', '-c', '1', str(ip)], capture_output=True)
            if result.returncode == 0:
                print(f" {host} availible")
            else:
                print(f" {host} not availible")
        except ValueError:
            print(f" incorrect address {host}")


def host_range_ping(start_ip, end_ip):
    start = IPv4Address(start_ip)
    end = IPv4Address(end_ip)

    for ip in range(int(start), int(end)+1):
        try:
            result = subprocess.run(
                ['ping', '-c', '1', str(IPv4Address(ip))], capture_output=True)
            if result.returncode == 0:
                print(f"{IPv4Address(ip)} availible")
            else:
                print(f"{IPv4Address(ip)} not availible")
        except ValueError:
            print(f"incorrect address {IPv4Address(ip)}")


def host_range_ping_tab(ip_range):
    reachable = []
    unreachable = []
    for i in range(ip_range[0], ip_range[1]+1):
        ip = ip_address('10.0.0.' + str(i))
        result = subprocess.run(
            ['ping', '-n', '1', '-w', '100', str(ip)], stdout=subprocess.PIPE)
        if result.returncode == 0:
            reachable.append(str(ip))
        else:
            unreachable.append(str(ip))

    table = [
        ['Reachable'] + reachable,
        ['Unreachable'] + unreachable
    ]

    print(tabulate(table))


num_clients = 3
client_procs = []

for i in range(num_clients):
    proc = subprocess.Popen(["python", "client.py"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    client_procs.append(proc)

for proc in client_procs:
    proc.wait()


if __name__ == '__main__':
    hosts = ['8.8.8.8', 'google.com', 'invalid', '127.0.0.1']
    host_ping(hosts)
    start_ip = '193.167.0.0'
    end_ip = '193.167.0.11'
    host_range_ping(start_ip, end_ip)
    host_range_ping_tab([1, 4])
