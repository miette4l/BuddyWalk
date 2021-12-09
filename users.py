import datetime


class User:
    # Instantiated when a user logs in.
    # user would log in, with a username and password.
    # integrate with SQL database to make and retrieve user accounts and details.
    # we imagine authentication is done separately but have authentication column in db with all set to True.

    def __init__(self, username: str):
        """
        user object is instantiated == user is online/has logged in
        """
        self.username = username
        self.online = True
        self.searching = False

    def search(self, current_loc: str, destination: str, ToD: str):
        """
        prepare attributes for the find_buddy function from user inputs
        """
        self.searching = True
        self.current_loc = current_loc
        self.destination = destination
        if type(ToD) == str:
            self.ToD = datetime.datetime.fromisoformat(ToD)
        elif type(ToD) == datetime.datetime:
            self.ToD = ToD
        else:
            raise TypeError("Invalid input type for ToD")

    def find_buddy(self, users: list):
        """
        Finds the buddy or buddies?
        """
        # THIS IS CURRENTLY INCOMPLETE as cannot deal with multiple results
        for user in users:
            if not user == self:
                if abs(user.ToD - self.ToD) <= datetime.timedelta(0, 600):
                    self.buddy = user
                    user.buddy = self
        return self.buddy


class SearchingUsers:

    @staticmethod
    def get_searching_users():
        """
        return: a list of searching users for the find_buddy function
        (mocked for now)
        """
        holly = User("miette4l")
        current_loc = "SE42RW"
        destination = "SE87RN"
        ToD = datetime.datetime(2021, 12, 8, 14, 59, 11)
        holly.search(current_loc, destination, ToD)

        phoebe = User("meowphoebs")
        current_loc = "SE42RW"
        destination = "SE87RN"
        ToD = datetime.datetime(2021, 12, 8, 14, 49, 11)
        phoebe.search(current_loc, destination, ToD)

        users = [holly, phoebe]

        return users


def return_buddy(data: dict):
    user = User(data['username'])
    # what if this user becomes another user's buddy?
    # then no need to search...
    user.search(data['CurrentLoc'], data['Destination'], data['ToD'])
    users = SearchingUsers.get_searching_users()
    buddy = user.find_buddy(users)
    message = "Your buddy is: {}".format(buddy.username)
    return message


# Test Cases #
#
# holly = User("miette4l")
# print("Username:", holly.username)
# print("Online status:", holly.online)
# print("Searching status:", holly.searching)
#
# location1 = "SE42RW"
# location2 = "SE87RN"
# time = datetime.datetime(2021, 12, 8, 14, 59, 11)
#
# holly.search(location1, location2, time)
# print("Searching status:", holly.searching)
# print("Starting location:", holly.start)
# print("Ending location:", holly.end)
# print("Starting time:", holly.time)
#
# phoebe = User("meowphoebs")
# print("Username:", phoebe.username)
# print("Online status:", phoebe.online)
# print("Searching status:", phoebe.searching)
#
# location1 = "SE42RW"
# location2 = "SE87RN"
# time = datetime.datetime(2021, 12, 8, 14, 49, 11)
#
# phoebe.search(location1, location2, time)
# print("Searching status:", phoebe.searching)
# print("Starting location:", phoebe.start)
# print("Ending location:", phoebe.end)
# print("Starting time:", phoebe.time)
#
# Users = [holly, phoebe]
#
# holly.find_buddy()
# print("{}'s buddy:".format(holly.username), holly.buddy.username)
# print("{}'s buddy:".format(phoebe.username), phoebe.buddy.username)
