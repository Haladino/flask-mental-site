from util import read_file
from config import DATABASE_FILES
from flask import json

class new_database():

    def __init__(self):
        self.LOADED_FILES = {}
        self.NUMBER_OF_FILES_LOADED = 0
        self.LOADED_FILE_NAMES = []
        self.HISTORY = []
        

    def load(self, filename=None):
        if filename and filename.find('.json') < 1:
            print("The file your're trying to load is not JSON")
        
        elif filename:
            key = filename.replace('.json' , '_data')

            self.LOADED_FILES[key] = read_file('database/' + filename, json)
            self.NUMBER_OF_FILES_LOADED += 1
            self.LOADED_FILE_NAMES.append(filename)            
        else:
            for databasefile in DATABASE_FILES:
                key = databasefile.replace('.json' , '_data')

                self.LOADED_FILES[key] = read_file('database/' + databasefile, json)
                self.NUMBER_OF_FILES_LOADED += 1
                self.LOADED_FILE_NAMES.append(databasefile)


    def reload_database(self):
        self.reset_database()
        if len(self.HISTORY) > 0:
            for filename in self.HISTORY:
                self.load(filename)
        else:
            self.load()


    def reset_database(self):
        self.LOADED_FILES = {}
        self.NUMBER_OF_FILES_LOADED = 0
        self.HISTORY = self.get_loaded_files_name()
        self.LOADED_FILE_NAMES = []


    def get_loaded_files_json(self):
        return self.LOADED_FILES


    def get_number_of_loaded_files(self):
        return self.NUMBER_OF_FILES_LOADED

    
    def get_loaded_files_name(self):
        return self.LOADED_FILE_NAMES