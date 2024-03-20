from main import run_porechop
from main import run_necat
from main import run_inspector
from dorado import run_dorado
import argparse
import os
import shutil

##################################################

parser=argparse.ArgumentParser(description='FHAGON - long read assembly pipeline')

## raw_reads or fastq_reads argument setting
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--raw_reads', metavar='', help='Path to raw pod5 files')
group.add_argument('-q', '--fastq', metavar='',  help='Path to fastq files [Only if basecalling is not required.]')

# Add additional arguments to the group if -r is selected
raw_reads_group = parser.add_argument_group('If basecalling is required please provide following:')
raw_reads_group.add_argument('-m', '--basecall_model', metavar='', help='Basecalling model - Please specify the model based on the sequecing kit.')
raw_reads_group.add_argument('-b', '--basecall_type', metavar='', default='basecaller', help='Type of basecalling - simplex (default) or duplex.')

parser.add_argument('-g', '--genome_size', metavar='', type=int, help='Estimated size of the genome', required=True)
parser.add_argument('-t', '--threads', metavar='', type=int, default=12, help='Number of threads')
parser.add_argument('-p', '--project', metavar='', type=str, default='my_project', help='Name of the project')
parser.add_argument('-o', '--output', metavar='', type=str, default='fhgaon_output', help='Output directory path')


args = parser.parse_args()

##################################################
# Create the output directory if it doesn't exist
output_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.output)))
os.makedirs(output_dir, exist_ok=True)

##################################################

if args.fastq:
    fastq_location = os.path.abspath(os.path.expanduser(os.path.expandvars(args.fastq)))

# Change the current working directory to the output directory
os.chdir(output_dir)

# running dorado

if args.raw_reads:
    pod5_path = os.path.abspath(os.path.expanduser(os.path.expandvars(args.raw_reads)))
    model = args.basecall_model
    type = args.basecall_type
    run_dorado(type, model, pod5_path)
    fastq_location = os.path.abspath(os.path.expanduser(os.path.expandvars("dorado_output.fastq")))

    
## print('fastq_path', fastq_location)
# running porechop

run_porechop(fastq_location)

## get porechoped fastq file location
porechop_fastq_path = os.path.abspath(os.path.expanduser(os.path.expandvars("./adapter_trimmed/porechoped.fastq")))

# running necat

proj = args.project
thread = args.threads
g_size = args.genome_size

run_necat(proj, g_size, thread, porechop_fastq_path)

## get porechoped fastq file location
necat_final_asm_path = os.path.abspath(os.path.expanduser(os.path.expandvars('NECAT_assembly/' + proj + '/6-bridge_contigs/polished_contigs.fasta')))

# running inspector

run_inspector(necat_final_asm_path, porechop_fastq_path)

# copying the final polished assembly to output folder
shutil.copy(necat_final_asm_path, output_dir)
