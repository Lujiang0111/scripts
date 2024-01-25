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
    __release = False
    __dst_path = None
    __lib_base_path = None

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
        if param_cnt < 4:
            raise SystemExit("param cnt={} too less".format(param_cnt))

        self.__release = args[1] == "release"
        self.__dst_path = args[2]
        self.__lib_base_path = args[3]

        libs = args[4].split(" ")
        for i in range(1, len(libs), 2):
            lib_name = libs[i - 1]
            lib_version = libs[i]
            self.__CopyLib(lib_name, lib_version)

    def __CopyLib(self, lib_name, lib_version) -> None:
        lib_path = os.path.join(self.__lib_base_path, lib_name)
        if not os.path.isdir(lib_path):
            raise SystemExit("{} not found!".format(lib_path))

        sub_paths = [
            d for d in os.listdir(lib_path) if os.path.isdir(os.path.join(lib_path, d))
        ]
        if not sub_paths:
            raise SystemExit("{} versions not found!".format(lib_name))

        choose_version_path = max(sub_paths)
        choose_version = re.sub(r"^[^0-9]+", "", choose_version_path)

        if choose_version < lib_version:
            raise SystemExit(
                "{} max version={} < {}!".format(lib_name, choose_version, lib_version)
            )

        lib_os_version_choose_path = None
        if True:
            lib_os_version_path = os.path.join(
                lib_path, choose_version_path, self.__os_version
            )
            lib_os_version_default_path = os.path.join(
                lib_path, choose_version_path, self.__os_version_default
            )

            if os.path.isdir(lib_os_version_path):
                lib_os_version_choose_path = lib_os_version_path
                print(
                    "{} {} => choose {}".format(lib_name, lib_version, choose_version)
                )
            else:
                lib_os_version_choose_path = lib_os_version_default_path
                print(
                    "{} {} => choose {} {}".format(
                        lib_name, lib_version, choose_version, self.__os_version_default
                    )
                )

        lib_debug_path = os.path.join(lib_os_version_choose_path, self.__os_arch)
        lib_debug_path_exist = os.path.isdir(lib_debug_path)
        lib_release_path = os.path.join(
            lib_os_version_choose_path, "{}_release".format(self.__os_arch)
        )
        lib_release_path_exist = os.path.isdir(lib_release_path)

        if (not lib_debug_path_exist) and (not lib_release_path_exist):
            raise SystemExit(
                "{} arch {} not found!".format(
                    lib_os_version_choose_path, self.__os_arch
                )
            )

        lib_os_arch_path = None
        if self.__release:
            if lib_release_path_exist:
                lib_os_arch_path = lib_release_path
            else:
                lib_os_arch_path = lib_debug_path
        else:
            if lib_debug_path_exist:
                lib_os_arch_path = lib_debug_path
            else:
                lib_os_arch_path = lib_release_path

        CopyDir(os.path.join(lib_os_arch_path, "lib"), self.__dst_path)

        # for plugin
        CopyDir(os.path.join(lib_os_arch_path, "bin"), self.__dst_path)


if __name__ == "__main__":
    postbuild = Postbuild()
    postbuild.Do(sys.argv)
