#!D:/Python2.7/python.exe

from __future__ import print_function
from robotremoteserver import RobotRemoteServer
from ConfigParser import ConfigParser as cp
from argparse import ArgumentParser
import vmlib
import logging
import os

def log(msg):
    stdout = sys.stdout
    sys.stdout = sys.__stdout__
    print(msg)
    sys.stdout = stdout

def parse_conf_to_dict(conf_path):
    parser = cp()
    try:
        parser.read(conf_path)
    except ConfigParser.Error, e:
        log("EXCEPTION: Parsing of {} failed.\n{}".format(conf_path, e.message))
        exit(1)

    d = dict(parser._sections)
    for k in d:
        d[k] = dict(**d[k])
        d[k].pop('__name__', None)
    return d
  

def main():
    """ Main entry point for vmconnector"""
    # define arguments
    parser = ArgumentParser(prog="vmconnector", description="Robot Remote Server implementing VMware commands")
    # server configuration
    parser.add_argument("-i","--ip", required=False, dest="ip", default="localhost")
    parser.add_argument("-p", "--port", required=False, type=int, dest="port", default=8000)
  
    # password for VMware server
    os.environ["vmpass"] = "" if "vmpass" not in os.environ else os.environ["vmpass"]
    parser.add_argument("--vmpass", required=False, dest="vmpass", default=os.environ["vmpass"])
  
    # vmware config file
    parser.add_argument("-c", "--config", required=True, dest="conf_path")
  
    # parse arguments
    args = parser.parse_args()
  
    if args.vmpass == "" :
        print("VMware password / username not in environment variables")
        print("Use vmconnector --vmpass PASSWORD --vmuser USERNAME")
        exit(1)

    conf = parse_conf_to_dict(args.conf_path)
    conf["vm_server"]["vmpass"] = args.vmpass
  
    # run server
    try:
        server = RobotRemoteServer(vmlib.Library(conf), args.ip, args.port)
    except KeyboardInterrupt, e:
        log("INFO: Keyboard Iterrupt: stopping server")
        server.stop_remote_server()

if __name__ == "__main__":
    main()
