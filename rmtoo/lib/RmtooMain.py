#
# Requirement Management Toolset
#
#  This is the main function - it is called from the 'rmtoo'
#  executable directly. 
#  It is stored here (in a seperate file) for (blackbox) testing
#  proposes. 
#
# (c) 2010 by flonatel
#
# For licencing details see COPYING
#

import os
import sys

from optparse import OptionParser
from rmtoo.lib.RequirementSet import RequirementSet
from rmtoo.lib.ReqsContinuum import ReqsContinuum
from rmtoo.lib.Modules import Modules
from rmtoo.lib.RMTException import RMTException
from rmtoo.lib.TopicHandler import TopicHandler
from rmtoo.lib.OutputHandler import OutputHandler
from rmtoo.lib.Analytics import Analytics

def parse_cmd_line_opts(args):
    parser = OptionParser()
    parser.add_option("-f", "--file-config", dest="config_file",
                  help="Config file")
    parser.add_option("-m", "--modules-directory", dest="modules_directory",
                  help="Directory with modules")
    parser.add_option("-c", "--create-makefile-dependencies",
                      dest="create_makefile_dependencies",
                      help="Create makefile dependencies")

    (options, args) = parser.parse_args(args=args)

    if options.modules_directory==None:
        # If there is no modules directory given, use the pycentral one.
        options.modules_directory = "/usr/share/pyshared"

    if options.config_file==None:
        raise RMTException(60, "no config_file option is specified")

    if len(args)>0:
        raise RMTException(61, "too many args")

    return options

def execute_cmds(opts, config, mods, mstdout, mstderr):
    # Checks are allways done - to be sure that e.g. the dependencies
    # are correct.
    try:
        rc = ReqsContinuum(mods, opts, config)
        reqs = rc.continnum_latest()
    except RMTException, rmte:
        mstderr.write("+++ ERROR: Problem reading in the continuum: '%s'"
                      % rmte)
        return False

    # Setup the OutputHandler
    # Note: this can be more than one!
    # For the topic based output also all the Topics are needed -
    # before the OutputHandler itself - because different output
    # handler may reference the same Topic.
    topics = TopicHandler(config, reqs)
    ohandler = OutputHandler(config, topics)

    # When only the dependencies are needed, output them to the given
    # file. 
    if opts.create_makefile_dependencies!=None:
        ofile = file(opts.create_makefile_dependencies, "w")
        # Write out the REQS=
        rc.cmad_write_reqs_list(ofile)
        # Write out the rest
        ohandler.create_makefile_dependencies(ofile, rc)
        ofile.close()
        return True

    # If there is a problem with the last requirement set included in
    # the requirements continuum, print out the errors here and stop
    # processing.
    if not reqs.is_usable():
        reqs.write_log(mstderr)
        return False

    # The requirments are syntatically correct now: therefore it is
    # possible to do some analytics on them
    if not Analytics.run(config, reqs, topics):
        reqs.write_log(mstderr)
        reqs.write_analytics_result(mstderr)

        if hasattr(config, 'analytics_specs') \
                and 'stop_on_errors' in config.analytics_specs \
                and config.analytics_specs['stop_on_errors']:
            return False

    # Output everything
    ohandler.output(rc)
    
    return True

def load_config(opts):
    # Load config file
    # ('execfile' does not work here.)
    f = file(opts.config_file, "r")
    conf_file = f.read()
    exec(conf_file)
    config = Config()
    f.close()
    return config

def main_impl(args, mstdout, mstderr):
    opts = parse_cmd_line_opts(args)
    config = load_config(opts)
    mods = Modules(opts.modules_directory, opts, config)
    return execute_cmds(opts, config, mods, mstdout, mstderr)

def main(args, mstdout, mstderr, main_impl=main_impl, exitfun=sys.exit):
    try:
        exitfun(not main_impl(args, mstdout, mstderr))
    except RMTException, rmte:
        mstderr.write("+++ ERROR: Exception occured: %s\n" % rmte)
        exitfun(1)
