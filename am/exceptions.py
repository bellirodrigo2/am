""" Asset Manager Exceptions """

###############################################################################


class AMError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class InconsistentIdTypeError(AMError):
    def __init__(self, target: str, webid: str) -> None:
        msg = f"{target=}, {webid=}"
        super().__init__(msg)


class ObjHierarchyError(AMError):
    """"""

    def __init__(self, parent: str, child: str) -> None:
        msg = f"{parent=}, {child=}"
        super().__init__(msg)


class IdNotFound(AMError):
    pass
