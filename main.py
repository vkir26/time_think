from session import run
from auth.my_account import identification


def main() -> None:
    if identification() is not None:
        run()


if __name__ == "__main__":
    main()
