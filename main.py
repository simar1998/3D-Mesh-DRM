from STLReader import STLReader
##Code that calculates Hausdorff distance and the Root Mean Square Deviation between two stl files

class MainClass:
    def __init__(self):
        self.message = "Starting python stl comparision application"


    def main(self):
        print(self.message)
        reader = STLReader("file1.stl", "file2.stl")
        coords1, coords2 = reader.read_stl_files()


if __name__ == "__main__":
    main_class = MainClass()
    main_class.main()
