# Standard Library
import abc

# Third Party
from vcs_scanner.api.schema.finding import FindingCreate
from vcs_scanner.api.schema.repository import Repository, RepositoryBase
from vcs_scanner.api.schema.scan import Scan, ScanRead
from vcs_scanner.api.schema.scan_type import ScanType
from vcs_scanner.api.schema.vcs_instance import VCSInstanceRead

# First Party
from vcs_scanner.model import VCSInstanceRuntime


class OutputModule(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_rules(self, toml_rule_file_path: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def write_vcs_instance(self, vcs_instance_runtime: VCSInstanceRuntime) -> VCSInstanceRead | None:
        raise NotImplementedError

    @abc.abstractmethod
    def write_repository(self, repository: Repository) -> RepositoryBase | None:
        raise NotImplementedError

    @abc.abstractmethod
    def write_findings(
        self,
        scan_id: int,
        repository_id: int,
        scan_findings: list[FindingCreate],
        repository_name: str = "",
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def write_scan(
        self,
        scan_type_to_run: ScanType,
        last_scanned_commit: str,
        scan_timestamp: str,
        repository: Repository,
        rule_pack: str,
    ) -> Scan:
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_scan_for_repository(self, repository: Repository) -> ScanRead | None:
        raise NotImplementedError
