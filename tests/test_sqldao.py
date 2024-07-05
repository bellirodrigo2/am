""""""

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    join,
    select,
)

meta = MetaData()

basetable = Table(
    "baseobj/",
    meta,
    # aqui precisa de dois obj, ou da pra fazer tudo em 1 ????
    Column("webid", String(32), primary_key=True),
    Column("objid", BigInteger),
    Column("name", String(64)),
)

treetable = Table(
    "tree",
    meta,
    Column("parent", BigInteger, ForeignKey(basetable.c.objid), primary_key=True),
    Column("child", BigInteger, ForeignKey(basetable.c.objid), primary_key=True),
    Column("depth", Integer),
)

nodetable = Table(
    "node",
    meta,
    Column("objid", BigInteger, ForeignKey(basetable.c.objid), primary_key=True),
    Column(
        "template",
        String(64),
    ),
)

itemtable = Table(
    "item",
    meta,
    Column("objid", BigInteger, ForeignKey(basetable.c.objid), primary_key=True),
    Column(
        "datatype",
        Integer,
    ),
)


def bootstrap(url: str, echo: bool = False):
    engine = create_engine(url, echo=echo)
    meta.create_all(engine)
    return engine


if __name__ == "__main__":

    node = {"webid": "foobar", "objtype": "node", "name": "RBELL", "template": "TEMP1"}
    item = {"webid": "foobar", "objtype": "item", "name": "itemname", "datatype": 5}
    print(spin(node, Node))
    print(spin(item, Item))

    # PENSAR COMO FAZER O JOIN QDO DER SELECT COM JOIN....WEBID VAI SER DUPLICADO ???

    try:
        spin(node, Item)
    except Exception as e:
        print("--->", e)

    try:
        spin(item, Node)
    except Exception as e:
        print("--->", e)
#     url = "sqlite://"
#     echo = False
#     engine = bootstrap(url, echo)

#     n = 6
#     uuids = [str(uuid1()) for _ in range(n)]
#     bases = [{"webid": uuids[i], "name": f"NAME{i}"} for i in range(n)]
#     nodes = [{"webid": uuids[i], "template": f"TEMP{i}"} for i in range(n)]
#     items = [{"webid": uuids[i], "datatype": i} for i in range(n)]

#     def insert(obj:dict, parent_webid: str):

#         #extract base from obj and insert
#         #
#         pass

#     # def inserts():
#         # with engine.begin() as conn:

#             # stmt = insert(basetable).values(bases)
#             # stmt2 = insert(treetable).values(
#                 [
#                     {"parent": uuids[0], "child": uuids[0], "depth": 0},
#                     {"parent": uuids[1], "child": uuids[1], "depth": 0},
#                     {"parent": uuids[0], "child": uuids[1], "depth": 1},
#                     {"parent": uuids[2], "child": uuids[2], "depth": 0},
#                     {"parent": uuids[0], "child": uuids[2], "depth": 1},
#                     {"parent": uuids[3], "child": uuids[3], "depth": 0},
#                     {"parent": uuids[1], "child": uuids[3], "depth": 1},
#                     {"parent": uuids[0], "child": uuids[3], "depth": 2},
#                     {"parent": uuids[4], "child": uuids[4], "depth": 0},
#                     {"parent": uuids[1], "child": uuids[4], "depth": 1},
#                     {"parent": uuids[0], "child": uuids[4], "depth": 2},
#                     {"parent": uuids[5], "child": uuids[5], "depth": 0},
#                     {"parent": uuids[2], "child": uuids[5], "depth": 1},
#                     {"parent": uuids[0], "child": uuids[5], "depth": 2},
#                 ]
#             )
#             # stmt2 = insert(nodetable).values(nodes)
#             # conn.execute(stmt2)

#             # conn.execute(stmt)
#             # conn.execute(stmt2)
#             # conn.commit()


# # insert()

# # # def test_one():
# # #     # with engine.connect() as conn:
# # #     with engine.begin() as conn:
# # #         stmt = select(basetable)
# # #         rows = conn.execute(stmt)
# # #         assert len(rows.fetchall()) == n


# # def test_read_tree():

# #     with engine.begin() as conn:
# #         query = select_descendants(uuids[0])
# #         res = conn.execute(query)
# #         assert len(res.fetchall()) == n - 1
# #         # for r in res:
# #         # print(r)

# #         query = select_descendants(uuids[1])
# #         res = conn.execute(query)
# #         assert len(res.fetchall()) == 2
# #         # for r in res:
# #         # print(r)

# #         query = select_descendants(uuids[4])
# #         res = conn.execute(query)
# #         assert len(res.fetchall()) == 0
# #         # for r in res:
# #         # print(r)


# # def test_read_children():

# #     with engine.begin() as conn:
# #         query = select_children(uuids[0])
# #         res = conn.execute(query)
# #         assert len(res.fetchall()) == 2
# #         # for r in res:
# #         # print(r)


# # def test_insert_node():

# #     uuids2 = [str(uuid1()) for _ in range(n)]

# #     bases = [{"name": f"NAMENODE{i}", "webid": uuids2[i]} for i in range(4)]
# #     nodes = [{"webid": uuids2[i], "template": f"TEMP{i}"} for i in range(4)]

# #     with engine.begin() as conn:
# #         stmt = insert(basetable).values(bases)
# #         stmt2 = insert(nodetable).values(nodes)
# #         conn.execute(stmt)
# #         conn.execute(stmt2)
# #         conn.commit()

# #     def read_node(id):
# #         return (
# #             select(basetable, nodetable)
# #             .join(nodetable, basetable.c.webid == nodetable.c.webid)
# #             .where(nodetable.c.webid == id)
# #         )

# #     with engine.begin() as conn:
# #         query = read_node(uuids2[0])
# #         res = conn.execute(query)
# #         # assert len(res.fetchall()) == 2
# #         for r in res:
# #             print(r._asdict())


# # def test_insert_item():
# #     pass


# # def test_read_item():
# #     pass
