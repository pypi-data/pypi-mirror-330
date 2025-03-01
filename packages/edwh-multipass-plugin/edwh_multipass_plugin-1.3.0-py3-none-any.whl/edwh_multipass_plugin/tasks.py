import json
import os
import re
import sys
import typing
from pathlib import Path
from typing import Optional

import edwh
import tomlkit
import yaml
from edwh import AnyDict, confirm, fabric_read, fabric_write
from edwh.improved_invoke import improved_task as task
from fabric import Connection, Result
from invoke import UnexpectedExit
from termcolor import cprint

T = typing.TypeVar("T")

# abs path required for remote connections
MULTIPASS = "/snap/bin/multipass"

# DON'T resolve ~ yet, since it can be executed remotely!
EW_MP_CONFIG = "~/.config/edwh/multipass.toml"
DEFAULT_MACHINE_NAME = "dockers"


@task(name="getsnap")
def install_snap(c, quiet=False):
    if edwh.tasks.is_installed(c, "snap"):
        if not quiet:
            print("Snap already installed")
        return
    try:
        c.sudo("rm /etc/apt/preferences.d/nosnap.pref")
        if not quiet:
            print("Nosnap found and removed.")
    except UnexpectedExit:
        if not quiet:
            print("No nonsnap.pref found")
    c.sudo("apt update")
    if not quiet:
        print("Installing snap...")
    c.sudo("apt install -y snapd")


@task(name="install", pre=[edwh.tasks.require_sudo])
def install_multipass(c: Connection) -> None:
    """
    Install multipass on this host.
    """
    if not c.run(f"{MULTIPASS} --version", warn=True, hide=True).ok:
        print(" [ ] Multipass not found. installing...")
        install_snap(c, quiet=True)

        c.sudo("snap install multipass")
        print(" [x] Multipass installed")
    else:
        print(" [x] Multipass already installed")


def generate_key(c: Connection, comment: str, filename: str) -> None:
    """
    Create an SSH pub-priv keypair.
    """
    c.run(f'ssh-keygen -t ed25519 -C "{comment}" -f {filename} -N ""')


def uniq(lst: list[T]) -> list[T]:
    """
    Filter out duplicates from 'lst'.

    Does not preserve order!
    """
    return list(set(lst))


@task(name="fix-host", aliases=["fix-dns"], iterable=["hostname"], pre=[edwh.tasks.require_sudo])
def fix_hosts_for_multipass_machine(c: Connection, machine_name: str, hostname: Optional[list[str]] = None) -> None:
    """
    Update your hosts file to connect fake hostnames to your multipass IP.

    `edwh mp.fix-host -m dockers -h delen.dockers.local -h dockers.local`
    """
    # Collection is Sized + Iterable

    if not machine_name:
        print("Machine name required. Use -m or --machine-name", file=sys.stderr)
        exit(1)

    output = c.run(f"{MULTIPASS} list --format yaml", hide=True).stdout.strip()
    machines = yaml.load(output, yaml.SafeLoader)
    if machine_name not in machines:
        print(
            f"'{machine_name}' not found. Choose one of: {', '.join(machines.keys())}",
            file=sys.stderr,
        )
        exit(1)

    machine = machines[machine_name][0]
    if machine["state"] != "Running":
        print(
            f"'{machine_name}' is not running.",
            file=sys.stderr,
        )
        if confirm("Should i start the machine for you? [Yn]", default=True):
            c.run(f"multipass start {machine_name}")
        return fix_hosts_for_multipass_machine(c, machine_name)

    first_address = machine["ipv4"][0]
    # start with the given hostnames (it's iterable, so should be a list style or default empty tuple)
    hostnames = list(hostname or [])
    # register the hostname
    hostnames.append(machine_name)
    # only unique values
    hostnames = uniq(hostnames)

    with open("/etc/hosts", "r") as hosts_handle:
        host_lines = hosts_handle.read().split("\n")

    found = any(name for name in hostnames if name in " ".join([line.split("#")[0] for line in host_lines]))
    if found:
        print("Updating hosts file")
        if len(hostname) > 1:
            print("You have entered hostnames, that argument is incompatible with the upgrade. ")
            print("Edit /etc/hosts manually to register aliases manually")
        new_hosts = []
        for line in host_lines:
            if any(name in line for name in hostnames):
                # line found, replace ip adress: convert tabs to spaces
                line = line.replace("\t", "    ")
                # create a new line with the ipv, whitespace, and the remainder of the original
                # line (everything after the first space), replacing multiple spaces with one.
                new_hosts.append(re.sub(r"  +", " ", f"{first_address}      {line.split(' ', 1)[1]}"))
                print(new_hosts[-1])
            else:
                new_hosts.append(line)
        overwrite_hosts_command = """python3 -c "import sys \nwith open('/etc/hosts','w') as h: h.write(sys.stdin.read().strip())" <<EOFEOFEOF\n"""
        overwrite_hosts_command += "\n".join(new_hosts)
        overwrite_hosts_command += "\nEOFEOFEOF"
        c.sudo(overwrite_hosts_command)
    else:
        print("Appending to hosts file")
        line_to_append = re.sub(r"  +", " ", f"{first_address}  {' '.join(hostnames)}")
        print(line_to_append)
        # simpelweg overschrijven via een echo of cat >> /etc/hosts mag niet. dus dan maar via een python script.
        c.sudo(f'''python3 -c "with open('/etc/hosts','a') as f: f.write('{line_to_append}')"''')


