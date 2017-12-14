# coding: utf-8

# use for shell scripts
from subprocess import check_call
from os import path

# use for database
from sqlite3 import connect

# use for janome methods
from janome.tokenizer import Tokenizer

# use for graph
import networkx as nx
from itertools import combinations

raw_database_file = "History.db"
database_file = "my_history.db"


def setup_history_database():
    # copy safari history database to working directory
    # for safety work
    check_call(["cp", path.expanduser("~/Library/Safari/") + raw_database_file, "./"])


def open_sql(filename, f):
    # open (or create) database
    connector = connect(filename)
    cursor = connector.cursor()

    # execute sql commands
    result = f(cursor)

    if result is None:
        # updated this database if return value of f() is None
        connector.commit()
    # else: got data from this database if return value of f() is not None

    cursor.close()
    connector.close()

    # result value is None or data
    return result


def execute_sql_command(command=""):
    def f(cursor):
        cursor.execute(command)
        # get selected data if this command use select
        if command[:6] == "select":
            return cursor.fetchall()
        return None
    return f


def get_prepared_data():
    cmd = "select visit_time,title from history_visits where title != '' group by title order by id"
    result = open_sql(raw_database_file, execute_sql_command(cmd))
    # add id
    # Maybe this is not necessary....
    for i in range(len(result)):
        result[i] = (i, result[i][0], result[i][1])
    return result


def get_noun(content=""):
    # set tokenizer
    t = Tokenizer()
    # return nouns in content
    return [token.surface for token in t.tokenize(content) if token.part_of_speech.split(',')[0] == '名詞']


def get_edge_list(contents=None):
    if contents is None:
        contents = []
    return list(combinations(contents, 2))


def crate_graph(contents=None):
    if contents is None:
        contents = []
    # set Graph (not Directed Graph)
    G = nx.Graph()
    for content in contents:
        G.add_nodes_from(content)
        G.add_edges_from(get_edge_list(content))
    return G


def main():
    setup_history_database()
    r = get_prepared_data()
    for t in r:
        s = get_noun(t[2])
        print(s)


if __name__ == '__main__':
    main()
