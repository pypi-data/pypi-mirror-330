import argparse
from f1_report_by_viacent.functions import build_report, driver_report, print_report

def main():
    """
    Function parse arguments
    """
    parser = argparse.ArgumentParser(description="Formula 1 Report Generator")
    parser.add_argument('--files', type=str, required=True, help="Path to the folder containing log files")
    parser.add_argument('--asc', action='store_true', help="Sort results in ascending order")
    parser.add_argument('--desc', action='store_true', help="Sort results in descending order")
    parser.add_argument('--driver', type=str, help="Display statistics for a specific driver")
    args = parser.parse_args()
    if args.asc and args.desc:
        parser.error("Dont use both --asc & --desc")
    order = 'desc' if args.desc else 'asc'
    report = build_report(args.files, order)
    if args.driver:
        driver_report(report, args.driver)
    else:
        print_report(report)

if __name__ == '__main__':
    main()