@task(name="list")
def list_machines(c: Connection, quiet: bool = False) -> list[AnyDict]:
    """
    List multipass machines.
    """

    output = c.run(f"{MULTIPASS} list --format json", hide=True).stdout
    if quiet:
        return typing.cast(list[AnyDict], json.loads(output)["list"])
    else:
        print(output)
        return []


@task(pre=[install_multipass], name="prepare")
def prepare_multipass(c: Connection, machine_name: str) -> None:
    """
    Setup ssh access to a multipass machine.
    """
    print(" ... Searching for vms")
    # convert to lookup by name
    machines = {m["name"]: m for m in list_machines(c, quiet=True)}
    if machine_name not in machines:
        raise KeyError(
            f'Machine name "{machine_name}" not found in multipass. Available names: {", ".join(list(machines.keys()))}'
        )
    machine = machines[machine_name]
    ip = machine["ipv4"][0]
    print(f" [x] {machine_name} found @ {ip} ")
    multipass_keyfile = Path("~/.ssh/multipass.key").expanduser()
    if not multipass_keyfile.exists():
        # create keyfile
        generate_key(c, "pyinvoke access to multipass machines", str(multipass_keyfile))
        print(" [x] created missing key file")
    else:
        print(" [x] key file exists")
    pub_file = Path(f"{multipass_keyfile}.pub")
    pub_key = pub_file.read_text().strip()
    installed_keys = c.run(
        f'echo "cat .ssh/authorized_keys ; exit " | multipass shell {machine_name}',
        warn=False,
        hide=True,
    ).stdout

    if pub_key in installed_keys:
        print(" [x] public key is installed to connect")
    else:
        print(" [ ] installing public key to access machine")
        c.run(
            f'echo "echo {pub_key} >> .ssh/authorized_keys; exit" | multipass shell {machine_name}',
            hide=True,
        )
        print(f" [x] installed multipass keyfile on {machine_name}")

    edwh_cmd = Path(sys.argv[0]).name
    print(f"Execute {edwh_cmd} with for example:")
    # fab_commands = "|".join(c.run(f"{edwh_cmd} --complete", hide=True).stdout.strip().split("\n"))
    # print(f"  {edwh_cmd} -eH ubuntu@{ip} [{fab_commands}]")
    print(f"  {edwh_cmd} -eH ubuntu@{ip} remote.prepare-generic-server")
    print(f'  {edwh_cmd} -eH ubuntu@{ip} -- echo "or some other arbitrary bash command"')


# todo: mp.mount which stores mounts in a file
#    so mp.remount knows which folders to remount


def _resolve_multipass_paths(folder: str, target: str) -> tuple[str, str]:
    source_path = Path(folder) if folder.startswith("/") else Path.cwd() / folder
    source_name = str(source_path).rstrip("/")
    target_name = (target or folder).rstrip("/")

    return source_name, target_name


