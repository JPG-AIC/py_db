import pickle

DEBUG = True
LOG_ACTIONS = True
LOG_WARNINGS = True

STEP = 1

'''

TODO:
    Fix Debug Stuff
    Create Querying

'''

class Serializable(object):

    def __init__(self, filename):
        """filename is its own string i.e. to make a file: 'test.p', input 'test'"""
        self.filename = filename + ".p"

    def serialize(self, stuff_to_dump):
        pickle.dump(stuff_to_dump, open(self.filename, "wb"))

    def unserialize(self):
        return pickle.load(open(self.filename, "rb"))

    def open_logfile(self):
        return open('logfile.txt', 'w')

class Database(Serializable):

    '''
    
        Database Structure will be as follows:
            
            [col0, row0][col1, row0][col2, row0]
            [col0, row1][col1, row1][col2, row1]
            [...]          [...]           [...]

    '''
    
    def __init__(self, filename, columns):
        super(Database, self).__init__(filename)
        self.def_column = []
        self.rows = []
        for n in columns:
            self.def_column.append(Column(n[0], n[1]))

    def add_row(self, row):
        global DEBUG
        global STEP
        if DEBUG:
            self.log_file = self.open_logfile()
            self.log_file.write("Step {0} - Entering Add Row with argument: {1}".format(STEP, row))
            self.log_file.close()
        row_added = False
        idx = 0
        if len(row) != len(self.def_column):
            raise AttributeError("Rows input do not equal the rows in the table")
        else:
            for n in self.def_column:
                if self.def_column[idx].check_type(row[idx]) and not row_added:
                    self.rows.append(row)
                    row_added = True
                elif not self.def_column[idx].check_type(row[idx]) and not row_added:
                    raise TypeError("Invalid type in column {0} of row to be added".format(idx))
                elif row_added:
                    break
                idx += 1

    def save(self):
        self.serialize(self.database)
        
    def load(self):
        return self.unserialize()
    

class Column(object):

    def __init__(self, ident, arg_type):
        self.arg_type = arg_type
        self.identifier = ident

    def check_type(self, applicant_object):
        if type(applicant_object) == self.arg_type:
            return True
        else:
            return False
        
        
class Row(object):

    def __init__(self, ident):
        self.contents = []
        self.identifier = ident

    def get_contents(self):
        return self.contents


    
class CustomTable(Serializable):
    '''Example of Inheriting the Serializable Class'''
    '''
    Maybe have something like: {column_identifier: [value_in_row1, value_in_row2, ..., value_in_row_n], column_identifier2: [...]}
    '''

    def __init__(self, filename, nums):
        super(CustomTable, self).__init__(filename)
        self.nums = nums
        self.table = {}

    def add_column(self, column_identifier):
        self.table.update({column_identifier: []})

    def append_row_to_column(self, column_identifier, value_at_next_row):
        self.table[column_identifier].append(value_at_next_row)

    def populate_column_row(self, column_identifier, row_num, populate_data):
        if row_num >= len(self.table[column_identifier]):
            raise IndexError("Index out of bounds in Database.table, column_identifier = {0}".format(column_identifier))
        else:
            self.table[column_identifier][row_num] = populate_data 

    def __repr__(self):
        for n in self.table:
            
            print n
        
    def save(self):
        self.serialize(self.nums)

    def load(self):
        return self.unserialize()

if __name__ == "__main__":
    print "Creating Database"
    a = Database("test", ['name', 'age', 'type'])
    print "Populating Database"
    a.add_row(['jordan', 19, 'water'])
    print "Printing Database contents"
    a.database
    print "Saving database a"
    a.save()
    print "Loading database a"
    a.load()
