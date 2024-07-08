""""""

from collections.abc import Mapping

import pytest
from sqlalchemy import create_engine, func, insert, join, literal, over, select

from am.repo.sql.get_table import (
    Column,
    Integer,
    String,
    Table,
    label,
    link,
    make_foreign,
    meta,
)
from am.schemas.id_.objectid import ObjectId

node = Table(
    "node",
    meta,
    Column("template", String(64)),
    make_foreign("label", "webid", "webid", String(32), True),
)
item = Table(
    "item",
    meta,
    Column("datatype", Integer),
    make_foreign("label", "webid", "webid", String(32), True),
)


def insert_link(parentid: str, childid: str):
    sstmt = select(
        link.c.parent,
        literal(childid),
        over(func.row_number(), order_by=link.c.depth),
    ).where(link.c.child == parentid)
    return link.insert().from_select(
        ["parent", "child", "depth"],
        sstmt,
    )


def insert_node(parentid: str, base: Mapping, node: Mapping): ...


def insert_items(parentid: str, **item: str): ...


def select_children(id):  # depende do label e link
    j = join(label, link, label.c.webid == link.c.child)
    return select(link).select_from(j).where(link.c.parent == id, link.c.depth == 1)


def select_descendants(id):  # depende do label e link
    j = join(label, link, label.c.webid == link.c.child)
    return (
        select(link)
        .select_from(j)
        .where(link.c.parent == id, link.c.depth > 0)
        .order_by(link.c.depth.asc())
    )


def bootstrap(url: str, echo: bool = False):
    engine = create_engine(url, echo=echo)
    meta.create_all(engine)
    return engine


@pytest.fixture
def db():
    n = 6
    uuids = [str(ObjectId()) for _ in range(2 * n)]
    bases = [
        {
            "webid": uuids[i],
            "name": f"NAME{i}",
            "description": f"DESCR{i}",
            "clientid": f"ID{i}",
        }
        for i in range(2 * n)
    ]
    nodes = [{"webid": uuids[i], "template": f"TEMP{i}"} for i in range(n)]
    items = [{"webid": uuids[i + n], "datatype": i + n} for i in range(n)]
    url = "sqlite://"
    echo = False
    engine = bootstrap(url, echo)

    with engine.begin() as conn:

        stmt = insert(label).values(bases)
        nstmt = insert(node).values(nodes)
        istmt = insert(item).values(items)

        conn.execute(stmt)
        conn.execute(nstmt)
        conn.execute(istmt)
        conn.commit()

    inserts = [
        ("ZERO", uuids[0]),
        (uuids[0], uuids[1]),
        (uuids[0], uuids[2]),
        (uuids[1], uuids[3]),
        (uuids[1], uuids[4]),
        (uuids[2], uuids[5]),
        (uuids[3], uuids[6]),
        (uuids[3], uuids[7]),
        (uuids[4], uuids[8]),
        (uuids[4], uuids[9]),
        (uuids[5], uuids[10]),
        (uuids[6], uuids[11]),
    ]

    for i in range(2 * n):
        with engine.begin() as conn:

            val = {"parent": inserts[i][1], "child": inserts[i][1], "depth": 0}

            isself = insert(link).values(val)
            istmt = insert_link(parentid=inserts[i][0], childid=inserts[i][1])

            conn.execute(isself)
            conn.execute(istmt)
            conn.commit()

    return engine, bases, nodes, items, n, uuids


def test_insert(db):

    engine, bases, nodes, items, n, uuids = db
    with engine.begin() as conn:
        q = select(label)
        res = conn.execute(q)
        assert len(res.fetchall()) == 2 * n

        q = select(node)
        res = conn.execute(q)
        assert len(res.fetchall()) == n

        q = select(item)
        res = conn.execute(q)
        assert len(res.fetchall()) == n

        q = select(link).order_by(link.c.depth)
        res = conn.execute(q)
        assert len(res.fetchall()) == 39

        q = select_children(uuids[0])
        res = conn.execute(q)
        assert len(res.fetchall()) == 2

        q = select_descendants(uuids[0])
        res = conn.execute(q)
        assert len(res.fetchall()) == 2 * n - 1
