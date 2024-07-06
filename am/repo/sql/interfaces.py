""""""

from typing import Protocol

from sqlalchemy import Column, Table


class ClosureTable(Protocol):

    table: Table
    parent: Column
    child: Column
    depth: Column


class LabelTable(Protocol):

    table: Table
    webid: Column
