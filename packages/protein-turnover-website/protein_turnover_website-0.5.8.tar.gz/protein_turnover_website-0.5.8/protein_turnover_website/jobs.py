from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from dataclasses import replace
from pathlib import Path

from flask import abort
from flask import current_app
from flask import Flask
from flask import request
from protein_turnover.background import SimpleQueueClient
from protein_turnover.jobs import PeptideSettings
from protein_turnover.jobs import TurnoverJob

from .explorer.explorer import find_mountpoint_for
from .explorer.explorer import get_mountpoints
from .explorer.explorer import logger
from .explorer.explorer import safe_repr
from .flask_utils import oktokill
from .jobsmanager import JobsManager
from .jobsmanager import PersonalJobsManager


def oktokill_abort() -> None:
    if not oktokill():
        abort(404)


def sanitize(job: TurnoverJob) -> TurnoverJob:
    mountpoints = get_mountpoints()

    def rep(p: str) -> str:
        mp, fname = safe_repr(Path(p), mountpoints)
        return f"<b>{mp.label}</b>:{fname}"

    return replace(
        job,
        pepxml=[rep(f) for f in job.pepxml],
        protxml=rep(job.protxml),
        mzmlfiles=[rep(f) for f in job.mzmlfiles],
    )


@dataclass
class File:
    # what was loaded into hidden value object in jobs.ts
    mountpoint: str
    parent: str
    files: list[str]

    @classmethod
    def from_files(cls, files: list[str]) -> File:
        if len(files) == 0:
            return File("", "", [])

        mountpoints = get_mountpoints()
        paths = [Path(f).resolve() for f in files]
        mp = find_mountpoint_for(paths[0], mountpoints)
        if mp is None:
            return File("", "", [])
        parent = paths[0].parent.relative_to(mp.mountpoint)
        return File(mp.label, str(parent), [p.name for p in paths])

    @property
    def tojson(self) -> str:
        if len(self.files) == 0:
            return ""
        return json.dumps(asdict(self))

    def to_realfiles(self) -> list[Path]:
        if len(self.files) == 0:
            abort(404)
        if Path(self.parent).is_absolute():  # expecting only relative paths
            abort(404)
        if any(Path(f).is_absolute() for f in self.files):
            abort(404)
        mountpoints = get_mountpoints()
        m = mountpoints.get(self.mountpoint)
        if m is None:  # unknown mountpoint
            abort(404)
        assert m is not None
        return [m.mountpoint.joinpath(self.parent, f) for f in self.files]


def input2files(key: str) -> list[Path]:
    return File(**json.loads(request.form[key])).to_realfiles()


def job_from_form(jobid: str) -> TurnoverJob:
    if (
        not request.form["pepxmlfiles"]
        or not request.form["mzmlfiles"]
        or not request.form["protxmlfile"]
    ):
        abort(404)

    CVT = dict(
        float=float,
        str=str,
        int=int,
        bool=lambda v: v.lower() in {"yes", "y", "1", "true"},
    )
    res = {}
    for field in fields(PeptideSettings):
        if field.name in request.form:
            t = "str" if field.type.startswith("Literal") else str(field.type)
            val = CVT[t](request.form[field.name])  # type: ignore
            res[field.name] = val

    settings = PeptideSettings(**res)
    if "mzTolerance" in res:
        settings = replace(settings, mzTolerance=settings.mzTolerance / 1e6)

    try:
        pepxmlfiles = input2files("pepxmlfiles")
        protxmlfile = input2files("protxmlfile")
        mzmlfiles = input2files("mzmlfiles")
    except (TypeError, UnicodeDecodeError):
        abort(404)

    if (
        not pepxmlfiles
        or not protxmlfile
        or not mzmlfiles
        or not all(f.exists() for f in protxmlfile)
        or not all(f.exists() for f in mzmlfiles)
        or not all(f.exists() for f in pepxmlfiles)
    ):
        logger.error(
            'job_from_form: no files found: pepxml="%s" protxml="%s" mzml="%s"',
            pepxmlfiles,
            protxmlfile,
            mzmlfiles,
        )
        abort(404)

    match_runNames = request.form.get("match_runNames", "no") == "yes"

    cachedir: str | None = current_app.config.get("CACHEDIR")
    email = request.form.get("email", None)
    if email == "":
        email = None
    jobby = TurnoverJob(
        job_name=request.form.get("job_name", jobid),
        pepxml=[str(s) for s in pepxmlfiles],
        protxml=str(protxmlfile[0]),
        mzmlfiles=[str(s) for s in mzmlfiles],
        settings=settings,
        jobid=jobid,
        cache_dir=str(cachedir) if cachedir else None,
        email=email,
        match_runNames=match_runNames,
    )
    return jobby


def get_bg_client() -> SimpleQueueClient:
    return current_app.extensions["bgclient"]


def get_jobs_manager() -> JobsManager:
    return current_app.extensions["jobsmanager"]


def create_jobs_manager(app: Flask, jobsdir: Path) -> JobsManager:
    website_state = app.config.get("WEBSITE_STATE", "multi_user")
    jobsdir = jobsdir.resolve()
    manager = (
        JobsManager(jobsdir, check_dir=True)
        if website_state == "multi_user"
        else PersonalJobsManager(jobsdir, check_dir=True)
    )
    if not jobsdir.exists():
        jobsdir.mkdir(parents=True, exist_ok=True)
        new_layout = True
    else:
        new_layout = manager.check_config()

    if new_layout:
        if website_state != "multi_user":
            manager.sub_directories = 0  # don't create subdirectories for single_user
        manager.write_config()
    if website_state != "multi_user":
        app.logger.info(
            "JOBSDIR: %s (%s)",
            jobsdir,
            "new" if new_layout else "existing",
        )
    return manager


def ensure_cachedir(app: Flask) -> None:
    cachedir = app.config.get("CACHEDIR")
    if not cachedir:
        return

    path = Path(cachedir).expanduser()

    app.config["CACHEDIR"] = path


def ensure_jobsdir(app: Flask) -> None:
    jobsdir = app.config.get("JOBSDIR")
    if not jobsdir:
        app.logger.error("need config.JOBSDIR directory")
        raise RuntimeError("need config.JOBSDIR directory")

    path = Path(jobsdir).expanduser()

    app.config["JOBSDIR"] = path
    app.extensions["bgclient"] = SimpleQueueClient(path)
    app.extensions["jobsmanager"] = create_jobs_manager(app, path)


def view_jobsdir(app: Flask) -> None:
    jobsdir = app.config.get("JOBSDIR")
    if not jobsdir:
        app.logger.error("need config.JOBSDIR directory")
        raise RuntimeError("need config.JOBSDIR directory")

    path = Path(jobsdir).expanduser()

    app.config["JOBSDIR"] = path
    app.extensions["bgclient"] = SimpleQueueClient(path)
    app.extensions["jobsmanager"] = PersonalJobsManager(path, sub_directories=0)
