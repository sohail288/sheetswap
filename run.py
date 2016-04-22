"""
    Imports App and Runs it
"""


from app import create_app

smtrade = create_app()
manager = Manager(app)


if __name__ == "__main__":
