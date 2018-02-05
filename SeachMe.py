# coding: utf-8

# use for shell scripts
from subprocess import check_call
from os import path

# use for database
from sqlite3 import connect

# use for janome methods
from janome.tokenizer import Tokenizer

# use for word view
from wordcloud import WordCloud

# use for print percent of 'for loop'
from tqdm import tqdm

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
        # if not input("Do you permit us to override it? (y or n) >> ") == "y":
            # kill this program
            # raise PermissionError("hoge hoge hoge")

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


def get_noun_list(data, size=50):
    if data is None:
        raise ValueError
    datalist = [t[2] for t in data]
    if len(datalist) < size:
        size = len(datalist)
    print("Morphological analysis...")
    return [get_noun(i) for i in tqdm(datalist[len(datalist)-size:])]


def crean_up_text(text):
    return text.replace('- ', '').replace('| ', '')


def extends_list(list_of_list):
    ls = []
    for l in list_of_list:
        ls += l
    return ls


def create_wordcloud(text, filepath="./wordcloud.png"):
    wordcloud = WordCloud(background_color="white",
                          font_path="font/ipaexg.ttf",
                          width=800,height=600).generate(text)
    wordcloud.to_file(filepath)


def main():
    # setup_history_database()
    r = get_prepared_data()
    text = crean_up_text(" ".join(extends_list(get_noun_list(r, size=300))))
    create_wordcloud(text)


if __name__ == '__main__':
    main()
