# Test the croniter functions when constructing croniter strings

import argparse
import os
import lib.tags as tags

def parse_arg() -> argparse.Namespace:
    """Parse input arguments.

    Returns:
        argparse object with parsed arguments.
    """

    parser = argparse.ArgumentParser(prog=os.path.basename(__file__))

    parser.add_argument("cron", help="Test CROn string")
    parser.add_argument("region", help="VCFaaS Director region.")

    return parser.parse_args()



def main() -> int:

    # parse input arguments
    args = parse_arg()

    # Check region
    if not tags.is_valid_region(args.region):
        print(f'ERROR: {args.region} is not a registered region.')
        exit()
    else:
        print("region valid")

    # Check cron string
    if not tags.is_valid_cron(args.cron):
        print(f'ERROR: {args.cron} is not a valid cron string')
        exit()
    else:
        print("cron string valid")

    # Calculate the time to next execution
    now = tags.get_now(args.region)
    next = tags.next_exec(args.cron, now)
    delta = now - next
    print(f'Current time in region {args.region} : {now}')
    print(f'Next execution time - {next}')

if __name__ == "__main__":
    exit(main())

