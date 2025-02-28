import argparse
import logging
import sys
import os
import traceback
from argparse import RawTextHelpFormatter

from pathlib import Path
from json.decoder import JSONDecodeError
from pydantic import ValidationError

from upgen import __version__
from upgen.model import *
from upgen.generators import EtherCATGenerator
from upgen.generators import ProfinetGenerator
from upgen.generators import EthernetipGenerator
from upgen.generators import CCodeGenerator
from upgen.generators import SIIGenerator

_logger = logging.getLogger(__name__)

GENERATORS = {
    'EtherCAT': EtherCATGenerator,
    'Profinet': ProfinetGenerator,
    "EtherNetIP":EthernetipGenerator,
        'Code': CCodeGenerator,
         'SII': SIIGenerator,

}


def get_generator_classes(name):
    if name == 'All':
        return [GENERATORS[g] for g in GENERATORS]
    try:
        return [GENERATORS[name]]
    except KeyError:
        raise ValueError(f"--generator name must be in {tuple(GENERATORS)} or \'All\')")


def parse_args(args):
    parser = argparse.ArgumentParser(description=
    """
    Tool for generation of device artifacts from a U-Phy device model
    file, including:
    - C-code with the device specific data model
    - EtherCAT ESI file
    - EtherCAT SII EEPROM file
    - Profinet GSDML file

    To evaluate the device functionality, copy generated model.c/h and
    eeprom.bin to the \'generated\' folder of the U-Phy sample application
    and rebuild.

    Example usage:
        upgen export my_device_model.json
    """,
    formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--version",
        action="version",
        version=f"upgen {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument("-d", "--destination", help="destination folder for generated model", default=".")

    parser.add_argument('--generator', help="the generator to use. Option value "
                        "can be one of  {} or \'All\'. Default value is \'All\'".format(tuple(GENERATORS)), default="All")

    parser.add_argument('-n', '--device_name', help="the name of the device to generate. "
                        "Only used when generating C code or SII eeprom for multi device models.")

    # Import device description file or
    # Export source code and device description files from json model
    # TODO - for export the generators for fieldbuses defined by the
    # model should be run. All outputs placed in the destination folder.
    parser.add_argument('action', choices=('import', 'export', 'schema'))
    parser.add_argument("file", help="Device model in JSON format")

    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    if loglevel is None:
        loglevel = logging.WARNING
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.action == 'import':
        raise Exception( "import not supported")
        generator_class = get_generator_class(args.generator)
        generator = generator_class(None)
        generator.import_file(args.file)
        print(generator.model)

    elif args.action == 'export':
        try:
            model = Root.parse_file(Path(args.file))
        except (JSONDecodeError, ValidationError) as e:
            print(e)
            sys.exit(1)

        os.makedirs(args.destination, exist_ok=True)
        os.chdir(args.destination)
        generator_classes = get_generator_classes(args.generator)
        for gen_cls in generator_classes:
            try:
                generator = gen_cls(model)
                if (gen_cls in [CCodeGenerator, SIIGenerator, EthernetipGenerator]):
                    generator.select_device(args.device_name)
                generator.export_file()
            except Exception as e:
                print(
                    f"Error while running {gen_cls.__name__}: \"{str(e)}\" Continue generating rest of artifacts.")
                _logger.warning(''.join(traceback.TracebackException.from_exception(e).format()))

    elif args.action == 'schema':
        print(Root.schema_json(indent=2))

    _logger.info("Script ends here")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
