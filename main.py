import fileinput
import glob
import re
import FileOutput
import os
import vininfo

is_hex = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars
is_numeric = re.compile('[-0-9.]+')
is_alnum = re.compile('^[a-zA-Z0-9]+$')
is_badvin = re.compile('[IOQioq]')

last_token = ''
current_data = []
current_tokens = []
result_txt = ""
token_index_dict = {".asc": ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1],
                    ".csv": ["csv",",",1,7,99,10,11,12,13,14,15,16,17,6,6], # TODO why is csv shorter? (currently need to repeat last element for unknown reason)
                    ".txt": ["txt",",",0,2,3,4,5,6,7,8,9,10,11,1,1]}
asc_tokens = ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1] # token order: time(abs),arb,DLC,data bytes 0-7, network
csv_tokens = ["csv",",",1,7,99,10,11,12,13,14,15,16,17,6,6] # TODO why is csv shorter? (currently need to repeat last element for unknown reason)
txt_tokens = ["txt",",",0,2,3,4,5,6,7,8,9,10,11,1,1]

for line in fileinput.input(glob.glob("samples/*.asc") + glob.glob("samples/*.csv") + glob.glob("samples/*.txt")):

    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        new = FileOutput.FileOutput(fileinput.filename())
        print("Created new file from " + fileinput.filename())
        current_tokens = token_index_dict[os.path.splitext(fileinput.filename())[1]]

    tokenList = line.split(current_tokens[1])  # tokenize each line

    current_data = []
    for i, d in enumerate(tokenList):
        if d == '8' and tokenList[i-1] == 'd':
            for j in range(7):
                current_data.append(tokenList[i+j+1])
            current_data.append(str(tokenList[i+8])[:2])

    # print(current_data)
    out_data = ""
    print_data = ""
    for i, d in enumerate(current_data):
        dcd_data = (bytearray.fromhex(current_data[i]).decode(encoding='latin-1'))
        out_data += dcd_data
        if is_alnum.match(dcd_data):
            print_data += dcd_data
    if print_data.__len__() >= 1 and not bool(is_badvin.match(print_data)):
        result_txt += print_data
print(result_txt)
    # currently this just prints all valid VIN chars in each file in the order they appear
    # need to use arb ID to filter out request messages




