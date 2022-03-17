
"""Draw a sankey diagram using data from a given input file.
    Student Number: 20058670
    comment: the inital line: "#!/usr/bin/env python3" was removed as it caused my program to crash. Please reinsert it if you can not run program. 
"""
import sys
from ezgraphics import GraphicsWindow

WIDTH = 1000        # Width of the window in pixels
HEIGHT = 700        # Height of the window in pixels
GAP = 100            # Gap between disagram arrows in pixels
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
    try: #values can be converted to float
        str = float(str)
        return str
    except ValueError:
        print(f"Value Error: Value provided is not a number {str}\nLine: {line_number} is not valid.")
        raise ValueError

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
                v = parse_value(v, i)
                list_dict.update({k: v}) #add to the dictionary
                flag = True
            else:
                raise ValueError
        except AttributeError:
            print("Attribute Error: Key and Value not added")
    if flag == True:        
        return list_dict
    else:
        return ValueError         

def get_colour(c):
    """Retreives the the colour RGB from the gloab COLOURS list
    Args: 
        c (int): A number representing the index for the global list COLOURS that will be assessed
    Returns:
        3 integer values representing the amount of red, green and blue needed for that colour
    """
    return COLOURS[c][0], COLOURS[c][1], COLOURS[c][2]

def draw_source(canvas, title, ppf, df, border = 100):
    """Caclulate source and draw the source block for the diagram.
    Args:
        canvas (Object from Ezgraphics module): contains the object instance that holds the graph
        title (string): contains the label to overlay on the source block
        ppf (int): the number of pixels per data flow
        df (int): the amount of data into each flow 
        border_size (int): the amount of pixels for the borders or margins of the window set default to 100
    Returns:
        start (int) the starting x coordinate for the source block
        low (int) the lowest y coordinate of the s block 
    """
    width = ppf * df
    start = (WIDTH/2)-(width/2)
    height = 50
    low = border + height
    canvas.setFill(0,0,0)
    canvas.drawRectangle(start, border, width, height) #draw the source rectangle
    canvas.setTextAnchor("center")
    canvas.setColor(255, 255, 255)
    canvas.drawText((WIDTH / 2), 125, title)
    return start, low
    
def colour_grad(canvas, s_start, n, s_low, pixel, r , g, b):
    """Contsruct the colour gradient for the connectors from source to destination
    Args:
        canvas (Object from Ezgraphics module): contains the object instance that holds the graph
        s_start (int): starting x coordinate for the source
        n (int): the starting x coordinate for each destination
        s_low (int): the Y coordinate representing the bottom of the source block
        pixel (int): width of each destination
        r (int): A number representing the amount of red
        g (int): A number representing the amount of green
        b (int): A number representing the amount of blue
    """
    x = s_start #x corrdinate initially for the lines
    h = (HEIGHT - 150) - s_low #height between the source low and destination high
    shift = n - s_start  #difference between the x cordinate of the destination and source block
    dx = shift / h #shift per unit height
    dr, dg, db = (r/h), (g/h), (b/h) #change in colour per line 
    for i in range(0, h+1): #from the start to the maximum height
        r , g, b = round(i*dr), round(i*dg), round(i*db)  
        canvas.setColor(r, g, b)
        canvas.drawLine(x + 1, i + s_low, x + pixel, i + s_low)
        x = x + dx

def draw_dest(canvas, key, pixel, n, start, low, c):
    """Draw the shapes in the diagram such as the destination and connectors
    Args:
        Canvas (Object from Ezgraphics module): contains the object instance that holds the graph
        key (string): contains the label of the destinations
        pixel (int): width of each destination
        n (int): the starting x coordinate for each destination
        start (int): starting x coordinate for the source
        low (int): the Y coordinate representing the bottom of the source block
        c (int): A number representing the index for the global list COLOURS that will be assessed
    """
    r, g, b = get_colour(c)
    canvas.setColor(0, 0, 0)
    canvas.setFill(r, g, b) #sets colour of destinations
    canvas.drawPolygon(n, (HEIGHT - 150), (n+pixel), (HEIGHT - 150),\
        (n + (n + pixel))/2, HEIGHT - 100) #contructs the destinations
    canvas.setColor(0,0,0)
    canvas.drawPolygon(start, low, start +\
            pixel, low, n+pixel, HEIGHT - 150, n, (HEIGHT - 150)) #draws the connectors
    colour_grad(canvas, start, n, low, pixel,r, g, b) #construct the color gradient
    canvas.setColor(255-r, 255 - g, 255 - b) #sets colour of the destination label
    canvas.drawText((n + (n + pixel))/2, HEIGHT - 150, key) #forms the destination label

def draw_sankey(window, title, data_dic, gap_size = 100, border_size = 100):
    """Draw the sankey diagram
    Args:
        window (GraphicsWindow): contains the graph
        title (string): contains the label to overlay on the source arrow
        data_dic (dictionary): contains the data for the graph
        gap_size (int): number of pixels to leave between destination arrows
        border_size (int): Minimum separation to othe edges of the window
    """
    n = border_size
    data_flow = sum(data_dic.values()) #values sumd
    diagram_width = 1000 - (2*100) - ((len(data_dic) - 1)*gap_size) #total available width to use
    ppf = diagram_width / data_flow #pixels per flow
    canvas = window.canvas() #start drawing
    s_start, s_low = draw_source(canvas, title, ppf, data_flow, border_size) #contructs the source block
    iteration = 0 #keep track of how many destinations have been plotted to get their color
    for key in data_dic:
        p_data = data_dic[key] * ppf # calculates the pixel width for each destination
        draw_dest(canvas, key, p_data, n, s_start, s_low, iteration) #contructs the desitinations and connecters
        n = n + p_data + gap_size #moves the starting point for the destinations
        s_start = s_start + p_data #moves starting point for the source
        iteration += 1 #increases after each destination has been plotted

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