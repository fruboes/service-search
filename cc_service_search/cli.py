"""Console script for cc_service_search."""
import argparse
import sys
import cc_service_search


def main():
    """Console script for cc_service_search."""
    allowed_actions = "dropdb initdb upload compare".split()

    parser = argparse.ArgumentParser()
    parser.add_argument('action', help="Action to perform. Known actions: " + "/".join(allowed_actions))
    parser.add_argument("--dry-run", action="store_true", default=False, help="Do not perform any writes/changes to db")
    parser.add_argument("--file", action="store", default=None, help="xls input file")

    args = parser.parse_args()

    if args.action not in allowed_actions:
        print(f"Action {args.action} not known. Allowed actions: {'/'.join(allowed_actions)}")
        sys.exit(1)

    if args.action in ["compare", "upload"]:
        if args.file is None:
            print("Input file missing (use --file to provide)")
            sys.exit(1)

    if args.action == "dropdb":
        cc_service_search.drob_db(args)
    elif args.action == "initdb":
        cc_service_search.init_db(args)
    elif args.action == "upload":
        cc_service_search.upload(args, quiet=True)
    elif args.action == "compare":
        args.dry_run = True
        cc_service_search.upload(args, quiet=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
