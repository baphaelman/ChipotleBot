import re
import csv

def read_openings():
    openings_raw = []
    with open('openings.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            openings_raw.append(row)
    
    openings = []
    for line in openings_raw:
        cleaned_line = re.sub(r'\d+\.', '', line[2])  # Remove all numbers followed by a period
        openings.append(cleaned_line.strip())  # Strip any leading/trailing whitespace
    
    openings_dict = {}
    for opening in openings:
        add_to_dict(opening, openings_dict)
    return openings_dict

def add_to_dict(opening: str, openings_dict: dict):
    curr_string = ''
    opening_list = opening.split()
    for i in range(len(opening_list) - 1):
        this_move = opening_list[i]
        next_move = opening_list[i + 1]
        if not curr_string: # for first move
            curr_string += this_move
        else: 
            curr_string += ' ' + this_move
        
        if curr_string not in openings_dict: # if another opening not already in dict
            openings_dict[curr_string] = [next_move]
        else:
            openings_dict[curr_string].append(next_move)

if __name__ == "__main__":
    print(read_openings())