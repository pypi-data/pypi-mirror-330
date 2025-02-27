"""Provide builting schedulers"""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from diot import Diot
from xqute import Scheduler
from xqute.schedulers.local_scheduler import LocalScheduler as XquteLocalScheduler
from xqute.schedulers.sge_scheduler import SgeScheduler as XquteSgeScheduler
from xqute.schedulers.slurm_scheduler import SlurmScheduler as XquteSlurmScheduler
from xqute.schedulers.ssh_scheduler import SshScheduler as XquteSshScheduler
from xqute.schedulers.gbatch_scheduler import GbatchScheduler as XquteGbatchScheduler
from xqute.path import DualPath

from .defaults import SCHEDULER_ENTRY_GROUP
from .exceptions import NoSuchSchedulerError, WrongSchedulerTypeError
from .job import Job
from .utils import is_subclass, load_entrypoints

if TYPE_CHECKING:
    from .proc import Proc


class SchedulerPostInit:
    """Provides post init function for all schedulers"""

    job_class = Job

    MOUNTED_METADIR: str
    MOUNTED_OUTDIR: str

    def post_init(self, proc: Proc) -> None:
        ...


class LocalScheduler(SchedulerPostInit, XquteLocalScheduler):
    """Local scheduler"""


class SgeScheduler(SchedulerPostInit, XquteSgeScheduler):
    """SGE scheduler"""


class SlurmScheduler(SchedulerPostInit, XquteSlurmScheduler):
    """Slurm scheduler"""


class SshScheduler(SchedulerPostInit, XquteSshScheduler):
    """SSH scheduler"""


class GbatchScheduler(SchedulerPostInit, XquteGbatchScheduler):
    """Google Cloud Batch scheduler"""

    MOUNTED_METADIR: str = "/mnt/pipen-pipeline/workdir"
    MOUNTED_OUTDIR: str = "/mnt/pipen-pipeline/outdir"

    def post_init(self, proc: Proc):
        super().post_init(proc)

        mounted_workdir = f"{self.MOUNTED_METADIR}/{proc.name}"
        self.workdir: DualPath = DualPath(self.workdir.path, mounted=mounted_workdir)

        # update the mounted metadir
        self.config.taskGroups[0].taskSpec.volumes[-1].mountPath = mounted_workdir

        # update the config to map the outdir to vm
        self.config.taskGroups[0].taskSpec.volumes.append(
            Diot(
                {
                    "gcs": {
                        "remotePath": proc.pipeline.outdir._no_prefix,  # type: ignore
                    },
                    "mountPath": self.MOUNTED_OUTDIR,
                }
            )
        )


def get_scheduler(scheduler: str | Type[Scheduler]) -> Type[Scheduler]:
    """Get the scheduler by name of the scheduler class itself

    Args:
        scheduler: The scheduler class or name

    Returns:
        The scheduler class
    """
    if is_subclass(scheduler, Scheduler):
        return scheduler  # type: ignore

    if scheduler == "local":
        return LocalScheduler

    if scheduler == "sge":
        return SgeScheduler

    if scheduler == "slurm":
        return SlurmScheduler

    if scheduler == "ssh":
        return SshScheduler

    if scheduler == "gbatch":
        return GbatchScheduler

    for n, obj in load_entrypoints(SCHEDULER_ENTRY_GROUP):  # pragma: no cover
        if n == scheduler:
            if not is_subclass(obj, Scheduler):
                raise WrongSchedulerTypeError(
                    "Scheduler should be a subclass of " "pipen.scheduler.Scheduler."
                )
            return obj

    raise NoSuchSchedulerError(str(scheduler))
