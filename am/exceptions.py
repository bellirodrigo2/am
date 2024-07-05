""" Asset Manager Exceptions """

###############################################################################


class AMError(Exception):
    pass


class InconsistentIdTypeError(AMError):
    pass


class ObjHierarchyError(AMError):
    pass


class IdNotFound(AMError):
    pass
