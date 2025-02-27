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

import click
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import CtxpException, recent

from hcs_cli.service import task


@click.group(name="task")
def task_cmd_group():
    pass


@task_cmd_group.command("namespaces")
def list_namespaces(**kwargs):
    """List namespaces"""
    return task.namespaces()


@task_cmd_group.command()
@click.argument("smart_path", type=str, required=False)
def use(smart_path: str, **kwargs):
    """Use a namespace"""
    if smart_path:
        namespace, group, key = _parse_task_param(smart_path)

    else:
        namespace = recent.get("task_namespace")
        group = recent.get("task_group")
        key = recent.get("task_key")
        return f"{namespace}/{group}/{key}"


@task_cmd_group.command()
@click.option("--namespace", "-n", type=str, required=False)
@cli.search
def list(namespace: str, search: str, **kwargs):
    """List tasks."""
    if namespace:
        recent.set("task_namespace", namespace)
    else:
        namespace = recent.get("task_namespace")
        if not namespace:
            return "Missing recent namespace. Specify '--namespace'.", 1
    return task.query(namespace, search, **kwargs)


@task_cmd_group.command()
@click.argument("smart_path", type=str, required=False)
@cli.org_id
def get(smart_path: str, org: str, **kwargs):
    """Get a task."""
    namespace, group, key = _parse_task_param(smart_path)
    org_id = cli.get_org_id(org)
    return task.get(org_id, namespace, group, key, **kwargs)


@task_cmd_group.command()
@click.argument("smart_path", type=str, required=False)
@cli.confirm
def delete(smart_path: str, confirm: bool, **kwargs):
    """Delete a task."""
    namespace, group, key = _parse_task_param(smart_path)

    ret = task.get(namespace, key, **kwargs)
    if not ret:
        return "", 1

    if not confirm:
        click.confirm(
            f"Delete task {namespace}/{group}/{key}? (type={ret['type']}, worker={ret['worker']})", abort=True
        )
    return task.delete(namespace, group, key, **kwargs)


@task_cmd_group.command()
@click.argument("smart_path", type=str, required=False)
@click.option("--last", is_flag=True, default=False, help="If specified, return only the last log instead of all logs.")
@cli.search
@cli.org_id
def logs(smart_path: str, last: bool, search: str, org: str, **kwargs):
    """List task logs."""
    namespace, group, key = _parse_task_param(smart_path)
    org_id = cli.get_org_id(org)
    if last:
        t = task.last(org_id, namespace, group, key, **kwargs)
        if t:
            return t.log
        else:
            return
    else:
        return task.logs(org_id, namespace, group, key, search, **kwargs)


@task_cmd_group.command()
@click.argument("smart_path", type=str, required=False)
@click.option(
    "--states",
    "-s",
    type=str,
    required=False,
    default="Success",
    help="Comma separated states to wait for. Valid values: Success, Error, Canceled, Running, Init.",
)
@cli.wait
@cli.org_id
def wait(smart_path: str, wait: str, states: str, org: str, **kwargs):
    """Wait for a specific task"""
    namespace, group, key = _parse_task_param(smart_path)
    org_id = cli.get_org_id(org)
    return task.wait(org_id=org_id, namespace=namespace, group=group, key=key, wait=wait, states=states, **kwargs)


def _parse_task_param(smart_path: str):
    if smart_path:
        parts = smart_path.split("/")
        if len(parts) == 3:
            namespace, group, key = parts
            if not namespace:
                raise CtxpException("Missing namespace. Valid example: <namespace>/<group>/<key>.")
            if not group:
                raise CtxpException("Missing group. Valid example: <namespace>/<group>/<key>.")
            if not key:
                raise CtxpException("Missing key. Valid example: <namespace>/<group>/<key>.")

            recent.set("task_namespace", namespace)
            recent.set("task_group", group)
            recent.set("task_key", key)
        elif len(parts) == 2:
            namespace = recent.require(parts[0], "task_namespace")
            group = recent.require("default", "task_group")
            key = recent.require(parts[1], "task_key")
        elif len(parts) == 1:
            namespace = recent.get("task_namespace")
            group = recent.get("task_group")
            key = parts[0]
            if not key:
                raise CtxpException("Missing key. Valid example: <namespace>/<group>/<key>.")
            recent.set("task_key", key)

            if not namespace:
                raise CtxpException(
                    "Missing recent namespace. Valid example: <namespace>/<group>/<key>, or use 'task use <namespace>/<group>'."
                )
            if not group:
                raise CtxpException(
                    "Missing recent group. Valid example: <namespace>/<group>/<key>, or use 'task use <namespace>/<group>'."
                )
    else:
        namespace = recent.get("task_namespace")
        group = recent.get("task_group")
        key = recent.get("task_key")
        if not namespace:
            raise CtxpException(
                "Missing recent namespace. Valid example: <namespace>/<group>/<key>, or use 'task use <namespace>/<group>'."
            )
        if not group:
            raise CtxpException(
                "Missing recent group. Valid example: <namespace>/<group>/<key>, or use 'task use <namespace>/<group>'."
            )
        if not key:
            raise CtxpException(
                "Missing recent key. Valid example: <namespace>/<group>/<key>, or use 'task use <namespace>/<group>'."
            )
    return namespace, group, key
