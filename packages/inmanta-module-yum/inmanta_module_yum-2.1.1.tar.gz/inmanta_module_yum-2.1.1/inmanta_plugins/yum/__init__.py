"""
Copyright 2016 Inmanta

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

import inmanta_plugins.mitogen.abc

import inmanta.agent.handler
import inmanta.export
import inmanta.resources


@inmanta.resources.resource("yum::Package", agent="host.name", id_attribute="name")
class Package(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A software package installed on an operating system.
    """

    fields = ("name",)  # type: ignore

    name: str


@inmanta.resources.resource(
    "yum::PackagesBatch", agent="host.name", id_attribute="name"
)
class PackagesBatch(inmanta_plugins.mitogen.abc.ResourceABC):
    """
    A software package installed on an operating system.
    """

    fields = ("name", "packages")  # type: ignore

    name: str
    packages: list[str]


class YumHelper(inmanta_plugins.mitogen.abc.HandlerABC):
    """
    Helper class for yum operations
    """

    def _run_yum(self, args: list[str]) -> tuple[str, str, int]:
        """
        Execute dnf command with provided args if dnf installed otherwise it uses yum.

        :param args: The arguments of the command
        :return: A tuple with (stdout, stderr, returncode)
        """
        if self.proxy.file_exists("/usr/bin/dnf"):
            return self.proxy.run("/usr/bin/dnf", ["-d", "0", "-e", "1", "-y"] + args)
        else:
            return self.proxy.run("/usr/bin/yum", ["-d", "0", "-e", "1", "-y"] + args)

    def raise_for_errors(
        self,
        output: tuple[str, str, int],
        ignore_errors: list[str] = [],
    ):
        """
        Process the output of yum command and raises an error if the return code is not 0.
        """
        stdout = output[0].strip()
        error_msg = output[1].strip()
        if output[2] != 0:
            for error in ignore_errors:
                if error in error_msg:
                    return
            raise Exception("Yum failed: stdout:" + stdout + " errout: " + error_msg)

    def is_installed(self, package: str) -> bool:

        assert self.proxy.file_exists("/usr/bin/rpm"), "The OS doesn't have rpm binary"

        output = self.proxy.run("/usr/bin/rpm", ["-q", package])

        if output[2] == 1:
            # For some package `rpm -q PACKAGE` doesn't work (eg: vim)
            # So we can check executable
            which_output = self.proxy.run("command", ["-v", package])
            if which_output[2] == 0:
                output = self.proxy.run("/usr/bin/rpm", ["-qf", which_output[0]])

        if output[2] == 0:
            return True
        return False


@inmanta.agent.handler.provider("yum::Package", name="yum")
class YumPackage(YumHelper):
    """
    A Package handler that uses yum
    """

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        if not self.is_installed(resource.name):
            raise inmanta.agent.handler.ResourcePurged()

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        self.raise_for_errors(self._run_yum(["install", resource.name]))
        ctx.set_created()

    def update_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        changes: dict,
        resource: Package,
    ) -> None:
        raise NotImplementedError("PackageHandler doesn't support update_resource !")

    def delete_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: Package
    ) -> None:
        self.raise_for_errors(self._run_yum(["remove", resource.name]))
        ctx.set_purged()


@inmanta.agent.handler.provider("yum::PackagesBatch", name="yum")
class YumPackagesBatch(YumHelper):
    """
    A Package handler that uses yum in batch
    """

    def read_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: PackagesBatch
    ) -> None:
        installed = [name for name in resource.packages if self.is_installed(name)]
        if len(installed) == 0:
            raise inmanta.agent.handler.ResourcePurged()
        resource.packages = installed

    def create_resource(
        self, ctx: inmanta.agent.handler.HandlerContext, resource: PackagesBatch
    ) -> None:
        yum_output = self._run_yum(["install"] + resource.packages)
        self.raise_for_errors(yum_output)

        ctx.set_created()

    def update_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        changes: dict,
        resource: PackagesBatch,
    ) -> None:
        to_add = [
            pkg
            for pkg in changes["packages"]["desired"]
            if pkg not in changes["packages"]["current"]
        ]
        yum_output = self._run_yum(["install"] + to_add)
        self.raise_for_errors(yum_output)

        ctx.set_updated()

    def delete_resource(
        self,
        ctx: inmanta.agent.handler.HandlerContext,
        resource: PackagesBatch,
    ) -> None:
        yum_output = self._run_yum(["remove"] + resource.packages)
        self.raise_for_errors(yum_output)

        ctx.set_purged()
