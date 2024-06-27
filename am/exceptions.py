""" Asset Manager Exceptions """

###############################################################################


class AMError(Exception):
    pass


class WebIdValidationError(AMError):
    pass


class AssetHierarchyError(AMError):
    pass


class AMValidationError(AMError):
    pass
