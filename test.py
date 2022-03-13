from multiprocessing.sharedctypes import Value


def readBigString(file_name):
    try :
        dataFile = open(file_name, "r")
        contents = dataFile.read()
        dataFile.close()
        print (contents)
    except IOError:
        print("Error: file not found.")

def readLoL(file_name):
    try :
        dataFile = open(file_name, "r")
        contents = dataFile.readlines()
        print (contents)
        dataFile.close()
    except IOError:
        print("Error: file not found.")

def readingLBL(file_name):
    try:
        with open(file_name, "r",) as file:
            line_count = 0
            data = [] #store the data
            title = file.readline().rstrip() #gets title
            source_label = file.readline().rstrip()#gets source_label
            for line in file:
                line_count += 1
                line.split()
                line.rstrip()
                data.append(line)
        return title, source_label, data
    except IOError:
        print("Error: file not found.")

def clean_list(dlist):
    list_dict = {} #create empty dict to fill in 
    for i in dlist: 
            key, value = i.split(",") #split the singl;e string in the list containing the key and value
            if key != None and value != None: #validating neither the key nor value are empty
                key, value = key.strip(), value.strip() #clean up the strings from white space and new lines
                try:
                    value = float(value)
                    list_dict.update({key: value}) #add to the dictionary
                except ValueError:
                    print("Value Error: Key and Value not added")
            else:
                raise ValueError

    return list_dict

def main():
    readBigString("netball_2018.txt")
    print()
    readLoL("netball_2018.txt")
    print()
    readBigString("test.txt")
    print()
    title, label, data_list = readingLBL("netball_2018.txt")
    print (clean_list(data_list)) 
    clean_list([1,2,3,4,5,6,7])

if __name__ == "__main__":
    main()