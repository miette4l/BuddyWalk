import datetime
# datetime library will be used for comparing journey start times
# we are going to use GM time across the board and constrain location, so there will be no timezone errors
# as such, datetime objects are "naive" as opposed to "aware"
# we also need a type for working with locations, which needs to work with the Google API

"""
User:
journey:
route:
"""


class User:
    # Instantiated when a user logs in.
    # user would log in, with a username and password.
    # integrate with SQL database to make and retrieve user accounts and details.
    # we imagine authentication is done separately but have authentication column in db with all set to True.

    def __init__(self, username: str):
        self.username = username
        self.online = True
        self.searching = False
        # user object is instantiated == user is online/has logged in.

    def search(self, start, end, time):
        # run this when the user clicks 'find buddy', to add the following instance attributes
        # prepares attributes for the find_buddy function, from our inputs
            self.searching = True
            self.start = start
            self.end = end
            self.time = time

    def find_buddy(self):
        """
        :return: another User
        """
        # find the buddy. this could be a big function, so maybe put logic in another file as a module and import?
        for user in Users:
            if not user == self:
                if abs(user.time - self.time) <= datetime.timedelta(0, 600):
                    self.buddy = user
                    user.buddy = self
        """
        if self.start and self.end are sufficiently close to buddy.start and buddy.end, it's a match
        return the buddy's phone number and a point to meet at
        if there are multiple people, make a group
        """

holly = User("miette4l")
print("Username:", holly.username)
print("Online status:", holly.online)
print("Searching status:", holly.searching)

location1 = "SE42RW"
location2 = "SE87RN"
time = datetime.datetime(2021, 12, 8, 14, 59, 11)

holly.search(location1, location2, time)
print("Searching status:", holly.searching)
print("Starting location:", holly.start)
print("Ending location:", holly.end)
print("Starting time:", holly.time)

phoebe = User("meowphoebs")
print("Username:", phoebe.username)
print("Online status:", phoebe.online)
print("Searching status:", phoebe.searching)

location1 = "SE42RW"
location2 = "SE87RN"
time = datetime.datetime(2021, 12, 8, 14, 49, 11)

phoebe.search(location1, location2, time)
print("Searching status:", phoebe.searching)
print("Starting location:", phoebe.start)
print("Ending location:", phoebe.end)
print("Starting time:", phoebe.time)

Users = [holly, phoebe]

holly.find_buddy()
print("{}'s buddy:".format(holly.username), holly.buddy.username)
print("{}'s buddy:".format(phoebe.username), phoebe.buddy.username)


# Mock a container full of users as a nested dictionary
# {user_id:
#   {user_id.online: Bool, user_id.searching: Bool, },
#   user_id_2: {} etc
#   },

# Users = {
#     {}
# }