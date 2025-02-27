"""
Copyright 2020 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import logging

import pytest
import ssh_container
from pytest_inmanta.plugin import Project

import inmanta.const

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    ["package_name"],
    [
        ("wget",),
    ],
)
def test_model(
    project: Project,
    remote_ssh_container: ssh_container.SshContainer,
    package_name: str,
    purged: bool = False,
) -> None:
    model = f"""
    import unittest
    import yum
    import mitogen

    svc = yum::Package(host=host, name="{package_name}", purged={str(purged).lower()})
    host = std::Host(
        name="server",
        os=std::linux,
        via=mitogen::Sudo(
            via=mitogen::Ssh(
                name="server",
                hostname={repr(remote_ssh_container.get_container_host_ip())},
                port={remote_ssh_container.get_exposed_port(remote_ssh_container.port)},
                username="user",
                python_path=["/usr/libexec/platform-python"],
                identity_file={repr(remote_ssh_container.private_key_file)},
                check_host_keys="ignore",
                via=null,
            ),
        ),
    )
    """

    project.compile(model)
    assert all(r.send_event for r in project.resources.values())


def test_handler(
    project: Project,
    remote_ssh_container: ssh_container.SshContainer,
) -> None:
    # Deploy wget package
    test_model(project, remote_ssh_container, package_name="wget")

    assert project.dryrun_resource("yum::Package")
    project.deploy_resource("yum::Package", run_as_root=False)
    assert not project.dryrun_resource("yum::Package")

    # delete wget package
    test_model(project, remote_ssh_container, package_name="wget", purged=True)

    assert project.dryrun_resource("yum::Package")
    project.deploy_resource("yum::Package", run_as_root=False)
    assert not project.dryrun_resource("yum::Package")

    # Try to deploy a package that doesn't exist
    test_model(project, remote_ssh_container, package_name="package_that_doesnt_exist")

    svc = project.get_resource("yum::Package", name="package_that_doesnt_exist")
    assert svc
    ctx = project.deploy(svc, run_as_root=False)
    assert ctx.status == inmanta.const.ResourceState.failed
    assert ctx.change == inmanta.const.Change.nochange
    assert (
        "Yum failed: stdout: errout: Error: Unable to find a match: package_that_doesnt_exist"
        in ctx.logs[-1].msg
    )


def test_batch_packages_model(
    project: Project,
    remote_ssh_container: ssh_container.SshContainer,
    package_names: list[str] = ["vim", "nano"],
    purged: bool = False,
) -> None:
    model = f"""
    import unittest
    import yum
    import mitogen

    svc = yum::PackagesBatch(
        name="my_batch",
        host=host,
        packages={package_names},
        purged={str(purged).lower()},
    )
    host = std::Host(
        name="server",
        os=std::linux,
        via=mitogen::Sudo(
            via=mitogen::Ssh(
                name="server",
                hostname={repr(remote_ssh_container.get_container_host_ip())},
                port={remote_ssh_container.get_exposed_port(remote_ssh_container.port)},
                username="user",
                python_path=["/usr/libexec/platform-python"],
                identity_file={repr(remote_ssh_container.private_key_file)},
                check_host_keys="ignore",
                via=null,
            ),
        ),
    )
    """
    project.compile(model)
    assert all(r.send_event for r in project.resources.values())


def test_batch_packages_handler(
    project: Project,
    remote_ssh_container: ssh_container.SshContainer,
) -> None:
    test_batch_packages_model(project, remote_ssh_container, package_names=["vim"])

    assert project.dryrun_resource("yum::PackagesBatch")
    project.deploy_resource("yum::PackagesBatch", run_as_root=False)
    assert not project.dryrun_resource("yum::PackagesBatch")

    test_batch_packages_model(
        project, remote_ssh_container, package_names=["vim", "nano"]
    )

    assert project.dryrun_resource("yum::PackagesBatch")
    project.deploy_resource("yum::PackagesBatch", run_as_root=False)
    assert not project.dryrun_resource("yum::PackagesBatch")

    test_batch_packages_model(
        project, remote_ssh_container, package_names=["vim", "nano"], purged=True
    )

    assert project.dryrun_resource("yum::PackagesBatch")
    project.deploy_resource("yum::PackagesBatch", run_as_root=False)
    assert not project.dryrun_resource("yum::PackagesBatch")
