from sqlalchemy import Column, Insert, Select, Table, func, insert, join, over, select


class ClosureJoinTable:

    def __init__(self, labeltab: Table, linktab: Table):
        self._labeltab = labeltab
        self._linktab = linktab
        self._join = join(
            self._labeltab,
            self._linktab,
            self.id == self.child,
        )

    @property
    def id(self) -> Column:
        return self._labeltab.c["webid"]

    @property
    def parent(self) -> Column:
        return self._linktab.c["parent"]

    @property
    def child(self) -> Column:
        return self._linktab.c["child"]

    @property
    def depth(self) -> Column:
        return self._linktab.c["depth"]

    def insert(self, id) -> Insert:

        sstmt = select(
            self.parent,
            self.id,
            over(func.row_number(), order_by=self.depth),
        ).where(self.child == id)

        istmt = insert(self._linktab).from_select(
            ["parent", "child", "depth"],
            sstmt,
        )
        return istmt

    def select_children(self, id, sstmt: Select) -> Select:

        return sstmt.select_from(self._join).where(self.parent == id, self.depth == 1)

    def select_descendants(self, id, sstmt: Select) -> Select:

        return (
            sstmt.select_from(self._join)
            .where(self.parent == id, self.depth > 0)
            .order_by(self.depth.asc())
        )


class ObjectJoinTable:

    def __init__(self, labeltab: Table, objtab: Table):
        self._labeltab = labeltab
        self._objtab = objtab
        self._join = join(
            self._labeltab,
            self._objtab,
            self.labelid == self.objid,
        )

    @property
    def labelid(self) -> Column:
        return self._labeltab.c["webid"]

    @property
    def objid(self) -> Column:
        return self._objtab.c["webid"]

    def insert(self, obj) -> Insert:

        istmt = insert(self._objtab).values(obj)
        return istmt

    def read(self, sstmt: Select) -> Select:

        return sstmt.select_from(self._join)

    def update(self): ...
    def delete(self): ...
