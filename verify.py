#!/usr/bin/env python
import click
import json


def verify_sizes(json_data):
    padding = 0
    #Get the padding size
    for element in reversed(json_data):
        if element['type'] == 'padding':
            padding = int(element['size'])
            break
        
    #Add all the sizes and make sure padding matches
    total = 0
    for element in json_data:
        total += int(element['size'])
    
    if total!=512:
        padding_should_be = 512-(total-padding)
        return "Block size not 512! " + "Padding should be: " + str(padding_should_be)  
    else:
        return "Sizes add up"      

@click.command()
@click.option('--i',default="definitions.json", help='Definitions file')
def main(i):
    """Verifies the definitions file"""
    with open(i) as definitions:
        json_defs = json.load(definitions)
        
    print verify_sizes(json_defs)	
main()    