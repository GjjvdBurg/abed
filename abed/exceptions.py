"""Custom Abed Exceptions

These are all subclasses of the Exception class.

"""


class AbedPBSException(Exception):
    pass


class AbedPBSMultipleException(Exception):
    pass


class AbedHashCollissionException(Exception):
    pass


class AbedNonstandardMetricDirection(Exception):
    pass


class AbedDatasetdirNotFoundException(Exception):
    pass


class AbedMethoddirNotFoundException(Exception):
    pass


class AbedExperimentTypeException(Exception):
    pass
