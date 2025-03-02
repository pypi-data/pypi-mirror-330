foo = "foo"


class Welcome:
    def __init__(self, username):
        self.username = username

    def run(self):
        print(f"welcome {self.username}")
