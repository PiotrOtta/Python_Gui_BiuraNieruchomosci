from options import Options


def main():
    while True:
        x = input("Type 1 to scan, 2 to join files, 4 to exit:")
        if x == str(1):
            key = input("Do you want to get only changed values? y/n (n): ")
            if key == "y":
                file = input("Enter file to compare: ")
                Options.generateData(file)
            else:
                Options.generateData()
        elif x == str(2):
            f1 = input("Enter first file to join: ")
            f2 = input("Enter second file to join: ")
            key = input("Do you want to remove files after joining? y/n (n): ")
            if key == "y":
                Options.joinFiles(f1, f2, True)
            else:
                Options.joinFiles(f1, f2)
        elif x == str(4):
            break
        else:
            pass


if __name__ == '__main__':
    main()
