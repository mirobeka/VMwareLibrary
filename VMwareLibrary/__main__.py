#!D:/Python2.7/python.exe

from __future__ import print_function
from robotremoteserver import RobotRemoteServer
from ConfigParser import ConfigParser as cp
from argparse import ArgumentParser
import logging
import vmlib
import sys
import os

def configure_logging():
    logging.basicConfig(
            format="%(asctime)s::[%(name)s.%(levelname)s] %(message)s",
            datefmt="%I:%M:%S %p",
            level='DEBUG')
    logging.StreamHandler(sys.__stdout__)

def parse_conf_to_dict(conf_path):
    parser = cp()
    try:
        parser.read(conf_path)
    except ConfigParser.Error, e:
        log("EXCEPTION: Parsing of {} failed.\n{}".format(conf_path, e.message))
        sys.exit(1)

    d = dict(parser._sections)
    for k in d:
        d[k] = dict(**d[k])
        d[k].pop('__name__', None)
    return d

def main():
    """ Main entry point for vmconnector"""

    # get configured logger
    logger = logging.getLogger("MAIN")

    # define arguments
    parser = ArgumentParser(prog="vmconnector", description="Robot Remote Server implementing VMware commands")
    # server configuration
    parser.add_argument("-i","--ip", required=False, dest="ip", default="0.0.0.0")
    parser.add_argument("-p", "--port", required=False, type=int, dest="port", default=8000)
  
    # password for VMware server
    os.environ["vmpass"] = "" if "vmpass" not in os.environ else os.environ["vmpass"]
    parser.add_argument("--vmpass", required=False, dest="vmpass", default=os.environ["vmpass"])
  
    # vmware config file
    parser.add_argument("-c", "--config", required=True, dest="conf_path")
  
    # parse arguments
    args = parser.parse_args()
  
    if args.vmpass == "" :
        logger.error("VMware password not in environment variables")
        logger.error("Use vmconnector --vmpass PASSWORD")
        sys.exit(1)

    # save password into config dictionary!
    conf = parse_conf_to_dict(args.conf_path)
    conf["vm_server"]["vmpass"] = args.vmpass
  
    # run server
    try:
        server = RobotRemoteServer(vmlib.Library(conf), args.ip, args.port)
    except KeyboardInterrupt, e:
        log("INFO: Keyboard Iterrupt: stopping server")
        server.stop_remote_server()

if __name__ == "__main__":
    configure_logging()
    main()
