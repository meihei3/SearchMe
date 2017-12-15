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
import matplotlib.pyplot as plt
from matplotlib import matplotlib_fname, font_manager

raw_database_file = "History.db"
database_file = "my_history.db"


def setup_history_database():
    # copy safari history database to working directory
    # for safety work
    check_call(["cp", path.expanduser("~/Library/Safari/") + raw_database_file, "./"])


def setup_family_font():
    # copy ipaexg.ttf to matplotlib
    # check_call(["cp", "./font/ipaexg.ttf", path.dirname(matplotlib_fname()) + "/fonts/ttf/"])

    # set matplotlibrc
    if path.isfile(path.expanduser("~/.matplotlib/matplotlibrc")):
        print("This program override '~/.matplotlib/matplotlibrc'.")
        if not input("Do you permit us to override it? (y or n) >> ") == "y":
            # kill this program
            raise PermissionError("hoge hoge hoge")

    # call cp command
    check_call(["cp", "./font/matplotlibrc", path.expanduser("~/.matplotlib/matplotlibrc")])


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


def add_edges(graph, edge_list=None):
    if edge_list is None:
        contents = []
    for node0, node1 in edge_list:
        if graph.has_edge(node0, node1):
            graph.edge[node0][node1]["weight"] += 1
        else:
            graph.add_edge(node0, node1, {"weight": 1})


def create_graph(contents=None):
    if contents is None:
        contents = []
    # set Graph (not Directed Graph)
    G = nx.Graph()
    for content in contents:
        G.add_nodes_from(content)
        add_edges(G, get_edge_list(content))
    return G


def main():
    setup_history_database()
    r = get_prepared_data()
    g = create_graph([get_noun(i) for i in [t[2] for t in r][:10]])
    print(g.nodes())

    setup_family_font()
    plt.figure(figsize=(15,15))
    pos = nx.spring_layout(g)
    nx.draw_networkx(g, pos, font_family="IPAexGothic")

    # nx.draw_networkx_nodes(g, pos, node_color="b", alpha=0.6)
    # nx.draw_networkx_labels(g, pos, fontsize=14, font_family="IPAexGothic", font_weight="bold")

    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    main()
