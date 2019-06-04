import os 
import csv
import json

path = './jsonfiles'
files = []

#createing CSV comparision result to display on the web page
def data_set_creator():
    #json objet to store pass fail result and additional information
    result ={}
    create_file_list()
    #Reading the files recived from the directory. Can be improved later
    with open(files[0]) as json_file:  
        file_data_1 = json.load(json_file)
    with open(files[1]) as json_file:  
        file_data_2 = json.load(json_file)
    f= open("./output/data.csv","w")
    if(file_data_1 == file_data_2):
        result['line1'] = "No mismatch"
        result['line2'] = 100
        result['line3'] = "Complete match"
        result['line3C'] = "green"            
    else:
        result['line1'] = "Mismatch in files"
        result['line3'] = "Incomplete match"
        result['line3C'] = "red"  
        json_file1 = open(files[0])
        json_file2 = open(files[1])
        count = 1
        issueline_count = 0
        f.write(files[0] + " --> Extra Lines \n") 
        for lines in json_file1:
            count+=1
            if lines not in json_file2:
                issueline_count+=1
                f.write(str(count)+" "+lines+"\n")
        file1_mismatch_percent = (issueline_count/count)*100
        f.write(files[1] + " --> Extra Lines \n")
        count = 1
        issueline_count = 0
        json_file1.close()
        json_file2.close()
        json_file1 = open(files[0])
        json_file2 = open(files[1])
        for line in json_file2:
            count+=1
            if line not in json_file1:
                issueline_count+=1
                f.write(line+"\n")  
        json_file1.close()
        json_file2.close()
        file2_mismatch_percent = (issueline_count/count)*100 
        result['line2'] = 100 - round((file1_mismatch_percent+file2_mismatch_percent)/2)
    f.close()
    #creating the final data csv whiching going to be used to display in HTML
    f= open("./output/data.csv","r")
    fhand = open('./output/data.js', 'w')
    fhand.write("myData = [\n")
    #f1= open("./output/data_fin.csv","w")
    for line in f.readlines():
        if line.strip() == '':
            continue
        output = "{"+"x1:"+'"'+line.replace('"','').strip('\n')+'"'+"},\n"
        fhand.write(output)
    fhand.write("\n];\n")
    fhand.close()
    #creating the json file for he HTML page
    outputdetails = open("./output/file.js",'w')
    outputdetails.write("extradata = ")
    outputdetails.write(json.dumps(result))
    outputdetails.close
    

#Function is being used to go through a complete folder and add CSV file path to the file global variable
def create_file_list():
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))

#main function
if __name__ == "__main__":
    data_set_creator()