#!/usr/bin/python3

# -*- coding:utf-8 -*-

import os
import re
import sys
import argparse
import subprocess
import pandas as pd
from Bio import SeqIO
import shutil
# from .cgmlst_core import mlst
from tabulate import tabulate
from cvmblaster.blaster import Blaster
from cvmcore.cvmcore import cfunc
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Config:
    DEFAULT_THREADS = 8
    DEFAULT_MIN_ID = 95
    DEFAULT_MIN_COV = 95
    DATABASE_DIR = 'db'


def get_database_path() -> Path:
    """Return the path to the database directory."""
    return Path(__file__).parent / Config.DATABASE_DIR


def args_parse():
    parser = argparse.ArgumentParser(
        description='cgMLST analysis tool',
        usage='cvmcgmlst -i <genome assemble directory> -o <output_directory>'
    )

    subparsers = parser.add_subparsers(dest='subcommand')

    # Simplified subparser creation
    subparsers.add_parser('show_db', help="Show available databases")
    subparsers.add_parser('init', help='Initialize reference database')

    create_parser = subparsers.add_parser(
        'create_db', help='<add custome database, use cvmcgmlst createdb -h for help>')
    create_parser.add_argument(
        '-file', required=True, help='Fasta format reference file')
    create_parser.add_argument('-name', required=True, help='Database name')
    create_parser.add_argument(
        '-force', action="store_true", help='Force create database')

    # Main parser arguments
    parser.add_argument("-i", help="Input genome assembly file path")
    parser.add_argument('-db', help="cgMLST database name")
    parser.add_argument("-o", help="Output directory path")
    parser.add_argument('-minid', type=float, default=Config.DEFAULT_MIN_ID,
                        help=f"Minimum identity threshold (default: {Config.DEFAULT_MIN_ID})")
    parser.add_argument('-mincov', type=float, default=Config.DEFAULT_MIN_COV,
                        help=f"Minimum coverage threshold (default: {Config.DEFAULT_MIN_COV})")
    parser.add_argument('-t', type=int, default=Config.DEFAULT_THREADS,
                        help=f'Number of threads (default: {Config.DEFAULT_THREADS})')
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='Display version')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args


def read(rel_path: str) -> str:
    """Read file content from a relative path using pathlib.

    Args:
        rel_path: Relative path to the file

    Returns:
        The content of the file as a string
    """
    here = Path(__file__).parent.resolve()
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return (here / rel_path).read_text()


def get_rel_path():
    """
    Get the relative path
    """
    here = os.path.abspath(os.path.dirname(__file__))
    return here


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def initialize_db():
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    # print(database_path)
    fsa_files = 0
    for file in os.listdir(database_path):
        # print(file)
        if file.endswith('.fsa'):
            fsa_files += 1
            file_path = os.path.join(database_path, file)
            file_base = os.path.splitext(file)[0]
            out_path = os.path.join(database_path, file_base)
            seq_type = cfunc.check_sequence_type(file_path)
            if seq_type == 'DNA':
                Blaster.makeblastdb(file_path, out_path, db_type='nucl')
            elif seq_type == 'Amino Acid':
                Blaster.makeblastdb(file_path, out_path, db_type='prot')
            else:
                print('Unknown sequence type, exit ...')
        else:
            next
    if fsa_files == 0:
        print('No valid reference file exist...')
        sys.exit(1)


def create_db(fasta_file: Path, db_name: str, force: bool = False) -> None:
    """Create a new database from a fasta file."""
    database_path = get_database_path()
    dest_file = database_path / f'{db_name}.fsa'

    if dest_file.exists() and not force:
        raise ValueError(
            f"Database {db_name} already exists. Use -force to overwrite.")

    if dest_file.exists() and force:
        dest_file.unlink()

    shutil.copy(str(fasta_file), str(dest_file))
    blastdb_out = database_path / db_name
    print(f"Adding {db_name} to database...")
    Blaster.makeblastdb(str(dest_file), str(blastdb_out), db_type='nucl')


def check_db():
    """
    ruturn database list
    """
    db_list = []
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    for file in os.listdir(database_path):
        if file.endswith('.fsa'):
            db_name = os.path.splitext(file)[0]
            db_list.append(db_name)
    return db_list


def show_db_list():
    """
    Convert the ResBlaster database to tidy dataframe
    Paramters
    ----------

    Returns
    ----------
    A tidy dataframe contains the blast database name and No. of seqs in database and the last modified date

    """
    here = get_rel_path()
    db_path = os.path.join(here, 'db')
    db_list = []
    for file in os.listdir(db_path):
        file_path = os.path.join(db_path, file)
        if file_path.endswith('.fsa'):
            db_dict = {}
            fasta_file = os.path.basename(file_path)
            file_base = os.path.splitext(fasta_file)[0]
            num_seqs = len(
                [1 for line in open(file_path) if line.startswith(">")])
            update_date = cfunc.get_mod_time(file_path)
            db_dict['DB_name'] = file_base
            db_dict['No. of seqs'] = num_seqs
            db_dict['Update_date'] = update_date
            db_list.append(db_dict)
        else:
            next

    db_df = pd.DataFrame(db_list)
    db_df = db_df.sort_values(by='DB_name', ascending=True)
    tidy_db_df = tabulate(db_df, headers='keys', showindex=False)
    return print(tidy_db_df)


def process_genome(input_file: Path, database: str, output_dir: Path,
                   threads: int, min_id: float, min_cov: float) -> None:
    """Process a single genome file."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not cfunc.is_fasta(str(input_file)):
        raise ValueError(f"Input file is not in FASTA format: {input_file}")

    output_file = output_dir / f"{input_file.stem}_tab.txt"
    database_path = get_database_path() / database

    print(f'Processing {input_file}')
    result = Blaster(str(input_file), str(database_path),
                     str(output_dir), threads, min_id, min_cov).mlst_blast()

    # df = pd.DataFrame.from_dict(result, orient='index') if result else pd.DataFrame(columns=['Allele_Num'])
    if result:
        df = pd.DataFrame.from_dict(result, orient='index')
        df.rename(columns={0: 'Allele_Num'}, inplace=True)
    else:
        df = pd.DataFrame(columns=['Allele_Num'])
    df.index.name = 'Loci'
    df.to_csv(output_file, sep='\t', index=True)
    print(f"Results written to {output_file}")


def main():
    args = args_parse()

    if args.subcommand is None:
        output_dir = Path(args.o)
        output_dir.mkdir(exist_ok=True)

        if args.db not in check_db():
            print(
                f"Database {args.db} not found. Use 'cvmcgmlst show_db' to list available databases.")
            sys.exit(1)

        try:
            process_genome(
                input_file=Path(args.i),
                database=args.db,
                output_dir=output_dir,
                threads=args.t,
                min_id=args.minid,
                min_cov=args.mincov
            )
        except Exception as e:
            print(f"Error processing genome: {e}")
            sys.exit(1)

    elif args.subcommand == 'show_db':
        show_db_list()
    elif args.subcommand == 'init':
        initialize_db()
    elif args.subcommand == 'create_db':
        try:
            create_db(Path(args.file), args.name, args.force)
        except Exception as e:
            print(f"Error creating database: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
