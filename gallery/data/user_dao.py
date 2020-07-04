class UserDAO:
    def get_users(self):
        raise Exception("Must be implemented")

    def get_single_user(self):
        raise Exception("Must be implemented")

    def delete_user(self, username):
        raise Exception("Must be implemented")

    def edit_user(self, username):
        raise Exception("Must be implemented")

    def create_user(self, username):
        raise Exception("Must be implemented")
