import argparse
import requests
import sys

from googlesearch import search


def main():
    parser = argparse.ArgumentParser(
        prog='dorker',
        description='Generate a Google query string',
        epilog='Thanks for using %(prog)s! :)',
    )

    parser.add_argument('search_terms', nargs='+', help='Key words to search for. (Must provide 1 term)')
    parser.add_argument('-e', '--exact', nargs='+', help='Exact search terms')
    parser.add_argument('-a', '--any', nargs='+', help='Any of the search terms')
    parser.add_argument('-n', '--none', nargs='+', help='None of the search terms to be included')
    parser.add_argument('-s', '--site', nargs='+', help='Show results from only these sites')
    parser.add_argument('-f', '--file_type', nargs='+', help='Search for these file types')
    parser.add_argument('-g', '--google', type=int, nargs='?', const=10, help='Query Google and provide '
                        'links to the top results based on the specified number; '
                        'if no number is given, it defaults to 10 results'
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    query_string = query_constructor(args)
    print(f'Query String: {query_string}')

    if args.google is not None:
        if check_internet():
            print(f'\nGoogle\'s top {args.google} results:')
            for result in search(query_string, stop=args.google):
                print(result)
        else:
            print('No Internet Connection: Internet Connection is required to perform Google search')


def query_constructor(args):
    query = ''

    query += ' '.join(args.search_terms)
    query += ' '

    if args.exact is not None:
        query += '('
        query += ' '.join(f'"{term}"' for term in args.exact)
        query += ') '

    if args.any is not None:
        query += '('
        query += ' | '.join(args.any)
        query += ')'

    if args.none is not None:
        query += ' ' + ' '.join(f'-{term}' for term in args.none)
        query += ' '

    if args.site is not None:
        if len(args.site) > 1:
            query += '('
            query += ' | '.join(f'site:{term}' for term in args.site)
            query += ')'
        else:
            query += f'site:{args.site[0]}'
        query += ' '

    if args.file_type is not None:
        if len(args.file_type) > 1:
            query += '('
            query += ' | '.join(f'filetype:{term}' for term in args.file_type)
            query += ')'
        else:
            query += f'filetype:{args.file_type[0]}'

    return query


def check_internet():
    url = 'https://www.google.com'
    timeout = 5

    try:
        response = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


if __name__ == '__main__':
    main()
