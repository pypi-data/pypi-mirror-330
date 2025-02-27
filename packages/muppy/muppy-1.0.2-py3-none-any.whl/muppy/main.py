'''
Muppy means MarkUp Preprocessor for Python. If you want some Python in markup, not
some markup in Python---Muppy is probably the thing you need.

Details: https://pypi.org/project/muppy
Git repo: https://codeberg.org/screwery/muppy
'''

__version__ = '1.0.2'
__repository__ = 'https://codeberg.org/screwery/muppy'
__bugtracker__ = 'https://codeberg.org/screwery/muppy/issues'

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter #

def find_comment(code, index, style, position):
    '''
    Find a comment block in markup/code.
    '''
    result = None
    if style == 'xml':
        if position == 'start':
            result = code.find('<!-- (py):', index), 10
        if position == 'end':
            result = code.find('-->', index), 3
    if style == 'c':
        if position == 'start':
            result = code.find('/* (py):', index), 8
        if position == 'end':
            result = code.find('*/', index), 2
    if style == 'shell':
        if position == 'start':
            result = code.find('# (py):', index), 7
        if position == 'end':
            result = code.find('\n', index), 1
    if style == 'tex':
        if position == 'start':
            result = code.find('% (py):', index), 7
        if position == 'end':
            result = code.find('\n', index), 1
    return result

def literal_name(number):
    '''
    Number to variable name.
    '''
    return f'__muppy{hex(number)[2:]}'

def preprocessor_compile(code, style, placeholder, definitions):
    '''
    Compile preprocessor Python code.
    '''
    intervals = []
    index = 0
    lit_num = 0
    while True:
        new_start, tag_len = find_comment(code, index, style, 'start')
        if new_start != -1:
            intervals.append({
                'type': 'literal',
                'content': code[index:new_start],
                'tag': literal_name(lit_num)
                })
            index = new_start + tag_len
        else:
            intervals.append({
                'type': 'literal',
                'content': code[index:len(code)],
                'tag': literal_name(lit_num)
                })
            break
        new_end, tag_len = find_comment(code, index, style, 'end')
        if new_end != -1:
            lit_num += 1
            intervals.append({
                'type': 'instruction',
                'content': code[index:new_end],
                'tag': literal_name(lit_num)
                })
            index = new_end + tag_len
        else:
            raise RuntimeError(f'Endless comment at position {index}')
    literals, instructions = '', ''
    if definitions is not None:
        for item in definitions:
            instructions += f'{item}\n'
    for item in intervals:
        if item['type'] == 'instruction':
            instructions += item['content'].replace(
                placeholder, item["tag"]
                ) + '\n'
        else:
            literals += f'{item["tag"]} = {repr(item["content"])}\n'
    return literals + instructions

def create_parser():
    '''
    Create CLI arguments parser
    '''
    default_parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f'muppy {__version__}: Markup Preprocessor for Python',
        epilog=f'Bug tracker: {__bugtracker__}'
        )
    default_parser.add_argument('-v', '--version', action='version',
                                version=__version__)
    subparsers = default_parser.add_subparsers(title='Commands', dest='command')
    # Compile parser
    compile_p = subparsers.add_parser('compile', help='compile and execute muppy file')
    compile_p.add_argument('-d', '--def', type=str, nargs='*', dest='definitions',
                          help='Definitions (formatted as Python instructions)')
    compile_p.add_argument('-i', '--input', required=True, type=str,
                          dest='input_file',  help='Input file path (REQUIRED)')
    compile_p.add_argument('-s', '--style', required=True, choices=['xml', 'c', 'shell', 'tex'],
                          dest='style', help='Comment style (REQUIRED)')
    compile_p.add_argument('-p', '--placeholder', type=str, default='?????',
                          dest='placeholder', help='Literal placeholder (default: "?????")')
    compile_p.add_argument('-c', '--code', type=str, default='',
                          dest='code_file',
                          help='Save preprocessor Python code in specified file (DEFAULT: none)')
    compile_p.add_argument('-n', '--noexec', action='store_true',
                          dest='no_exec', help='Do not execute preprocessor (DEFAULT: false)')
    return default_parser

def main():
    '''
    Main function (entrypoint)
    '''
    parser = create_parser()
    nmsp = parser.parse_args(sys.argv[1:])
    if nmsp.command == 'compile':
        with open(nmsp.input_file, 'rt', encoding='utf-8') as stream:
            code = stream.read()
        ppcode = preprocessor_compile(code, nmsp.style, nmsp.placeholder,
                                      nmsp.definitions)
        if nmsp.code_file:
            with open(nmsp.code_file, 'wt', encoding='utf-8') as stream:
                stream.write(ppcode)
        if not nmsp.no_exec:
            exec(ppcode)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
