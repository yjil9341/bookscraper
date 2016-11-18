from pymongo import Connection

if __name__ == '__main__':

    conn = Connection()
    db = conn.test_database
    people = db.people
    people.insert({'name':'Mike','food':'cheese'})

    peoples = people.find()
    print "printing result"
    for people in peoples:
        print people
