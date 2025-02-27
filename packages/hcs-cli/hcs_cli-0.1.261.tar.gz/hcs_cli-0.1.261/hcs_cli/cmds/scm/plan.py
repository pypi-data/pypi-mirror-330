"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import re
import sys
from os import path

import click
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent
from hcs_core.sglib.client_util import wait_for_res_status

import hcs_cli.service.scm as scm


@click.group
def plan():
    """Commands for calendar plans."""
    # return scm.health()
    pass


@plan.command
@cli.org_id
def list(org: str, **kwargs):
    """List named calendar plans."""
    org = cli.get_org_id(org)
    return scm.plan.list(org_id=org, **kwargs)


@plan.command
@cli.org_id
@click.argument("name", required=False)
def get(org: str, name: str, **kwargs):
    """Get a named calendar plan."""
    org = cli.get_org_id(org)
    name = recent.require(name, "scm.plan")
    ret = scm.plan.get(org_id=org, id=name, **kwargs)
    if ret is None:
        return "", 1
    return ret


@plan.command
@cli.org_id
@click.argument("name", required=False)
@cli.confirm
def delete(org: str, name: str, confirm: bool, **kwargs):
    """Delete a named calendar plan, or specific daily or slot config."""
    org = cli.get_org_id(org)
    name = recent.require(name, "scm.plan")

    ret = scm.plan.get(org_id=org, id=name, **kwargs)
    if not ret:
        return "", 1

    if not confirm:
        click.confirm(f"Delete calendar plan {name}?", abort=True)

    ret = scm.plan.delete(org_id=org, id=name, **kwargs)
    if ret is None:
        return "", 1


@plan.command
@cli.org_id
@cli.limit
@click.option("--day", required=False, help="Optional. Search by day-identifier.")
@click.option("--slot", required=False, help="Optional. Search by time slot.")
@click.option(
    "--state",
    "-s",
    required=False,
    type=str,
    help="Optional. Search by task state, as comma-separated values. E.g. 'init,running,success,error'.",
)
@click.argument("name", required=False)
def tasks(org: str, limit: int, day: str, slot: str, name: str, state: str, **kwargs):
    """Get tasks of a named calendar plan."""
    org = cli.get_org_id(org)

    name = recent.require(name, "scm.plan")

    if not day and slot and slot.find("/") > 0:
        day, slot = slot.split("/")

    if not state:
        state = "success,error"
    elif state.lower() == "all" or state.lower() == "any":
        state = "init,running,success,error"
    else:
        pass  # use API defaults.

    ret = scm.plan.tasks(org_id=org, id=name, limit=limit, day=day, slot=slot, states=state, **kwargs)
    if ret is None:
        return "", 1
    return ret


@plan.command
@cli.org_id
@click.argument("name", required=False)
@click.argument("task-key", required=False)
def task(org: str, name: str, task_key: str, **kwargs):
    """Get task by key."""
    org = cli.get_org_id(org)
    name = recent.require(name, "scm.plan")
    task_key = recent.require(task_key, "scm.task_key")

    ret = scm.plan.get_task(org_id=org, id=name, task_key=task_key, **kwargs)
    if ret is None:
        return "", 1
    return ret


@plan.command
@cli.org_id
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the template file name. If not specified, STDIN will be used.",
)
@click.option(
    "--predefined",
    "-p",
    required=False,
    help="Use a predefined template.",
)
def create(org: str, file, predefined: str, **kwargs):
    """Create a named calendar plan."""
    org = cli.get_org_id(org)

    if predefined:
        file_name = path.join(path.dirname(__file__), f"../../payload/scm/{predefined}.json")
        file_name = path.abspath(file_name)
        with open(file_name, "rt") as f:
            text = f.read()
    else:
        with file:
            text = file.read()

    try:
        payload = json.loads(text)
    except Exception as e:
        msg = "Invalid template: " + str(e)
        return msg, 1

    name = payload["name"]
    recent.set("scm.plan", name)

    return scm.plan.create(org_id=org, name=name, payload=payload, **kwargs)


@plan.command
@cli.org_id
@click.argument("name", required=False)
@click.option("--slot", "-s", required=True, type=str, help="Example: Mon/13:30")
@click.option("--config", "-c", required=True, type=str, help='Example: {"mydata":1}')
def update(org: str, name: str, slot: str, config: str, **kwargs):
    """Update a named calendar plan, or its slot config."""
    org = cli.get_org_id(org)
    name = recent.require(name, "scm.plan")

    day, slot_time = slot.split("/")
    slot_config = json.loads(config)

    payload = scm.plan.get(org_id=org, id=name)
    if not payload:
        return "Not found", 1
    payload[day][slot_time] = slot_config

    return scm.plan.update(org_id=org, name=name, payload=payload, **kwargs)


@plan.command
@cli.org_id
@click.argument("name", required=False)
@click.option("--slot", "-s", required=False, type=str, help="Run with config at this time slot. Example: Mon/13:30.")
@click.option("--config", "-c", required=False, type=str, help='Run with a custom config. Example: {"mydata":1}')
@cli.wait
def run(org: str, name: str, slot: str, config: str, wait: str, **kwargs):
    """Run task now, with slot config or custom config."""
    org = cli.get_org_id(org)
    name = recent.require(name, "scm.plan")

    if slot and config:
        return "--slot and --config can not be used together", 2

    while True:
        if slot:
            slot = slot.strip().lower()
            if not _validate_slot_format(slot):
                return "Invalid slot format. Example: with weekday name 'Mon/13:00', or with day of month '11/13:30'", 1
            ret = scm.plan.run(org_id=org, id=name, slot=slot, payload={})
            if not ret:
                "", 1
            break

        if config:
            slot_config = json.loads(config)
            ret = scm.plan.run(org_id=org, id=name, payload=slot_config)
            if not ret:
                return "", 1
            break

        ret = scm.plan.run(org_id=org, id=name, payload={})
        if not ret:
            return "", 1
        break

    # print(json.dumps(ret, indent=4))
    task_key = ret["group"] + ":" + ret["key"]
    recent.set("scm.task_key", task_key)

    if wait and wait != "0":
        return _wait_for_task(org, name, task_key, wait)
    else:
        return ret


def _wait_for_task(org_id: str, name: str, task_key: str, timeout: str):

    return wait_for_res_status(
        resource_name=name + "/" + task_key,
        fn_get=lambda: scm.plan.get_task(org_id, name, task_key),
        get_status=lambda t: t["log"]["state"],
        status_map={"ready": "Success", "error": "Error", "transition": ["Running", "Init"]},
        timeout=timeout,
    )


def _validate_slot_format(slot: str):
    pattern = "^(?:(?:mon|tue|wed|thu|fri|sat|sun|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|(?:0?[1-9]|[12][0-9]|3[01]))/(?:[01]?[0-9]|2[0-3]):[0-5][0-9]$"
    p = re.compile(pattern)
    if p.match(slot):
        return True
