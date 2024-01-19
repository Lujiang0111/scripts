import enum
import os
import platform
import shutil
import subprocess
import sys


def RmDir(dir) -> None:
    if not os.path.exists(dir):
        return

    if os.path.isdir(dir):
        shutil.rmtree(dir)
    else:
        os.remove(dir)


class Categorys(enum.Enum):
    kNone = 0
    kProject = 1
    kBaselib = 2
    kEngine = 3
    kFabrics = 4
    kPlugins = 5
    kExtra = 6


class RebuildAll:
    __os_version_default = None
    __os_version = None
    __os_arch = None
    __svn_root = "svn://192.165.152.13/sumard5/Project/Venus/Ability"
    __svn_username = "zhangwenjun"
    __svn_password = "qazse4321"
    __project_compile_root = None
    __project_path = None
    __release = False
    __make_parallel = 1
    __build_list = []

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

    def __SvnExport(self, svn_path, local_path):
        os.makedirs(local_path)
        RmDir(local_path)
        print("svn export {}".format(svn_path))
        subprocess.run(
            [
                "svn",
                "export",
                svn_path,
                local_path,
                "-q",
                "--non-interactive",
                "--trust-server-cert",
                "--username",
                self.__svn_username,
                "--password",
                self.__svn_password,
            ],
            check=True,
        )

    def ReadFormConfig(self, conf_file) -> None:
        try:
            with open(conf_file, "r", errors="ignore") as file:
                category = Categorys.kNone
                category_path = None
                for line in file:
                    line = line.strip()

                    if (not line) or (line.startswith("#")):
                        continue

                    if line == "[Project]":
                        category = Categorys.kProject
                    elif line == "[Baselib]":
                        category = Categorys.kBaselib
                        category_path = "Baselib"
                    elif line == "[Engine]":
                        category = Categorys.kEngine
                        category_path = "Engine"
                    elif line == "[Fabrics]":
                        category = Categorys.kFabrics
                        category_path = "Fabrics"
                    elif line == "[Plugins]":
                        category = Categorys.kPlugins
                        category_path = "Plugins/Antares"
                    elif line == "[Extra]":
                        category = Categorys.kExtra
                    else:
                        if category == Categorys.kProject:
                            key_value_pair = line.split("=")
                            if len(key_value_pair) == 2:
                                key = key_value_pair[0].strip()
                                value = key_value_pair[1].strip()
                                if key == "project":
                                    project = value
                                    self.__project_compile_root = "compile_{}".format(
                                        project
                                    )
                                    RmDir(self.__project_compile_root)
                                elif key == "project_path":
                                    self.__project_path = value
                                elif key == "release":
                                    self.__release = value.lower() == "true"
                                elif key == "make_parallel":
                                    if value.lower() == "auto":
                                        process_result = subprocess.run(
                                            ["echo -e $(nproc)"],
                                            shell=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True,
                                        ).stdout
                                        self.__make_parallel = int(process_result)
                                    else:
                                        self.__make_parallel = int(value)

                                    if self.__make_parallel <= 0:
                                        self.__make_parallel = 1

                        elif (
                            category == Categorys.kBaselib
                            or category == Categorys.kEngine
                            or category == Categorys.kFabrics
                            or category == Categorys.kPlugins
                        ):
                            items = line.split()
                            if len(items) >= 3:
                                lib_name = items[0].strip()
                                lib_repo = items[1].strip()
                                lib_version = items[2].strip()

                                if lib_repo == "Versions":
                                    svn_path = "{}/{}/{}/{}/{}".format(
                                        self.__svn_root,
                                        lib_repo,
                                        category_path,
                                        lib_name,
                                        lib_version,
                                    )
                                    lib_path = os.path.join(
                                        self.__project_compile_root,
                                        lib_repo,
                                        category_path,
                                        lib_name,
                                        lib_version,
                                    )
                                    self.__SvnExport(svn_path, lib_path)
                                else:
                                    svn_path = "{}/{}/{}/{}/{}".format(
                                        self.__svn_root,
                                        category_path,
                                        lib_name,
                                        lib_repo,
                                        lib_version,
                                    )
                                    lib_path = os.path.join(
                                        self.__project_compile_root,
                                        category_path,
                                        lib_name,
                                        lib_repo,
                                        lib_version,
                                    )
                                    self.__SvnExport(svn_path, lib_path)
                                    self.__build_list.append(lib_path)
                        elif category == Categorys.kExtra:
                            svn_path = "{}/{}".format(self.__svn_root, line)
                            local_path = os.path.join(self.__project_compile_root, line)
                            self.__SvnExport(svn_path, local_path)

        except FileNotFoundError:
            raise SystemExit("conf file not found: {}".format(conf_file))
        except Exception as e:
            raise SystemExit("An error occurred: {}".format(e))

    def StartBuild(self) -> None:
        self.__build_list.append(
            os.path.join(self.__project_compile_root, self.__project_path)
        )
        for build_item in self.__build_list:
            item_os_version_path = os.path.join(build_item, "build", self.__os_version)
            item_os_version_default_path = os.path.join(
                build_item, "build", self.__os_version_default
            )

            if os.path.isdir(item_os_version_path):
                item_os_version_choose_path = item_os_version_path
            else:
                item_os_version_choose_path = item_os_version_default_path

            item_debug_path = os.path.join(item_os_version_choose_path, self.__os_arch)
            item_debug_path_exist = os.path.isdir(item_debug_path)
            item_release_path = os.path.join(
                item_os_version_choose_path, "{}_release".format(self.__os_arch)
            )
            item_release_path_exist = os.path.isdir(item_release_path)

            if (not item_debug_path_exist) and (not item_release_path_exist):
                print(
                    "{} arch {} not found!".format(
                        item_os_version_choose_path, self.__os_arch
                    )
                )
                continue

            item_os_arch_path = None
            if self.__release:
                if item_release_path_exist:
                    item_os_arch_path = item_release_path
                else:
                    item_os_arch_path = item_debug_path
            else:
                if item_debug_path_exist:
                    item_os_arch_path = item_debug_path
                else:
                    item_os_arch_path = item_release_path

            try:
                print(
                    "{}make {} -j{} {}".format(
                        "\033[33m", item_os_arch_path, self.__make_parallel, "\033[0m"
                    )
                )
                if self.__release:
                    subprocess.run(
                        "cd {} && make clean && make release -j{} >> /dev/null".format(
                            item_os_arch_path, self.__make_parallel
                        ),
                        check=True,
                        shell=True,
                    )
                else:
                    subprocess.run(
                        "cd {} && make clean >> /dev/null && make -j{} >> /dev/null".format(
                            item_os_arch_path, self.__make_parallel
                        ),
                        check=True,
                        shell=True,
                    )
            except Exception as e:
                pass


if __name__ == "__main__":
    param_cnt = len(sys.argv) - 1
    if param_cnt < 1:
        raise SystemExit("param cnt={} to less".format(param_cnt))

    rebuild_all = RebuildAll()

    conf_file = sys.argv[1]
    rebuild_all.ReadFormConfig(conf_file)
    rebuild_all.StartBuild()
