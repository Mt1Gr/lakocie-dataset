from .database.db import init_db, engine
from sqlmodel import Session


def main():
    init_db()
    print("Database initialized")
