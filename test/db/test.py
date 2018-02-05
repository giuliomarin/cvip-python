#!/usr/bin/python

import datetime
import string
import MySQLdb
from nltk import word_tokenize
from PyDictionary import PyDictionary

WORDS_INTRO = ["i have", "i feel"]
WORDS_DISCARD = ["i", "have", "feel", "with", "it", "my", "in", "is", "a"]
WORDS_NEGATIVE = ['dont', 'no']


class DB:
    def __init__(self, host, username, password, database):
        self.db = None
        self.cursor = None
        self.connect(host, username, password, database)

    def connect(self, host, username, password, database):
        try:
            # Open database connection
            self.db = MySQLdb.connect(host, username, password, database)

            # prepare a cursor object using cursor() method
            self.cursor = self.db.cursor()

        except Exception as e:
            print(e)
            exit(1)
        print '\nConnected to database'

    def execute(self, sql):
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit changes in the database
            self.db.commit()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
            self.db.rollback()

    def add_session(self, patient_id, staff_id, conversation):
        sql = "INSERT INTO session (date_time, patient_id, staff_id, conversation) VALUES ('%s', %d, %d, '%s')" % (datetime.datetime.now(), patient_id, staff_id, conversation)
        self.execute(sql)
        print 'Add session'

    def get_conversation(self, session_id):
        sql = "SELECT conversation FROM session WHERE session.id = %d" % session_id
        self.execute(sql)
        val = self.cursor.fetchone()
        return val[0] if val else val

    def add_keywords(self, session_id, keywords):
        sql = "UPDATE session SET keywords = '%s' WHERE id = '%d'" % ('|'.join(keywords), session_id)
        print sql
        self.execute(sql)
        print 'Add session'

    def add_relationship(self, patient_1, patient_2, type):
        sql_fill = """
        INSERT INTO relationship (patient_1, patient_2, type)
            SELECT * FROM (SELECT '%d', '%d', '%s') AS tmp
            WHERE NOT EXISTS (SELECT patient_1, patient_2 FROM relationship WHERE (patient_1 = '%d' AND patient_2 = '%d')) LIMIT 1;
        """
        sql = sql_fill % (patient_1, patient_2, type, patient_1, patient_2)
        self.execute(sql)
        print 'Add relationship: %d is %s of %d' % (patient_1, type, patient_2)

        # Get gender patient 2
        self.execute("SELECT gender from patient p WHERE p.id = '%d'" % patient_2)
        gender_2 = self.cursor.fetchone()[0]

        # Add inverse
        if type == 'husband':
            type_inv = 'wife'
        elif type == 'wife':
            type_inv = 'husband'
        elif type == 'partner':
            type_inv = 'partner'
        elif type == 'brother':
            if gender_2 == 'F':
                type_inv = 'sister'
            else:
                type_inv = 'brother'
        elif type == 'sister':
            if gender_2 == 'F':
                type_inv = 'sister'
            else:
                type_inv = 'brother'
        elif type == 'son' or type == 'daughter':
            if gender_2 == 'F':
                type_inv = 'mother'
            else:
                type_inv = 'father'
        elif type == 'mother':
            if gender_2 == 'F':
                type_inv = 'daughter'
            else:
                type_inv = 'son'
        elif type == 'father':
            if gender_2 == 'F':
                type_inv = 'daughter'
            else:
                type_inv = 'son'
        else:
            return
        sql = sql_fill % (patient_2, patient_1, type_inv, patient_2, patient_1)
        self.execute(sql)
        print 'Add inverse relationship: %d is %s of %d' % (patient_2, type_inv, patient_1)

    def parse_conversation(self, text):
        text = text.translate(None, string.punctuation).lower()
        tokens = word_tokenize(text)
        keywords = []
        for t in tokens:
            if t in WORDS_DISCARD:
                continue
            if t in WORDS_NEGATIVE:
                keywords.append("!")
                continue
            keywords.append(t)
        return keywords

    def info(self):

        # Staff
        print "\nList of staff"
        sql = "SELECT * FROM staff"
        self.execute(sql)
        results = self.cursor.fetchall()
        print tuple([c[0] for c in self.cursor.description])
        for row in results:
            print row

        # Patients
        print "\nList of patients"
        sql = "SELECT * FROM patient"
        self.execute(sql)
        results = self.cursor.fetchall()
        print tuple([c[0] for c in self.cursor.description])
        for row in results:
            print row

        # Relationships
        print "\nList of relationships"
        sql = "SELECT p1.first_name first_name_1, p2.first_name first_name_2, r.type FROM patient p1 JOIN patient p2 JOIN relationship r ON (p1.id = r.patient_1 AND p2.id = r.patient_2)"
        self.execute(sql)
        results = self.cursor.fetchall()
        print tuple([c[0] for c in self.cursor.description])
        for row in results:
            print row

        # History
        print "\nList of history"
        sql = "SELECT session.date_time, p.first_name first_name_p, s.first_name first_name_s, session.conversation FROM patient p JOIN staff s JOIN session ON (session.patient_id = p.id AND session.staff_id = s.id)"
        self.execute(sql)
        results = self.cursor.fetchall()
        print tuple([c[0] for c in self.cursor.description])
        for row in results:
            print row

    def __del__(self):
        # disconnect from server
        self.db.close()
        print '\nDisconnected from database'


def test_dictionary():
    dictionary = PyDictionary()
    print (dictionary.synonym("ache"))
    print (dictionary.synonym("pain"))
    print (dictionary.synonym("bloated"))


if __name__ == "__main__":

    # Test dictionary
    # test_dictionary()

    # Test query database
    db = DB("localhost", "g", "0", "test")
    # db.info()
    # keywords = parse_conversation(db.get_conversation(1))
    for txt in open('/Data/10_smd/documents/text.txt', 'r').readlines():
        txt = txt.strip()
        key = db.parse_conversation(txt)
        print txt, key
    # db.add_keywords(1, keywords)