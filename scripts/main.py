import os
from config import configure_logger
from config import format_duration
import time

# Configure the shared logger
logger = configure_logger("logfile.log")

##################################################
# Porechop

def run_porechop(fastq_file):

    logger.info("*** Porechop Process ***")
    logger.info("Starting adapter trimming...")
    start_time = time.time()
    logger.info("Running Porechop...")

    if not os.path.exists("adapter_trimmed"):
        os.system('mkdir adapter_trimmed && cd adapter_trimmed && porechop -i ' + fastq_file + ' -o porechoped.fastq 1> porechop_summary.txt')
    else:
        os.system('cd adapter_trimmed && porechop -i ' + fastq_file + ' -o porechoped.fastq 1> porechop_summary.txt')

    # Calculate and log the duration
    end_time = time.time()
    duration = end_time - start_time
    logger.info("Porechop process completed.")
    logger.info(f"Total duration: {format_duration(duration)}\n")

##################################################
# NECAT

def run_necat(project_name, genome_size, threads, porechop_fastq):

    logger.info("*** NECAT Process ***")
    logger.info("Starting necat assembly...")
    start_time = time.time()
    logger.info("Running NECAT...")
    logger.info("Generating config file for necat...")


    if not os.path.exists("NECAT_assembly"):
        os.system('mkdir NECAT_assembly && cd NECAT_assembly && necat.pl config temp_config.txt')
    else:
        os.system('cd NECAT_assembly && necat.pl config temp_config.txt')

    ## get a list of the porechoped fastq file location
    os.system('realpath ' + porechop_fastq + ' > ./NECAT_assembly/read_list.txt')

    ## adding project info to config_file
    os.system('cd NECAT_assembly && sed "s/PROJECT=/PROJECT=' + project_name + '/ ; s/GENOME_SIZE=/GENOME_SIZE=' + str(genome_size) + '/ ; s/ONT_READ_LIST=/ONT_READ_LIST=read_list.txt/ ; s/THREADS=4/THREADS=' + str(threads) + '/" temp_config.txt > ' + project_name + '_config.txt && rm temp_config.txt')
   
    ## run NECAT assembler
    logger.info("Running necat assemlby...")

    ## runnig necat
    os.system('cd NECAT_assembly && necat.pl assemble ' + project_name + '_config.txt')

    ## run NECAT bridge
    logger.info("Running necat bridging...")
    os.system('cd NECAT_assembly && necat.pl bridge ' + project_name + '_config.txt')


    # Calculate and log the duration
    end_time = time.time()
    duration = end_time - start_time
    logger.info("Assembly process completed.")
    logger.info(f"Total duration: {format_duration(duration)}")

##################################################
# Inspector

def activate_conda_environment(env_name):
    os.environ["CONDA_DEFAULT_ENV"] = env_name
    return f"source activate {env_name}"

def run_inspector(final_asm, reads):


    logger.info("*** Assembly evaluation Process ***")
    logger.info("Starting assembly check...")
    start_time = time.time()

    # Define the Conda environment to activate
    conda_environment = "env"

    # Construct the command to run the Inspector
    command = "inspector.py -c {} -r {} -d nanopore -o inspector_output".format(final_asm, reads)
    print(command)
    activate_conda = activate_conda_environment(conda_environment)

    # Execute the Inspector command within the Conda environment
    shell_script = f"""
    #!/bin/bash
    {activate_conda}
    {command}
    """

    with open("script.sh", "w") as file:
        file.write(shell_script)

    logger.info("Running inspector...")

    ## running inspector
    os.system("bash script.sh")
    os.system('rm script.sh')

    # Calculate and log the duration
    end_time = time.time()
    duration = end_time - start_time
    logger.info("Assembly evaluation process completed.")
    logger.info(f"Total duration: {format_duration(duration)}\n")

##################################################
