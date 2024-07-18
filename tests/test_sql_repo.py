""""""

import json
from pathlib import Path

import pytest

from am.interfaces import Repository
from am.repo.closure import LinkTable
from am.repo.db import bootstrap
from am.repo.repo import SQLRepository
from am.schemas.objrules import WebId, make_input_object


def test_insert_link_ok(): ...


url = "sqlite://"
echo = False

engine = bootstrap(url, echo)

obj_file: Path = Path.cwd() / "tests/objs.json"
with open(file=obj_file) as f:
    inputs = json.load(fp=f)
    assert inputs is not None


@pytest.fixture
def repo() -> Repository:
    link = LinkTable()
    repo = SQLRepository(link, engine)

    return repo


async def test_insert_node_ok(repo: Repository):

    parent = WebId(pref=b"asse")
    target = "node"
    obj1, obj2, obj3 = inputs["nodes"]

    node1 = make_input_object(target, **obj1)
    node2 = make_input_object(target, **obj2)
    node3 = make_input_object(target, **obj3)

    await repo.create(node1, parent)
    await repo.create(node2, node1.web_id)
    await repo.create(node3, node1.web_id)

    read = await repo.read(node1.web_id)
    print(read)

    read2 = await repo.read(node2.web_id, "name", "type", "web_id")
    print(read2)

    read3 = await repo.read(node3.web_id, "name")
    print(read3)


# with Session(engine) as session:

#     n = 12

#     nodes = [
#         Node(web_id=f"{i}", name=f"name{i}", template=f"temp{i}", detached="always")
#         for i in range(n)
#     ]
#     items = [
#         Item(web_id=f"{i}", name=f"name{i}", data_point=f"dp{i}", data_type=f"dt{i}")
#         for i in range(n, 2 * n)
#     ]

#     session.add_all(nodes)

#     session.add_all(items)
#     session.commit()


# with engine.begin() as conn:

#     i01, i1 = link_table.insert_link("0", "1")
#     i02, i2 = link_table.insert_link("0", "2")
#     i03, i3 = link_table.insert_link("1", "3")
#     i04, i4 = link_table.insert_link("1", "4")
#     i05, i5 = link_table.insert_link("2", "5")
#     i06, i6 = link_table.insert_link("2", "6")
#     i07, i7 = link_table.insert_link("3", "7")
#     i08, i8 = link_table.insert_link("7", "8")
#     i09, i9 = link_table.insert_link("5", "9")
#     i010, i10 = link_table.insert_link("5", "10")
#     i011, i11 = link_table.insert_link("10", "11")

#     conn.execute(i01)
#     conn.execute(i02)
#     conn.execute(i03)
#     conn.execute(i04)
#     conn.execute(i05)
#     conn.execute(i06)
#     conn.execute(i07)
#     conn.execute(i08)
#     conn.execute(i09)
#     conn.execute(i010)
#     conn.execute(i011)

#     conn.execute(i1)
#     conn.execute(i2)
#     conn.execute(i3)
#     conn.execute(i4)
#     conn.execute(i5)
#     conn.execute(i6)
#     conn.execute(i7)
#     conn.execute(i8)
#     conn.execute(i9)
#     conn.execute(i10)
#     conn.execute(i11)

#     conn.commit()

# # with Session(engine) as session:
# #     q = session.query(Node)
# #     print(q.all())

# # with Session(engine) as session:
# #     q = session.query(Item)
# #     print(q.all())

# with engine.begin() as conn:

#     stmt = link_table.select_children(Node, "2", "web_id", "name", "template")
#     res = conn.execute(stmt)
#     for r in res:
#         print(r)

# with engine.begin() as conn:

#     stmt = link_table.select_descendants(Node, "2")
#     res = conn.execute(stmt)
#     for r in res:
#         print(r._asdict())  # type: ignore
#         print(int_rep(r._asdict()["type"]))
