"""
The program is very simple and can do only what is required in the task.
I created the program using the example code snippet (ETL().source(source_args).sink(sink_args).run()),
and wanted to make it work with it.

The code is very lame and it could be done much better with composition.
However, it does the job.
TODO: return and optimize the code

The source has two options(<path-to-file> or file name) or ('streaming').
The sink also has two options ('console') or ('postgres'). The sink also takes the return values from Source as *args.
"""


import json
import string
import random
from faker import Faker
import psycopg2


class ETL:
    def __init__(self):
        self.source = Source
        self.sink = Sink

class Source:
    def __init__(self, *args):
        self._fake = Faker('en_US')
        self.args = args
        self.sink = Sink
    def rtrn(self):
        if ".json" in self.args[0]:
            with open(self.args[0]) as json_file:
                a = json.load(json_file)
                if type(a) is dict: #If it is a dictionary eg.({key:value, value:value, ts:value}), returns it directly
                    yield a
                else:              #If it is a list of dictionaries eg.([{key:value, value:value, ts:value}]) - Iterate over it
                    for i in a:
                        yield i


        elif 'streaming' == self.args[0]:
            for _ in range(random.randint(10, 25)):
                my_dict = {'key': random.choice(string.ascii_uppercase) + str(random.randint(100, 200)),
                            'value': str(round(random.randint(10, 40) / random.uniform(0.1, 1), 1)),
                            'ts': str(self._fake.date_time())}
                yield my_dict
        else:
            print("You should either enter a valid directory or the word 'streaming'. Try again.")


class Sink:
    def __init__(self, *args):
        self._connection = psycopg2.connect(host='localhost',
                                            port='8000',
                                            database='test_db',
                                            user='postgres',
                                            password='940325')
        self._cursor = self._connection.cursor()
        self.args = args



    def run(self):
        if 'console' == self.args[0]:
            for line in self.args[1]:
                print(line)
        elif 'postgres' == self.args[0]:

            self._cursor.execute("SELECT version();")
            create_table_query = '''CREATE TABLE IF NOT EXISTS test_table           
                      (KEY TEXT NOT NULL,
                      VALUE TEXT NOT NULL,
                      TimeStamp TEXT NOT NULL); '''
            self._cursor.execute(create_table_query)
#           ^ Creates the table if it doesn't exist with TEXT columns for simplicity
            for line in self.args[1]:
                insert_query = "INSERT INTO test_table (key, value, timestamp) VALUES ('{}', '{}', '{}')" \
                    .format(line['key'], line['value'], line['ts'])
                self._cursor.execute(insert_query)
                self._connection.commit()
#           ^ Insert the values in the created table


se = Source("streaming") #or "<path-to-file>
ETL().source(se).sink("postgres", se.rtrn()).run()
                        #^ OR "streaming"