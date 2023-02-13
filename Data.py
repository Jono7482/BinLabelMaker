from sqlitedict import SqliteDict
import saved

# DB = SqliteDict('data.sqlite3', autocommit=True, journal_mode='OFF')


def save(key, sub, value, cache_file="data.sqlite3"):
    print('Save Ran')
    print(f"save key = {key} save sub = {sub} save value = {value}")
    db = SqliteDict('data.sqlite3', autocommit=True, journal_mode='OFF')
    try:
        with db as mydict:
            mydict[key][sub] = {value}  # Using dict[key] to store
            db.commit()  # Need to commit() to actually flush the data
            db.close()

    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)


def load(key, cache_file="data.sqlite3"):
    db = SqliteDict('data.sqlite3', autocommit=True, journal_mode='OFF')
    try:
        with db as mydict:
            value = mydict[key]
            mydict.commit()
            db.close()
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


def load_value(key, sub, cache_file="data.sqlite3"):
    db = SqliteDict('data.sqlite3', autocommit=True, journal_mode='OFF')
    try:
        with db as mydict:
            value = mydict[key][sub]
            mydict.commit()
            db.close()
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


def test():
    print('Testing start')
    print(f'saved.py test1 = {saved.test1}')
    saved.test1 = 2
    print('saved.test1 changed')
    print(f'saved.test1 = {saved.test1}')
    print('Testing End')


def create_default():
    db = SqliteDict('data.sqlite3', autocommit=True, journal_mode='OFF')
    print('Default ran')
    try:
        with db as mydict:
            default = {'a_start': '02',
                       'a_end': '04',
                       's_start': 'C',
                       's_end': 'D',
                       'b_start': '01',
                       'b_end': '23',
                       'p_start': 'A',
                       'p_end': 'A'}
            mydict["<DEFAULT>"] = default
            mydict.commit()
            db.close()
    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)

