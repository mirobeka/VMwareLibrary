from __future__ import print_function
from subprocess import Popen
from subprocess import PIPE
from time import time
from time import sleep
from telnetlib import Telnet
from socket import error as SocketError
import ConfigParser
import inspect
import sys

def log(msg):
    stdout = sys.stdout
    sys.stdout = sys.__stdout__
    print(msg)
    sys.stdout = stdout

class Library(object):
    """Factory creates vm commands from classes"""

    def __init__(self, conf):
        self.conf = conf

    def _vm_execute(self, cmd):
        sub = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = sub.communicate()
        returncode = sub.returncode
        return returncode, out, err

    def _get_authentication_flags(self, cfg):
        exe = self.conf["vmrun"]["command"]
        ip = self.conf["vm_server"]["ip"]
        guest_user = cfg["guest_user"]
        guest_passwd = cfg["guest_passwd"]
        vmuser = self.conf["vm_server"]["vmuser"]
        vmpass = self.conf["vm_server"]["vmpass"]
        vmx = cfg["vmx"]
        return exe, ip, vmuser, vmpass, guest_user, guest_passwd, vmx

    def _build_vm_command(self, command, cfg, *args):
        exe, ip, user, passwd, guest_user, guest_password, vmx = self._get_authentication_flags(cfg)
        additional_args = " ".join(map(str, args))
        cmd = "{} -h {} -u {} -p {} -gu {} -gp {} {} {} {}"
        cmd = cmd.format(
                exe, ip, user, passwd, guest_user, guest_password,
                command, vmx, additional_args)
        return cmd

    def _run(self, cmd_name, cfg, *args):
        cmd = self._build_vm_command(cmd_name, cfg, *args)
        log(cmd)
        returncode, out, err = self._vm_execute(cmd)

        if returncode != 0:
            msg = out+ " " +err
            raise AssertionError("VMware returned error code: {code} with message {msg}".format(code=returncode, msg=msg))
        return out

    def run_program_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        runProgramInGuest        vmx      Run a program in Guest OS
                                 [-noWait]
                                 [-activeWindow]
                                 [-interactive]
                                 Complete-Path-To-Program
                                 [Program arguments]
        """
        return self._run("runProgramInGuest", cfg, *args)

    def file_exists_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        fileExistsInGuest        Name of cfg      Check if a file exists in Guest OS
                                 Path to file in guest
        """
        return self._run("fileExistsInGuest", cfg, args)

    def directory_exists_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        directoryExistsInGuest   Path to vmx file     Check if a directory exists in Guest OS
                                 Path to directory in guest
        """
        return self._run("directoryExistsInGuest", cfg, args)

    def set_shared_folder_state(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        setSharedFolderState     Path to vmx file     Modify a Host-Guest shared folder
                                 Share name
                                 Host path
                                 writable | readonly
        """
        return self._run("setSharedFolderState", cfg, args)

    def add_shared_folder(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        addSharedFolder          Path to vmx file     Add a Host-Guest shared folder
                                 Share name
                                 New host path
        """
        return self._run("addSharedFolder", cfg, args)

    def remove_shared_folder(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        removeSharedFolder       Path to vmx file     Remove a Host-Guest shared folder
                                 Share name
        """
        return self._run("removeSharedFolder", cfg, args)

    def enable_shared_folders(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        enableSharedFolders      Path to vmx file     Enable shared folders in Guest
                                 [runtime]
        """
        return self._run("enableSharedFolders", cfg, *args)

    def disable_shared_folders(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        disableSharedFolders     Path to vmx file     Disable shared folders in Guest
                                 [runtime]
        """
        return self._run("disableSharedFolders", cfg, *args)

    def list_processes_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        listProcessesInGuest     Path to vmx file     List running processes in Guest OS
        """
        return self._run("listProcessesInGuest", cfg, *args)

    def kill_process_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        killProcessInGuest       Path to vmx file     Kill a process in Guest OS
                                 process id
        """
        return self._run("killProcessInGuest", cfg, *args)

    def run_script_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        runScriptInGuest         Path to vmx file     Run a script in Guest OS
                                 [-noWait]
                                 [-activeWindow]
                                 [-interactive]
                                 Interpreter path
                                 Script text
        """
        return self._run("runScriptInGuest", cfg, *args)

    def delete_file_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        deleteFileInGuest        Path to vmx file     Delete a file in Guest OS
        Path in guest
        """
        return self._run("deleteFileInGuest", cfg, *args)

    def create_directory_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        createDirectoryInGuest   Path to vmx file     Create a directory in Guest OS
        Directory path in guest
        """
        return self._run("createDirectoryInGuest", cfg, *args)

    def delete_directory_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        deleteDirectoryInGuest   Path to vmx file     Delete a directory in Guest OS
        Directory path in guest
        """
        return self._run("deleteDirectoryInGuest", cfg, *args)

    def create_temp_file_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        CreateTempfileInGuest    Path to vmx file     Create a temporary file in Guest OS
        """
        return self._run("CreateTempfileInGuest", cfg, *args)

    def list_directory_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        listDirectoryInGuest     Path to vmx file     List a directory in Guest OS
                                 Directory path in guest
        """
        return self._run("listDirectoryInGuest", cfg, *args)

    def copy_file_from_host_to_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        CopyFileFromHostToGuest  Path to vmx file     Copy a file from host OS to guest OS
        Path on host             Path in guest
        """
        return self._run("CopyFileFromHostToGuest", cfg, *args)

    def copy_file_from_guest_to_host(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        CopyFileFromGuestToHost  Path to vmx file     Copy a file from guest OS to host OS
        Path in guest            Path on host
        """
        return self._run("CopyFileFromGuestToHost", cfg, *args)


    def rename_file_in_guest(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        renameFileInGuest        Path to vmx file     Rename a file in Guest OS
                                 Original name
                                 New name
        """
        return self._run("renameFileInGuest", cfg, *args)

    def capture_screen(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        captureScreen            Path to vmx file     Capture the screen of the VM to a local file
        Path on host
        """
        return self._run("captureScreen", cfg, *args)

    def write_variable(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        writeVariable            Path to vmx file     Write a variable in the VM state
                                 [runtimeConfig|guestEnv|guestVar]
                                 variable name
                                 variable value
        """
        return self._run("writeVariable", cfg, *args)

    def read_variable(self, cfg, *args):
        """
        GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
        -----------------        ----------           -----------
        readVariable             Path to vmx file     Read a variable in the VM state
                                 [runtimeConfig|guestEnv|guestVar]
                                 variable namen response.get_value()
        """
        return self._run("readVariable", cfg, *args)

    def reset(self, cfg, *args):
        """VMware api command implementation

        POWER COMMANDS        PARAMETERS      DESCRIPTION
        --------------        ----------      -----------
        reset                 path to vmx     Reset a VM or Team
        """
        return self._run("reset", cfg, *args)

    def stop(self, cfg, *args):
        """VMware api command implementation

        POWER COMMANDS        PARAMETERS      DESCRIPTION
        --------------        ----------      -----------
        stop                  path to vmx     Stop a VM or Team
        """
        return self._run("stop", cfg, *args)

    def start(self, cfg, *args):
        """VMware api command implementation

        POWER COMMANDS        PARAMETERS      DESCRIPTION
        --------------        ----------      -----------
        start                 path to vmx     Start a VM or Team
        """
        return self._run("start", cfg, *args)

    def list_snapshots(self, cfg, *args):
        """VMware api command implementation

        SNAPSHOT COMMANDS        PARAMETERS      DESCRIPTION
        -----------------        ----------      -----------
        listSnapshots            path to vmx     List all snapshots in a VM
        """
        return self._run("listSnapshots", cfg, *args)

    def snapshot(self, cfg, *args):
        """VMware api command implementation

        SNAPSHOT COMMANDS        PARAMETERS      DESCRIPTION
        -----------------        ----------      -----------
        snapshot                 path to vmx,    Create a snapshot of a VM
                                 snapshot name
        """
        return self._run("snapshot", cfg, *args)

    def delete_snapshot(self, cfg, *args):
        """VMware api command implementation

        SNAPSHOT COMMANDS        PARAMETERS      DESCRIPTION
        -----------------        ----------      -----------
        deleteSnapshot           path to vmx,    Remove a snapshot from a VM
                                 snapshot name
        """
        return self._run("deleteSnapshot", cfg, *args)

    def revert_to_snapshot(self, cfg, *args):
        """VMware api command implementation

        SNAPSHOT COMMANDS        PARAMETERS      DESCRIPTION
        -----------------        ----------      -----------
        revertToSnapshot         path to vmx,    Set VM state to a snapshot
                                 snapshot name
        """

        self._run("revertToSnapshot", cfg, *args) 
        return self._run("start", cfg)

    def install_tools(self, cfg):
        """VMware api command implementation

        GENERAL COMMANDS         PARAMETERS      DESCRIPTION
        ----------------         ----------      -----------
        installTools             path to vmx     Mount vmtools disc
        """
        return self._run("installTools", cfg)
