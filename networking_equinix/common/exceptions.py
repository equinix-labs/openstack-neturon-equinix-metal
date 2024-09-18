# networking_equinix/common/exceptions.py

class EquinixRpcError(Exception):
    """Exception raised for errors in the Equinix Metal API request."""
    def __init__(self, msg=None):
        self.msg = msg or "An error occurred in the Equinix Metal API request."
        super(EquinixRpcError, self).__init__(self.msg)
