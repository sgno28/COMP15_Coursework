
from ezgraphics import GraphicsWindow

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

def eg(window, title, data_dic, gap_size = 100, border_size = 100):
    WIDTH = 1000
    HEIGHT = 700
    win = GraphicsWindow(WIDTH, HEIGHT)
    win.setTitle(title)
    border_size = 100
    n = border_size
    data_flow = sum(data_dic.values()) #values sumd
    diagram_width = 1000 - (2*100) - ((len(data_dic) - 1)*gap_size) #total width to use
    ppf = diagram_width / data_flow #pixels per flow
    source_width = ppf * data_flow
    source_start = (WIDTH/2)-(source_width/2)
    source_height = 50
    source_low = border_size + source_height
    #start drawing
    canvas = win.canvas()
    canvas.drawRectangle(100,100, (800), (500)) #margins
    canvas.setFill()
    canvas.drawRectangle(source_start, border_size, source_width, source_height) #draw the source rectangle
    canvas.setTextAnchor("center")
    canvas.drawText((WIDTH / 2), 125, title)
    
    n = border_size
    for key in data_dic:
        p_data = data_dic[key] * ppf
        canvas.setFill(0,0,0)
        canvas.drawPolygon(n, (HEIGHT - 150), (n+p_data), (HEIGHT - 150), (n + (n + p_data))/2, HEIGHT - 100)
        canvas.drawText((n + (n + p_data))/2, HEIGHT - 150, key)
        canvas.drawPolygon(source_start, source_low,  n, (HEIGHT - 150), source_start + p_data, source_low, n+p_data, HEIGHT - 150)
        n = n + p_data + gap_size
        source_start = source_start + p_data
    #wait to close
    win.wait()

def main():
    title, label, data_list = readingLBL("netball_2018.txt")
    dict_data = clean_list(data_list)
    eg(title, label, dict_data)
    
    

if __name__ == "__main__":
    main()