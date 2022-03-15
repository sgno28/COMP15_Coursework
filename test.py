
from ezgraphics import GraphicsWindow

COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
(245,	130,	48),	(145,	30, 180), (70, 240,	240),	(240, 50, 230),
(210,	245,	60),	(250,	190, 212), (0, 128,	128),	(220, 190, 255),
(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195),
(128,	128,	0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]
WIDTH = 1000        # Width of the window in pixels
HEIGHT = 700        # Height of the window in pixels
GAP = 10

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
    flag = False #flag to make sure that the returned dict actually has a correctly formated key and value 
    for i in dlist:
        try: #check if the input from the list is a string
            k, v = i.split(",") #split the single string in the list containing the key and value
            if k != None and v != None: #validating neither the key nor value are empty
                k, v = k.strip(), v.strip() #clean up the strings from white space and new lines
                try: #values can be converted to float
                    v = float(v)
                    list_dict.update({k: v}) #add to the dictionary
                    flag = True
                except ValueError:
                    print("Value Error: Key and Value not added")
            else:
                raise ValueError
        except AttributeError:
            print("Attribute Error: Key and Value not added")
    if flag == True: # dict will return filled with at least one key and value  
        return list_dict
    else:
        return ValueError

def get_colour(c):
    return COLOURS[c][0], COLOURS[c][1], COLOURS[c][2]

def draw_source(canvas, title, s_start, s_width, s_height, border_size = 100):
    canvas.setFill(0,0,0)
    canvas.drawRectangle(s_start, border_size, s_width, s_height) #draw the source rectangle
    canvas.setTextAnchor("center")
    canvas.setColor(255, 255, 255)
    canvas.drawText((WIDTH / 2), 125, title)
    
def colour_grad(canvas, s_start, n, s_low, pixel, r , g, b):
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
    
def eg(win, title, data_dic, gap_size = 100, border_size = 100):
    n = border_size
    data_flow = sum(data_dic.values()) #values sumd
    diagram_width = 1000 - (2*100) - ((len(data_dic) - 1)*gap_size) #total available width to use
    ppf = diagram_width / data_flow #pixels per flow
    s_width = ppf * data_flow
    s_start = (WIDTH/2)-(s_width/2)
    s_height = 50
    s_low = border_size + s_height
    canvas = win.canvas() #start drawing
    draw_source(canvas, title, s_start, s_width, s_height, border_size) #contructs the source block
    iteration = 0 #keep track of how many destinations have been plotted to get their color
    for key in data_dic:
        p_data = data_dic[key] * ppf # calculates the pixel width for each destination
        draw_dest(canvas, key, p_data, n, s_start, s_low, iteration) #contructs the desitinations and connecters
        n = n + p_data + gap_size #moves the starting point for the destinations
        s_start = s_start + p_data #moves starting point for the source
        iteration += 1 #increases after each destination has been plotted

def main():
    title, label, data_list = readingLBL("netball_2018.txt")
    dict_data = clean_list(data_list)
    win = GraphicsWindow(WIDTH, HEIGHT)
    win.setTitle(title)
    eg(win, label, dict_data)
    win.wait()
    

if __name__ == "__main__":
    main()