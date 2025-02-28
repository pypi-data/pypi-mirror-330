# pylint: disable=E1101,W0603
# Standard Library
import json
import os

# Third Party
from celery import Celery
from celery.utils.log import get_task_logger

from vcs_scanner.api.constants import TEMP_RULE_DIR_FILE, TEMP_RULE_FILE, TEMP_RULE_REPO_FILE
from vcs_scanner.api.schema.repository import Repository

# First Party
from vcs_scanner.common import initialise_logs, load_vcs_instances
from vcs_scanner.constants import LOG_FILE_PATH
from vcs_scanner.helpers.environment_wrapper import validate_environment
from vcs_scanner.helpers.providers.rule_file import RuleFileProvider
from vcs_scanner.helpers.providers.rule_tag import RuleTagProvider
from vcs_scanner.model import RepositoryRuntime
from vcs_scanner.output_modules.rws_api_writer import RESTAPIWriter
from vcs_scanner.post_processing.post_processor import PostProcessor
from vcs_scanner.secret_scanners.configuration import (
    GITLEAKS_PATH,
    RABBITMQ_DEFAULT_VHOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_QUEUE,
    RABBITMQ_SERVICE_HOST,
    RABBITMQ_USERNAME,
    REQUIRED_ENV_VARS,
    RESC_API_NO_AUTH_SERVICE_HOST,
    RESC_API_NO_AUTH_SERVICE_PORT,
    RESC_IGNORE_TAGS,
    RESC_INCLUDE_TAGS,
    VCS_INSTANCES_FILE_PATH,
)
from vcs_scanner.secret_scanners.secret_scanner import SecretScanner

env_variables = validate_environment(REQUIRED_ENV_VARS)
app = Celery(
    "secret_scanner_worker",
    broker="amqp://"
    + f"{env_variables[RABBITMQ_USERNAME]}"
    + ":"
    + f"{env_variables[RABBITMQ_PASSWORD]}"
    + "@"
    + f"{env_variables[RABBITMQ_SERVICE_HOST]}"
    + "/"
    + f"{env_variables[RABBITMQ_DEFAULT_VHOST]}",
)
app.conf.update({"worker_hijack_root_logger": False})
app.conf.update({"broker_connection_retry": True})
app.conf.update({"broker_connection_max_retries": 100})

logger = get_task_logger(__name__)
logger_config = initialise_logs(LOG_FILE_PATH)
rabbitmq_queue = env_variables[RABBITMQ_QUEUE]
rws_url = f"http://{env_variables[RESC_API_NO_AUTH_SERVICE_HOST]}:{env_variables[RESC_API_NO_AUTH_SERVICE_PORT]}"
rws_writer: RESTAPIWriter = RESTAPIWriter(rws_url=rws_url)

VCS_INSTANCES_LIST = None
VCS_INSTANCES = None
DOWNLOADED_RULE_PACK_VERSION = None


@app.task(name="scan_repository", Queue=rabbitmq_queue)
def scan_repository(repository):
    global VCS_INSTANCES_LIST, VCS_INSTANCES, DOWNLOADED_RULE_PACK_VERSION
    if not VCS_INSTANCES_LIST:
        VCS_INSTANCES_LIST = load_vcs_instances(env_variables[VCS_INSTANCES_FILE_PATH])
    if not VCS_INSTANCES:
        VCS_INSTANCES = rws_writer.write_vcs_instances(VCS_INSTANCES_LIST)
    if not DOWNLOADED_RULE_PACK_VERSION:
        DOWNLOADED_RULE_PACK_VERSION = rws_writer.download_rule_pack()

    active_rule_pack_version = rws_writer.check_active_rule_pack_version(rule_pack_version=DOWNLOADED_RULE_PACK_VERSION)

    repository_runtime = RepositoryRuntime(**json.loads(repository))

    logger.info(
        f"Received repository to scan via the queue '{rabbitmq_queue}' => "
        f"{repository_runtime.project_key}/{repository_runtime.repository_name}"
    )
    try:
        vcs_instance = VCS_INSTANCES[repository_runtime.vcs_instance_name]

        repository = Repository(
            project_key=repository_runtime.project_key,
            repository_id=repository_runtime.repository_id,
            repository_name=repository_runtime.repository_name,
            repository_url=repository_runtime.repository_url,
            vcs_instance=vcs_instance.id_,
        )
        # Split the include_tags by comma if supplied
        include_tags = env_variables[RESC_INCLUDE_TAGS].split(",") if env_variables[RESC_INCLUDE_TAGS] else []
        include_tags = list(set(include_tags) | set(vcs_instance.include_tags))

        # Split the ignore_tags by comma if supplied
        ignore_tags = env_variables[RESC_IGNORE_TAGS].split(",") if env_variables[RESC_IGNORE_TAGS] else []
        ignore_tags = list(set(ignore_tags) | set(vcs_instance.ignore_tags))

        logger.debug(
            f"include_tags for vcs {repository_runtime.vcs_instance_name}: "
            f"{include_tags}, "
            f"ignore_tags for vcs {repository_runtime.vcs_instance_name}: "
            f"{ignore_tags}"
        )

        rule_tag_provider = RuleTagProvider()
        rule_tag_provider.load(TEMP_RULE_FILE)

        rest_api_writer = RESTAPIWriter(
            rws_url=rws_url, include_tags=include_tags, ignore_tags=ignore_tags, rule_tag_provider=rule_tag_provider
        )
        post_processor = PostProcessor(rule_tag_provider=rule_tag_provider)

        gitleaks_rules_provider = RuleFileProvider(TEMP_RULE_FILE)
        gitleaks_rules_provider.init(
            destination_rule_as_repo=TEMP_RULE_REPO_FILE,
            destination_rule_as_dir=TEMP_RULE_DIR_FILE,
        )

        secret_scanner = SecretScanner(
            gitleaks_binary_path=env_variables[GITLEAKS_PATH],
            gitleaks_rules_provider=gitleaks_rules_provider,
            rule_pack_version=active_rule_pack_version,
            output_plugin=rest_api_writer,
            post_processor=post_processor,
            repository=repository,
            username=vcs_instance.username,
            personal_access_token=vcs_instance.token,
            force_base_scan=os.getenv("FORCE_BASE_SCAN", "false").lower() in "true",
            latest_commit=repository_runtime.latest_commit,
        )

        secret_scanner.run_scan(as_dir=True, as_repo=True)
    except KeyError:
        logger.error(
            f"No configuration found for vcs instance {repository_runtime.vcs_instance_name}, "
            f"unable to scan {repository_runtime.project_key}/{repository_runtime.repository_name}"
        )
