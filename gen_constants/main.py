from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, Sequence

from .__version__ import VERSION
from .config import parse_config
from .generate import generate_c, generate_python

SUPPORTED_LANGUAGES = {
    'c': { 'suffix': '.h', 'fn': generate_c },
    'python': { 'suffix': '.py', 'fn': generate_python },
}


def parse_args(args: Optional[Sequence[str]]) -> Namespace:
    parser = ArgumentParser(prog=__package__, description='Auto-generate definition files for various languages')

    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s v{VERSION}')

    for lang in SUPPORTED_LANGUAGES:
        parser.add_argument(
            f'--generate-{lang}', action='store_true',
            help=f'Generates {lang.capitalize()} compatible file for the constants'
        )

    parser.add_argument(
        '--out-dir', type=Path, default='.', help='Places the generated files in the specified directory.'
    )

    parser.add_argument(
        'config', type=Path, metavar='CONFIG', help='The config file to use to generate the code'
    )

    return parser.parse_args(args)


def main(args: Optional[Sequence[str]] = None) -> None:
    args = parse_args(args)

    constants = parse_config(args.config)

    args.out_dir.mkdir(exist_ok=True)

    for lang, lang_dict in SUPPORTED_LANGUAGES.items():
        if getattr(args, f'generate_{lang}'):
            with open(args.out_dir / args.config.with_suffix(lang_dict['suffix']).name, 'w') as f:
                lang_dict['fn'](constants, f)
