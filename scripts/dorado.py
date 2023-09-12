import sys
import glob
import os
from config import configure_logger
from config import format_duration
import time


logger = configure_logger("logfile.log")


# Basecalling with dorado
## need pod5 files (so convert fast5 to pod5, if required)
## mode : duplex or simplex
## config file: download and put in the same folder

def run_dorado(basecall_type, basecall_model, pod5_files):
    logger.info("*** Dorado basecalling Process ***")
    logger.info("Starting basecalling...")
    start_time = time.time()
    logger.info("Checking operating system...")
    # check the operating system of the host machine
    operating_system = ''
    if sys.platform.startswith('darwin'):
        operating_system = 'osx'

        # required library installation
        if not os.path.exists("/opt/homebrew/opt/libaec/lib/libsz.2.dylib"):
            os.system('brew install libaec')

    elif sys.platform.startswith('linux'):
        operating_system = 'linux'

    elif sys.platform.startswith('win32'):
        operating_system = 'win'


    # check if required dorado software file is provided by the user
    dorado_file_pattern = 'dorado-*64'

    files = glob.glob(dorado_file_pattern)

    # Check if any files matching the pattern exist
    if len(files) > 0:
        for file in files:
            if operating_system in file:
                if not os.path.exists(file):
                    os.system('tar -xvf ' + file)
                else:
                    # get the path of dorado 
                    dorado_basecaller = os.path.abspath(os.path.expanduser(os.path.expandvars(file + '/bin/dorado')))

    else:
        logger.error("Please download the required dorado software from https://github.com/nanoporetech/dorado")
        print("Please download the required dorado software from https://github.com/nanoporetech/dorado")
        quit()


    ## basecalling model setting and location
    if basecall_model is None:
        logger.error('Error: Please provide the basecalling model. -m not given \n Abort.\n')
        print('Error: Please provide the basecalling model. -m not given \n Abort.\n')
        quit()
    elif not os.path.exists(basecall_model):
        os.system(dorado_basecaller + ' download --model ' + basecall_model)
        basecalling_model = os.path.abspath(os.path.expanduser(os.path.expandvars(basecall_model)))
    else:
        basecalling_model = os.path.abspath(os.path.expanduser(os.path.expandvars(basecall_model)))


    logger.info("Running dorado...")
    os.system(dorado_basecaller + ' ' + basecall_type + ' ' + basecalling_model + ' ' + pod5_files + '/ --emit-fastq > dorado_output.fastq')


    # Calculate and log the duration
    end_time = time.time()
    duration = end_time - start_time
    logger.info("Basecalling process completed.")
    logger.info(f"Total duration: {format_duration(duration)}\n")

####################################################################################