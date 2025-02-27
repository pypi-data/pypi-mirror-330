import argparse
import pkg_resources

def version():
    """Returns the installed version of SJM."""
    return pkg_resources.get_distribution("sjm").version

def main():
    parser = argparse.ArgumentParser(description="SJM CLI")
    parser.add_argument("--version", "-v", action="store_true", help="Show SJM version")

    args = parser.parse_args()

    if args.version:
        print(version())

if __name__ == "__main__":
    main()

