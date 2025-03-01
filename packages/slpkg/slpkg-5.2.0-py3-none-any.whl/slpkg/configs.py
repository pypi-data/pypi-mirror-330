#!/usr/bin/python3
# -*- coding: utf-8 -*-


import platform
from pathlib import Path

import tomlkit
from tomlkit import exceptions

from slpkg.toml_errors import TomlErrors


class Configs:  # pylint: disable=[R0902, R0903]
    """Default configurations."""

    toml_errors = TomlErrors()

    prog_name: str = 'slpkg'
    tmp_path: Path = Path('/tmp')
    tmp_slpkg: Path = Path(tmp_path, prog_name)
    build_path: Path = Path(tmp_path, prog_name, 'build')
    etc_path: Path = Path('/etc', prog_name)
    lib_path: Path = Path('/var/lib', prog_name)
    log_path: Path = Path('/var/log/', prog_name)
    log_packages: Path = Path('/var', 'log', 'packages')

    deps_log_file: Path = Path(log_path, 'deps.log')
    slpkg_log_file: Path = Path(log_path, 'slpkg.log')
    upgrade_log_file: Path = Path(log_path, 'upgrade.log')
    error_log_file: Path = Path(log_path, 'error.log')

    os_arch: str = platform.machine()
    file_list_suffix: str = '.pkgs'
    package_type = [".tgz", ".txz"]
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'
    kernel_version: bool = True
    bootloader_command: str = ''
    colors: bool = True
    makeflags: str = '-j4'
    gpg_verification: bool = False
    checksum_md5: bool = True
    dialog: bool = True
    view_missing_deps: bool = True
    package_method: bool = False
    downgrade_packages: bool = False
    delete_sources: bool = False
    downloader: str = 'wget'
    wget_options: str = '--c -q --progress=bar:force:noscroll --show-progress'
    curl_options: str = ''
    lftp_get_options: str = '-c get -e'
    lftp_mirror_options: str = '-c mirror --parallel=100 --only-newer --delete'
    git_clone: str = 'git_clone'
    download_only_path: Path = Path(tmp_slpkg, '')
    ascii_characters: bool = True
    ask_question: bool = True
    parallel_downloads: bool = False
    maximum_parallel: int = 5
    progress_bar_conf: bool = False
    progress_spinner: str = 'spinner'
    spinner_color: str = 'green'
    border_color: str = 'bold_green'
    process_log: bool = True

    urllib_retries: bool = False
    urllib_redirect: bool = False
    urllib_timeout: float = 3.0

    proxy_address: str = ''
    proxy_username: str = ''
    proxy_password: str = ''

    try:
        # Load user configuration.
        config_path_file: Path = Path(etc_path, f'{prog_name}.toml')
        conf: dict[str, dict[str, str]] = {}
        if config_path_file.exists():
            with open(config_path_file, 'r', encoding='utf-8') as file:
                conf = dict(tomlkit.parse(file.read()))

        if conf:
            config = conf['CONFIGS']

            os_arch = config['OS_ARCH']
            file_list_suffix = config['FILE_LIST_SUFFIX']
            package_type = list(config['PACKAGE_TYPE'])
            installpkg = config['INSTALLPKG']
            reinstall = config['REINSTALL']
            removepkg = config['REMOVEPKG']
            kernel_version = bool(config['KERNEL_VERSION'])
            bootloader_command = config['BOOTLOADER_COMMAND']
            colors = bool(config['COLORS'])
            makeflags = config['MAKEFLAGS']
            gpg_verification = bool(config['GPG_VERIFICATION'])
            checksum_md5 = bool(config['CHECKSUM_MD5'])
            dialog = bool(config['DIALOG'])
            view_missing_deps = bool(config['VIEW_MISSING_DEPS'])
            package_method = bool(config['PACKAGE_METHOD'])
            downgrade_packages = bool(config['DOWNGRADE_PACKAGES'])
            delete_sources = bool(config['DELETE_SOURCES'])
            downloader = config['DOWNLOADER']
            wget_options = config['WGET_OPTIONS']
            curl_options = config['CURL_OPTIONS']
            lftp_get_options = config['LFTP_GET_OPTIONS']
            lftp_mirror_options = config['LFTP_MIRROR_OPTIONS']
            git_clone = config['GIT_CLONE']
            download_only_path = Path(config['DOWNLOAD_ONLY_PATH'])
            ascii_characters = bool(config['ASCII_CHARACTERS'])
            ask_question = bool(config['ASK_QUESTION'])
            parallel_downloads = bool(config['PARALLEL_DOWNLOADS'])
            maximum_parallel = int(config['MAXIMUM_PARALLEL'])
            progress_bar_conf = bool(config['PROGRESS_BAR'])
            progress_spinner = config['PROGRESS_SPINNER']
            spinner_color = config['SPINNER_COLOR']
            border_color = config['BORDER_COLOR']
            process_log = bool(config['PROCESS_LOG'])

            urllib_retries = bool(config['URLLIB_RETRIES'])
            urllib_redirect = bool(config['URLLIB_REDIRECT'])
            urllib_timeout = float(config['URLLIB_TIMEOUT'])

            proxy_address = config['PROXY_ADDRESS']
            proxy_username = config['PROXY_USERNAME']
            proxy_password = config['PROXY_PASSWORD']

    except (KeyError, exceptions.TOMLKitError) as e:
        toml_errors.raise_toml_error_message(str(e), toml_file=Path('/etc/slpkg/slpkg.toml'))

    blink: str = ''
    bold: str = ''
    red: str = ''
    bred: str = ''
    green: str = ''
    bgreen: str = ''
    yellow: str = ''
    byellow: str = ''
    cyan: str = ''
    bcyan: str = ''
    blue: str = ''
    bblue: str = ''
    grey: str = ''
    violet: str = ''
    endc: str = ''

    if colors:
        blink = '\033[32;5m'
        bold = '\033[1m'
        red = '\x1b[91m'
        bred = f'{bold}{red}'
        green = '\x1b[32m'
        bgreen = f'{bold}{green}'
        yellow = '\x1b[93m'
        byellow = f'{bold}{yellow}'
        cyan = '\x1b[96m'
        bcyan = f'{bold}{cyan}'
        blue = '\x1b[94m'
        bblue = f'{bold}{blue}'
        grey = '\x1b[38;5;247m'
        violet = '\x1b[35m'
        endc = '\x1b[0m'

    # Creating the paths if not exists
    paths = [
        lib_path,
        etc_path,
        build_path,
        tmp_slpkg,
        log_path,
        download_only_path,
    ]

    for path in paths:
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
