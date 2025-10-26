import argparse


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(ArgParser, self).__init__(
            description="Filtering and aggregating CSV files."
        )
        self.add_argument(
            "--files", nargs="+", required=True, help="Path to CSV files."
        )
        self.add_argument(
            "--report",
            help="Creating <report-name> with given files.",
        )
