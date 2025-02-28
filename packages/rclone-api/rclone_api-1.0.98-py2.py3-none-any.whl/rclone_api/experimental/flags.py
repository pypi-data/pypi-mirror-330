from dataclasses import dataclass, field


@dataclass
class CopyFlags:
    check_first: bool = False
    checksum: bool = False
    ignore_existing: bool = False
    ignore_times: bool = False
    immutable: bool = False
    inplace: bool = False
    links: bool = False
    metadata: bool = False


@dataclass
class SyncFlags:
    backup_dir: str | None = None
    delete_after: bool = False
    delete_before: bool = False
    delete_during: bool = False
    ignore_errors: bool = False
    track_renames: bool = False


@dataclass
class ImportantFlags:
    dry_run: bool = False
    interactive: bool = False
    verbose: int = 0  # 0 = default, 1 = -v, 2 = -vv, etc.


@dataclass
class NetworkingFlags:
    bwlimit: str | None = None
    timeout: str | None = "5m0s"
    tpslimit: float | None = None
    user_agent: str | None = "rclone/v1.69.1"


@dataclass
class PerformanceFlags:
    buffer_size: str | None = "16MiB"
    checkers: int = 8
    transfers: int = 4


@dataclass
class ConfigFlags:
    config: str | None = None
    ask_password: bool = True
    auto_confirm: bool = False


@dataclass
class DebuggingFlags:
    cpuprofile: str | None = None
    memprofile: str | None = None


@dataclass
class FilterFlags:
    exclude: list[str] = field(default_factory=list)
    include: list[str] = field(default_factory=list)
    max_age: str | None = None
    min_size: str | None = None


@dataclass
class ListingFlags:
    fast_list: bool = False


@dataclass
class LoggingFlags:
    log_file: str | None = None
    log_level: str = "NOTICE"  # Options: DEBUG, INFO, NOTICE, ERROR
    stats: str | None = "1m0s"
    progress: bool = False


@dataclass
class Flags:
    copy: CopyFlags | None = None
    sync: SyncFlags | None = None
    important: ImportantFlags | None = None
    networking: NetworkingFlags | None = None
    performance: PerformanceFlags | None = None
    config: ConfigFlags | None = None
    debugging: DebuggingFlags | None = None
    filter: FilterFlags | None = None
    listing: ListingFlags | None = None
    logging: LoggingFlags | None = None
