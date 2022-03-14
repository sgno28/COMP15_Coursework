
"""Draw a sankey diagram using data from a given input file.
"""
import sys
from ezgraphics import GraphicsWindow

WIDTH = 1000        # Width of the window in pixels
HEIGHT = 700        # Height of the window in pixels
GAP = 10            # Gap between disagram arrows in pixels
COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
(245,	130,	48),	(145,	30, 180), (70, 240,	240),	(240, 50, 230),
(210,	245,	60),	(250,	190, 212), (0, 128,	128),	(220, 190, 255),
(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195),
(128,	128,	0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]


def read_file(file_name):
    """Opens and reads the file. Returns the title, left-hand axis label and 
    the data values in the file.

    Args:
        file_name (str): file containing the data.

    Raises:
        FileNotFoundError: If file not found or is not readable, 
                            this exception is raised

    Returns:
        str: diagram title
        str: left-hand axis label
        list: Each element contains one line of data from the file
    """
    try:
        with open(file_name, "r",) as file:
            data = [] #store the data
            title = file.readline().rstrip() #gets title
            source_label = file.readline().rstrip()#gets source_label
            print("Title: ", title,"label: ", source_label)
            for line in file:
                line.split() #split up each line containing data into seperate strings
                line.rstrip() #remove whitespace
                data.append(line) #add to a list which will hold the data and return it
        return title, source_label, data
    except IOError:
        print("Error: file not found.")
        raise FileNotFoundError

def set_up_graph(title):
    """Creates a window and canvas. Displays the title, left-hand axis label.
    Returns a reference to the window. 

    Args:
        title (str): title for the window
        
    Returns:
        GraphicsWindow: reference to the window
    """
    win = GraphicsWindow(WIDTH, HEIGHT)
    win.setTitle(title)
    return win

def parse_value (str, line_number) :
    """Parses and returns a floating point value from a string, cleaning required characters (e.g. white spaces).
       
    Args:
        str: string from which the value must be read
        line_number: line in the file, required in case errors neet to be notified
        
    Raises: 
        ValueError: raised if the string cannot be read as a float, datailing content and line number    
    Returns:
        float: The number read        
    """
    pass

def process_data(data_list) :
    """Returns a dictionary produced by processing the data in the list. 

    Args:
        data_list (list): list containing the data read from the file

    Raises:
        ValueError: raised if there are errors in the data values in the file

    Returns:
        dictionary: contains data about the flows
    """
    list_dict = {} #create empty dict to fill in
    flag = False #flag to make sure that the returned dict actually has a correctly formated key and value 
    for i in data_list:
        try: #check if the input from the list is a string
            k, v = i.split(",") #split the single string in the list containing the key and value
            if k != None and v != None: #validating neither the key nor value are empty
                k, v = k.strip(), v.strip() #clean up the strings from white space and new lines
                try: #values can be converted to float
                    v = float(v)
                    list_dict.update({k: v}) #add to the dictionary
                    flag = True
                except ValueError:
                    print(f"Value Error: Value provided is not a number {v}")
            else:
                raise ValueError
        except AttributeError:
            print("Attribute Error: Key and Value not added")
    if flag == True:        
        return list_dict
    else:
        return ValueError         

def draw_sankey(window, title, data_dic, gap_size = 100, border_size = 100):
    """Draw the sankey diagram

    Args:
        window (GraphicsWindow): contains the graph
        title (string): contains the label to overlay on the source arrow
        data_dic (dictionary): contains the data for the graph
        gap_size (int): number of pixels to leave between destination arrows
        border_size (int): Minimum separation to othe edges of the window
    """
    pass

def main():
    # DO NOT EDIT THIS CODE
    input_file = ""
    file_read = False
    # Try to read file name from input commands:
    args = sys.argv[1:]  
    if len(args) == 0 or len(args) > 1:
        print('\n\nUsage\n\tTo visualise data using a sankey diagram type:\
            \n\n\t\tpython sankey.py infile\n\n\twhere infile is the name of the file containing the data.\n')
        print('\nWe will ask you for a filename, as no filename was provided')    
       
    else:
        input_file = args[0]
    
    # Use file provided or ask user for valid filename (we will iterate until a valid file is provided)
    while not file_read :
        # Ask for filename if not available yet
        if input_file == "" :
            input_file = input("Provide name of the file to load: ")
        
        # Try to Read the file contents
        try:
            title, left_axis_label, data_list = read_file(input_file)
            file_read = True
        except FileNotFoundError:
            print(f"File {input_file} not found or is not readable.")
            input_file = ""
            
    # Section 2: Create a window and canvas
    win = set_up_graph(title)

    # Section 3: Process the data
    try:
        data_dic = process_data(data_list)
    except ValueError as error:
        print("Content of file is invalid: ")
        print(error)
        return

    # Section 4: Draw the graph
    draw_sankey(win, left_axis_label, data_dic, GAP, 100)

    win.wait()


if __name__ == "__main__":
    main()