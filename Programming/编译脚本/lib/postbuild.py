import os
import platform
import re
import shutil
import subprocess
import sys


def CopyDir(src_dir, dst_dir) -> None:
    if not os.path.isdir(src_dir):
        return

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)
        if os.path.isdir(src_item):
            CopyDir(src_item, dst_item)
        else:
            shutil.copy2(src_item, dst_item, follow_symlinks=False)


def RmDir(dir) -> None:
    if not os.path.exists(dir):
        return

    if os.path.isdir(dir):
        shutil.rmtree(dir)
    else:
        os.remove(dir)


class Postbuild:
    __os_version_default = None
    __os_version = None
    __os_arch = None

    def __init__(self) -> None:
        self.__GetOsVersion()
        self.__GetOsArch()

    def __GetOsVersion(self) -> None:
        system_platform = platform.system()
        if system_platform == "Windows":
            self.__os_version_default = "windows/vs2017/"
            self.__os_version = self.__os_version_default
            return
        else:
            self.__os_version_default = "linux/centos7.1/"
            with open("/etc/os-release", "r") as file:
                for line in file:
                    if "Ubuntu" in line:
                        self.__os_version = "linux/ubuntu22.04/"
                        return
                    elif "Kylin" in line:
                        self.__os_version = "linux/KylinV10/"
                        return
            self.__os_version = self.__os_version_default

    def __GetOsArch(self) -> None:
        system_platform = platform.system()
        if system_platform == "Windows":
            self.__os_arch = "x64"
            return
        else:
            process_result = subprocess.run(
                ["uname", "-a"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            ).stdout
            if "aarch64" in process_result:
                self.__os_arch = "aarch64"
                return
            else:
                self.__os_arch = "x64"
                return

    def Do(self, args) -> None:
        param_cnt = len(args) - 1
        if param_cnt < 6:
            raise SystemExit("param cnt={} too less".format(param_cnt))

        release = args[1] == "release"
        target_path = args[2]
        include_path = args[3]
        dst_base_path = args[4]
        project = args[5]
        version = re.sub(r"^[^0-9]+", "", args[6])

        if release:
            self.__os_arch = "{}_release".format(self.__os_arch)

        dst_version_path = os.path.join(dst_base_path, project, "v{}".format(version))
        dst_arch_path = os.path.join(
            dst_version_path, self.__os_version, self.__os_arch
        )

        RmDir(dst_arch_path)
        CopyDir(include_path, os.path.join(dst_arch_path, "include"))
        CopyDir(target_path, os.path.join(dst_arch_path, "lib"))

        if self.__os_version != self.__os_version_default:
            dst_default_arch_path = os.path.join(
                dst_version_path, self.__os_version_default, self.__os_arch
            )
            RmDir(dst_default_arch_path)
            CopyDir(dst_arch_path, dst_default_arch_path)
            print("copy {} to {}".format(dst_arch_path, dst_default_arch_path))


if __name__ == "__main__":
    postbuild = Postbuild()
    postbuild.Do(sys.argv)
