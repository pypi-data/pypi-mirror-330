from dataclasses import dataclass
from enum import Enum
from typing import List


class ServerOperationalState(Enum):
    STOPPED = 0
    STARTING = 1
    RUNNING = 2

class ServerAdminState(Enum):
    READY = 0
    MAINTENANCE = 1
    DRAIN = 2
    MAINT = 3
    DRAIN_WAIT = 4
    MAINT_WAIT = 5

@dataclass
class Server:
    id: int
    name: str
    address: str
    operational_state: ServerOperationalState
    admin_state: ServerAdminState
    user_weight: int
    initial_weight: int
    time_since_last_change: int
    check_status: int
    check_result: int
    check_health: int
    check_state: int
    port: int

    def enable(self, client, backend):
        response = client.send_command(f'enable server {backend.name}/{self.name}')
        if len(response) == 1 and response.isspace():
            return False
        return True
        pass

    def disable(self, client):
        pass


@dataclass
class Backend:
    id: int
    name: str
    servers: List[Server]

    def get_servers(self, client):
        response = client.get_stats(f"{self.name} 4 -1")
        return response


@dataclass
class Frontend:
    name: str
    bind_address: str
    bind_port: int
    status: str
    connections: int
    bytes_in: int
    bytes_out: int

@dataclass
class HAProxyInfo:
    version: str
    release_date: str
    nbproc: int
    process_num: int
    pid: int
    uptime: int
    mem_max_mb: int
    ulimit_n: int
    max_sock: int
    max_conn: int
    max_pipes: int
    curr_conns: int
    pipes_used: int
    pipes_free: int
    conn_rate: int
    conn_rate_limit: int
    max_conn_rate: int
    sess_rate: int
    sess_rate_limit: int
    max_sess_rate: int
    ssl_rate: int
    ssl_rate_limit: int
    max_ssl_rate: int
    ssl_frontend_key_rate: int
    ssl_frontend_max_key_rate: int
    ssl_frontend_session_reuse_pct: float
    ssl_backend_key_rate: int
    ssl_backend_max_key_rate: int
    ssl_cache_lookups: int
    ssl_cache_misses: int
    compress_bps_in: int
    compress_bps_out: int
    compress_bps_rate_limit: int
    zlib_mem_usage: int
    max_zlib_mem_usage: int

@dataclass
class Stats:
    uptime: int
    current_connections: int
    max_connections: int
    total_connections: int
    connections_rate: int
    bytes_in: int
    bytes_out: int