class MultipassMounts(typing.TypedDict, total=False):
    mounts: typing.MutableMapping[str, str]


MultipassConfig: typing.TypeAlias = dict[str, MultipassMounts]


def _load_mp_config(c: Connection) -> MultipassConfig:
    config_str = fabric_read(c, EW_MP_CONFIG, throw=False)
    config = tomlkit.loads(config_str) if config_str else {}
    return typing.cast(
        MultipassConfig,
        config,
    )


def get_mounts(config: MultipassConfig, machine: str) -> typing.MutableMapping[str, str]:
    """
    Extract mounts for a machine in config.
    """
    machine_config = config.setdefault(machine, {})
    return machine_config.setdefault("mounts", {})


def _store_mp_config(c: Connection, config: MultipassConfig) -> None:
    config_str = tomlkit.dumps(config)
    fabric_write(c, EW_MP_CONFIG, config_str, parents=True)


def mp_mount(
    c: Connection,
    folder: str,
    machine: str,
    target_name: str,
    map_uid: Optional[dict[int, int]] = None,
    map_gid: Optional[dict[int, int]] = None,
) -> Optional[Result]:
    # map current user on host to ubuntu in VM
    map_uid = {os.getuid(): 1000, 1050: 1050} if map_uid is None else map_uid
    map_gid = {os.getuid(): 1000, 1050: 1050} if map_gid is None else map_gid

    mapping_args = (
        ""
        + " ".join(f"--uid-map={k}:{v}" for k, v in map_uid.items())
        + " "
        + " ".join(f"--gid-map={k}:{v}" for k, v in map_gid.items())
    )

    return c.run(f"{MULTIPASS} mount {mapping_args} {folder} {machine}:{target_name}", warn=True)


@task(name="mount")
def do_mount(c: Connection, folder: str, machine: str = DEFAULT_MACHINE_NAME, target_name: str = "") -> None:
    """
    Configure a new mountpoint.
    """
    source_name, target_name = _resolve_multipass_paths(folder, target_name)

    mp_mount(
        c,
        folder,
        machine,
        target_name,
    )

    config = _load_mp_config(c)
    mounts = get_mounts(config, machine)
    mounts[source_name] = target_name

    _store_mp_config(c, config)


@task()
def remount(c: Connection, machine: str = DEFAULT_MACHINE_NAME) -> None:
    """
    Remount all edwh managed mounts.
    """
    config = _load_mp_config(c)
    mounts = get_mounts(config, machine)

    for source, target in mounts.items():
        mp_mount(
            c,
            source,
            machine,
            target,
        )


@task()
def unmount(c: Connection, folder: str, machine: str = DEFAULT_MACHINE_NAME, permanently: bool = True) -> None:
    """
    Remove an edwh managed mountpoint.

    Saves to config by default!
    """
    source_name, _ = _resolve_multipass_paths(folder, "")

    config = _load_mp_config(c)
    mounts = get_mounts(config, machine)
    if not (mount := mounts.get(source_name)):
        cprint(f"Could not find mount point for {source_name}", color="yellow")
        return

    c.run(f"{MULTIPASS} unmount {machine}:{mount}", warn=True)

    if permanently:
        del mounts[source_name]
        _store_mp_config(c, config)


@task()
def unmount_all(c: Connection, machine: str = DEFAULT_MACHINE_NAME, permanently: bool = False) -> None:
    """
    Unmount all mounted volumes.

    Don't save to config by default!
    """
    config = _load_mp_config(c)
    mounts = get_mounts(config, machine)

    for mount in mounts:
        unmount(
            c,
            folder=mount,
            machine=machine,
            permanently=permanently,
        )


@task(name="mounts")
def list_mounts(c: Connection, machine: str = DEFAULT_MACHINE_NAME) -> None:
    """
    List edwh managed mounts.
    """
    config = _load_mp_config(c)
    mounts = get_mounts(config, machine)

    home = str(Path.home())
    cprint(f"Mounts for '{machine}':")
    for source, target in mounts.items():
        if source.startswith(home):
            source = source.replace(home, "~", 1)

        print(f"  {source}: {target}")
