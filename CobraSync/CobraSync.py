# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import CobraSync.helpers.config_helper
import CobraSync.helpers.fme_helper
import fmeobjects
import tempfile
import sys
import os


def run_sync():
    config = CobraSync.helpers.config_helper.get_config()
    logger = config['LOGGING']['logger']

    logger.info("Temporäres File für GUIDCOL wird bestimmt...")
    tempfile_guidcol = os.path.join(tempfile.mkdtemp(), "guidcol.ffs")
    logger.info(tempfile_guidcol)
    
    logger.info("FME-Script CobraSync wird ausgeführt.")
    fme_main_script =  os.path.splitext(__file__)[0] + ".fmw"
    fme_main_script_logfile = CobraSync.helpers.fme_helper.prepare_fme_log(fme_main_script, config['LOGGING']['log_directory'])
    logger.info("Das FME-Logfile heisst: " + fme_main_script_logfile)
    
    runner = fmeobjects.FMEWorkspaceRunner()
    
    # Der FMEWorkspaceRunner akzeptiert keine Unicode-Strings!
    # Daher müssen workspace und parameters umgewandelt werden!
    parameters = {
        'MSSQL_DATABASE': str(config['MSSQL']['database']),
        'MSSQL_SERVER': str(config['MSSQL']['server']),
        'MSSQL_USERNAME': str(config['MSSQL']['username']),
        'MSSQL_PASSWORD': str(config['MSSQL']['password']),
        'GDBP_DATABASE': str(config['GDBP']['database']),
        'GDBP_USERNAME': str(config['GDBP']['username']),
        'GDBP_PASSWORD': str(config['GDBP']['password']),
        'MYSQL_DATABASE': str(config['MYSQL']['database']),
        'MYSQL_HOST': str(config['MYSQL']['host']),
        'MYSQL_PORT': str(config['MYSQL']['port']),
        'MYSQL_USERNAME': str(config['MYSQL']['username']),
        'MYSQL_PASSWORD': str(config['MYSQL']['password']),
        'PROXY_URL': str(config['EASYSDI_PROXY']['baseurl']),
        'GUIDCOL_FFS': str(tempfile_guidcol),
        'LOGFILE': str(fme_main_script_logfile)
    }
    try:
        runner.runWithParameters(str(fme_main_script), parameters)
    except fmeobjects.FMEException as ex:
        logger.error("FME-Workbench " + fme_main_script + " konnte nicht ausgeführt werden!")
        logger.error(ex)
        logger.error("Import wird abgebrochen!")
        sys.exit()
    
    
    logger.info("FME-Script CobraSync_PostProcessing wird ausgeführt.")
    fme_postprocessing_script =  os.path.splitext(__file__)[0] + "_PostProcessing.fmw"
    fme_postprocessing_script_logfile = CobraSync.helpers.fme_helper.prepare_fme_log(fme_postprocessing_script, config['LOGGING']['log_directory'])
    logger.info("Das FME-Logfile heisst: " + fme_postprocessing_script_logfile)

    runner = fmeobjects.FMEWorkspaceRunner()
    
    # Der FMEWorkspaceRunner akzeptiert keine Unicode-Strings!
    # Daher müssen workspace und parameters umgewandelt werden!
    parameters = {
        'MYSQL_DATABASE': str(config['MYSQL']['database']),
        'MYSQL_HOST': str(config['MYSQL']['host']),
        'MYSQL_PORT': str(config['MYSQL']['port']),
        'MYSQL_USERNAME': str(config['MYSQL']['username']),
        'MYSQL_PASSWORD': str(config['MYSQL']['password']),
        'GDBP_DATABASE': str(config['GDBP']['database']),
        'GDBP_USERNAME': str(config['GDBP']['username']),
        'GDBP_PASSWORD': str(config['GDBP']['password']),
        'GUIDCOL_FFS': str(tempfile_guidcol),
        'LOGFILE': str(fme_postprocessing_script_logfile)
    }
    try:
        runner.runWithParameters(str(fme_postprocessing_script), parameters)
    except fmeobjects.FMEException as ex:
        logger.error("FME-Workbench " + fme_postprocessing_script + " konnte nicht ausgeführt werden!")
        logger.error(ex)
        logger.error("Import wird abgebrochen!")
        sys.exit()
    
    print("SUCCESSFUL")