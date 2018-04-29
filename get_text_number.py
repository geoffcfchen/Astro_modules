def get_number(input_file,key_word):
     with open(input_file) as openfile:
          for line in openfile:
               counter=0
               for part in line.split():
                    counter = counter + 1
                    if key_word in part:
                         #print(line.split()[counter])
                         return line.split()[counter]

##get_TD return time delay and its uncertainty
def get_TD(input_file,key_word):
     with open(input_file) as openfile:
          for line in openfile:
               counter=0
               for part in line.split():
                    counter = counter + 1
                    if key_word in part:
                         return float(line.split()[counter]),float(line.split()[counter+1])
