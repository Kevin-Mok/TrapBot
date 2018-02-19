# Description:
# File used to test bits of code to add into trapbot.py.

# -*- coding: utf-8 -*-
import re

#  test_string {{{ # 
test_string = ' I’m sure you’ve heard it but\n\nKendrick Lamar - Humble (Skrillex Remix)\n\nAnd these are bangers\n\nMontell2099 - Hunnid on the Drop (Mr. Carmack Remix)\n\nASAP Rocky - Lord Pretty Flacko Joyde 2 (Y2K Remix)\n\nEkali - Babylon (feat. Denzel Curry) (Woodpile flip)\n\nBrockhampton - Stains (Whethan Bootleg)\n\nKrane and B. Lewis - PCP (feat. Nick Row)\n\nSorry bout no links I’m on mobile\n'
search_words = ["kendrick", "hunnid", "denzel"]
#  }}} test_string #

#  reg_str() {{{ # 
def reg_str():
    matches = re.findall("(.+)\s-\s(.+)", test_string)
    #  if matches:
        #  print("true")
    for match in matches:
        #  print("0 = {0}, 1 = {1}".format(match[0], match[1]))
        print("{0} {1}".format(match[0], match[1]))
#  }}} reg_str() #

#  reg_url_file {{{ # 
def reg_url_file(file_name):
    file = open(file_name)
    for line in file:
        #  print(line)
        last_slash_index = line.rfind('/')
        title_words = line[last_slash_index + 1:].replace("\n", "").split('-')
        for word in search_words:
            if word in title_words:
                print("'{0}' was found in '{1}'".format(word, title_words))
#  }}} reg_url_file # 

if __name__ == '__main__':
    #  file_name = 'urls.txt'
    #  reg_url_file(file_name)
    reg_str()
