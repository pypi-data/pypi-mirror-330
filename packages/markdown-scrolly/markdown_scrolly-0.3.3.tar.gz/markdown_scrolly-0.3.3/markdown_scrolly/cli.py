import argparse
from .mdparser import convert_file_markdown

def main():

    #### fname, signature='', date='today', extensions=[]):
    parser = argparse.ArgumentParser(
        prog = 'scrolly',
        description='Markdown formatter to html with scroll animations.',
        epilog= '\n'
    )
    parser.add_argument(
        '-s', '--signature', type=str,
        help="String to include as signature"
    )
    parser.add_argument(
        '-d', '--date', type=str,
        help="Date string to include at the end of document(default: 'today')"
    )
    parser.add_argument(
        '-e', '--extensions', nargs='*',
        help="List of extensions to markdown parser to be included"
    )
    parser.add_argument(
        "filename", type=str, 
        help="The filename of the .md to be processed"
    )

    args = parser.parse_args()

    kwargs = {}
    if args.signature is not None:
        kwargs['signature'] = args.signature
    if args.date is not None:
        kwargs['date'] = args.date
        
    convert_file_markdown(args.filename, **kwargs)

if __name__ == "__main__":
    main()