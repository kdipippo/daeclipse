import pathlib
if __name__ == "__main__":
    print(pathlib.Path(__file__).parent.absolute())
    print(pathlib.Path(__file__).parent.parent.parent.absolute())