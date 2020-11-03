# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import AGILib
import tempfile
import sys
import os

def init_logging(config):
    log_directory = config['LOGGING']['basedir']
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logger = AGILib.agilogger.initialize_agilogger(logfile_name="CobraSync.log", logfile_folder=log_directory, list_log_handler=['file', 'stream'], archive=True, logger_name="CobraSyncLogger")        
    return logger

def run_sync():
    config = AGILib.Configuration(configfile_envvar='COBRASYNCHOME').config
    logger = init_logging(config)

    logger.info("Temporäres File für GUIDCOL wird bestimmt...")
    tempfile_guidcol = os.path.join(tempfile.mkdtemp(), "guidcol.ffs")
    logger.info(tempfile_guidcol)
    
    logger.info("FME-Script CobraSync wird ausgeführt.")
    fme_main_script =  os.path.splitext(__file__)[0] + ".fmw"
    fme_main_script_logfile = os.path.join(config['LOGGING']['basedir'], os.path.split(fme_main_script)[1].replace(".fmw","_fme.log"))
    logger.info("Das FME-Logfile heisst: " + fme_main_script_logfile)

    parameters = {
        'MSSQL_DATABASE': config['MSSQL']['database'],
        'MSSQL_SERVER': config['MSSQL']['server'],
        'MSSQL_USERNAME': config['MSSQL']['username'],
        'MSSQL_PASSWORD': config['MSSQL']['password'],
        'GDBP_DATABASE': config['GDBP']['database'],
        'GDBP_USERNAME': config['GDBP']['username'],
        'GDBP_PASSWORD': config['GDBP']['password'],
        'MYSQL_DATABASE': config['MYSQL']['database'],
        'MYSQL_HOST': config['MYSQL']['host'],
        'MYSQL_PORT': unicode(config['MYSQL']['port']),
        'MYSQL_USERNAME': config['MYSQL']['username'],
        'MYSQL_PASSWORD': config['MYSQL']['password'],
        'PROXY_URL': config['EASYSDI_PROXY']['baseurl'],
        'GUIDCOL_FFS': tempfile_guidcol,
        'LOGFILE': fme_main_script_logfile
    }

    fmerunner = AGILib.FMERunner(fme_workbench=fme_main_script, fme_workbench_parameters=parameters, fme_logfile=fme_main_script_logfile, fme_logfile_archive=True)
    fmerunner.run()
    if fmerunner.returncode != 0:
        logger.error("FME-Script %s abgebrochen." % (fme_main_script))
        raise RuntimeError("FME-Script %s abgebrochen." % (fme_main_script))
    
    if os.path.isfile(tempfile_guidcol):
        logger.info("FME-Script CobraSync_PostProcessing wird ausgeführt.")
        fme_postprocessing_script =  os.path.splitext(__file__)[0] + "_PostProcessing.fmw"
        fme_postprocessing_script_logfile = os.path.join(config['LOGGING']['basedir'], os.path.split(fme_postprocessing_script)[1].replace(".fmw","_fme.log"))
        logger.info("Das FME-Logfile heisst: " + fme_postprocessing_script_logfile)
    
        parameters = {
            'MYSQL_DATABASE': config['MYSQL']['database'],
            'MYSQL_HOST': config['MYSQL']['host'],
            'MYSQL_PORT': unicode(config['MYSQL']['port']),
            'MYSQL_USERNAME': config['MYSQL']['username'],
            'MYSQL_PASSWORD': config['MYSQL']['password'],
            'GDBP_DATABASE': config['GDBP']['database'],
            'GDBP_USERNAME': config['GDBP']['username'],
            'GDBP_PASSWORD': config['GDBP']['password'],
            'GUIDCOL_FFS': tempfile_guidcol,
            'LOGFILE': fme_postprocessing_script_logfile
        }
        fmerunner = AGILib.FMERunner(fme_workbench=fme_postprocessing_script, fme_workbench_parameters=parameters, fme_logfile=fme_postprocessing_script_logfile, fme_logfile_archive=True)
        fmerunner.run()
        if fmerunner.returncode != 0:
            logger.error("FME-Script %s abgebrochen." % (fme_postprocessing_script))
            raise RuntimeError("FME-Script %s abgebrochen." % (fme_postprocessing_script))
    else:
        logger.info("Temporäres GUIDCOL-File existiert nicht.")
        logger.info("FME-Script CobraSync_PostProcessing wird daher nicht ausgeführt.")
    
    print("SUCCESSFUL")