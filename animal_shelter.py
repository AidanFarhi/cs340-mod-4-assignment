from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # load the environment variables from the .env file


class AnimalShelter:
    """
    Class to perform CRUD operations for the Animal Shelter database.
    """

    def __init__(
        self,
        user: str = getenv("USERNAME"),
        pwd: str = getenv("PASSWORD"),
        host: str = getenv("HOST"),
        port: int = int(getenv("PORT")),
        db: str = getenv("DB"),
        collection: str = getenv("COLLECTION"),
    ):
        """
        Initialize an instance of AnimalShelter.
        If no values are supplied, default values will be
        read from the environment variables.
        """

        # initialize all of the member fields from the __init__ args.
        self.client = MongoClient(f"mongodb://{user}:{pwd}@{host}:{port}")
        self.database = self.client[f"{db}"]
        self.collection = self.database[f"{collection}"]

    def _validate_args(self, args: dict) -> bool:
        """
        Validates whether the arguments passed in are valid or not.
        """
        return args is None or not isinstance(args, dict) or len(args) == 0

    def create(self, data: dict) -> bool:
        """
        Creates an object in the database.
        """
        # check if data is a non-null and non-empty dictionary
        if data is not None and isinstance(data, dict) and len(data) > 0:
            try:
                # insert the data into the database
                self.collection.insert_one(data)
            except Exception as e:
                # raise an exception if any error occurs
                print("error while inserting data")
                raise e
        else:
            # return false if the data is not valid
            print("data must be a non-empty dict")
            return False
        # this will be returned if the operation was succesful
        return True

    def find(self, query: dict) -> list:
        """
        Runs a query against the database and returns a list of results.
        """
        # check if the query is a non-null and non-empty dictionary
        if self._validate_args(query):
            # if the above validation is true, return an empty list
            return []
        try:
            # if the query is valid, return a list of results
            return self.collection.find(query).to_list()
        except Exception as e:
            # if the operation was not succesfull, raise an exception
            print("error while searching the database")
            raise e

    def update(self, query: dict, update: dict) -> int:
        """
        Queries the database, updates found records, and returns number of records affected.
        """
        # check if the query and update args are valid
        if self._validate_args(query) and self._validate_args(update):
            return 0
        try:
            # use the update_many method to update the records and return the number affected
            return self.collection.update_many(query, update).modified_count
        except Exception as e:
            # if the operation was not succesfull, raise an exception
            print("error while trying to update")
            raise e

    def delete(self, query: dict) -> int:
        """
        Queries the database, deleted found records, and returns number of records affected.
        """
        # check if the query args is valid
        if self._validate_args(query):
            return 0
        try:
            # use the delete_many method to update the records and return the number affected
            return self.collection.delete_many(query).deleted_count
        except Exception as e:
            print("error while searching the database")
            raise e
