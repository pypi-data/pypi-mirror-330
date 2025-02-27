"""
A message publisher and listener for native Python objects, NumPy Arrays, and pandas Series/Dataframes.

This script demonstrates the capability to transmit native Python objects, NumPy arrays, and pandas series/dataframes using
the MiddlewareCommunicator within the Wrapyfi library. The communication follows the PUB/SUB pattern
allowing message publishing and listening functionalities between processes or machines.

Demonstrations:
    - Using the NativeObject message
    - Transmitting a nested dummy Python object with native objects, NumPy arrays, and pandas series/dataframes
    - Applying the PUB/SUB pattern with mirroring

Requirements:
    - Wrapyfi: Middleware communication wrapper (refer to the Wrapyfi documentation for installation instructions)
    - YARP, ROS, ROS 2, ZeroMQ (refer to the Wrapyfi documentation for installation instructions)
    - NumPy: Used for creating arrays (installed with Wrapyfi)
    - pandas: Used for creating and handling series and dataframes
    - PyArrow: Used for compatibility with pandas>=2.0. It is not required by pandas but required for this example when installing pandas >= 2.0. Not required for pandas < 2.0.

    Install using pip:
        ``pip install "pandas<2.0"``  # Basic installation of pandas<2.0 with Numpy as a dependency (for compatibility)
        ################## OR ##################
        ``pip install "pandas>=2.0" pyarrow``  # Basic installation of pandas>=2.0 with PyArrow as a dependency (for compatibility)

Run:
    # On machine 1 (or process 1): Publisher waits for keyboard input and transmits message
        ``python3 numpy_pandas_example.py --mode publish``

    # On machine 2 (or process 2): Listener waits for message and prints the entire dummy object
        ``python3 numpy_pandas_example.py --mode listen``
"""

import argparse

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Install pandas and NumPy before running this script.")

from wrapyfi.connect.wrapper import MiddlewareCommunicator, DEFAULT_COMMUNICATOR


class Notifier(MiddlewareCommunicator):
    @MiddlewareCommunicator.register(
        "NativeObject",
        "$mware",
        "Notifier",
        "/notify/test_native_exchange",
        carrier="tcp",
        should_wait=True,
    )
    def exchange_object(self, mware=None):
        """
        Exchange messages with NumPy arrays, pandas series/dataframes, and other native Python objects.
        """
        msg = input("Type your message: ")

        ret = {
            "message": msg,
            "numpy_array": np.ones((2, 4)),
            "pandas_series": pd.Series(
                [1, 3, 5, np.nan, 6, 8],
                dtype="float32" if pd.__version__ < "2.0" else "float32[pyarrow]",
            ),
            "pandas_dataframe": pd.DataFrame(
                np.random.randn(6, 4),
                index=pd.date_range("20130101", periods=6),
                columns=list("ABCD"),
            ),
        }
        return (ret,)


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A message publisher and listener for native Python objects, NumPy arrays, and pandas series/dataframes."
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="publish",
        choices={"publish", "listen"},
        help="The transmission mode",
    )
    parser.add_argument(
        "--mware",
        type=str,
        default=DEFAULT_COMMUNICATOR,
        choices=MiddlewareCommunicator.get_communicators(),
        help="The middleware to use for transmission",
    )
    return parser.parse_args()


def main(args):
    """
    Main function to initiate Notifier class and communication.
    """
    notifier = Notifier()
    notifier.activate_communication(Notifier.exchange_object, mode=args.mode)

    while True:
        (msg_object,) = notifier.exchange_object(mware=args.mware)
        print("Method result:", msg_object)


if __name__ == "__main__":
    args = parse_args()
    main(args)
