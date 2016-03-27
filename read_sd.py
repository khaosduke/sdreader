#!/usr/bin/env python

import io
import struct
import json
import pprint
import copy
import binascii
import click


#definitions_file = "definitions.json"
definitions_file = "statevar_definitions.json"
types_conversion = {
	"unsigned_long" : "L",
	"unsigned_short": "H",
	"unsigned_byte" : "B",
	"float_value"   : "f",
	"double_value"  : "f",
	"signed_byte"   : "b",
	"signed_short"  : "h",
	"signed_long"   : "l"
}


class DataPrototype:
      	def __init__(self):
            with open(definitions_file) as definitions:
                self.json_defs = json.load(definitions)
            #Toss the prefix
            self.json_defs.pop(0)
            #Toss the suffix, last element
            self.json_defs.pop()

            self.dictionary_prototype = {}
	    self.block_size = 0
            for definition in self.json_defs:
                self.dictionary_prototype[definition["type"]] = "" 
	    	#Get the total block size minus the prefix and suffix
	    	self.block_size += definition["size"]
		print(definition['name'])
	    print(self.block_size)	
	def json_definition(self):
		return self.json_defs
	
	def data(self):
		return self.dictionary_prototype
	
	def size(self):
		return self.block_size

data_block_prototype = DataPrototype()

class DataBlock:
    
    def __init__(self,data_array):
        #Use the prototype to create new datablocks 
        #copy the prototype
	self.new_block = copy.deepcopy(data_block_prototype.data())
	#Since iteration doesn't guarantee order in a dictionary, we have to do this the ugly way
	names_sizes = map(self.make_tuple, data_block_prototype.json_definition()) 	
	#Map works on list preserving our order, now we can create our new block
	#print(names_sizes)	
	for element in names_sizes:
		#reads in proper size
		self.new_block[element[0]] = data_array[0:element[1]] 
		#put it in proper little endian
		if (element[0] != 'sentence') and (element[0] != 'padding'):
			self.new_block[element[0]] = struct.unpack('<'+types_conversion[element[0]],self.new_block[element[0]])[0]
		#Slice array
		data_array = data_array[element[1]:]
	#print(json.dumps(self.new_block))    

    def data(self):
	return self.new_block
 	
    def make_tuple(self,element):
	return (element["type"],element["size"])

class StreamManager:

    def __init__(self,filename):
        #Load definitions files
        with open(definitions_file) as definitions:
            json_defs = json.load(definitions)
            print(json_defs[0]["value"])
        #Load our Prefix and Suffix from the definitions, convert the string to hex then make it little endian
        StreamManager.BLOCK_PREFIX = struct.pack('<I',int(json_defs[0]["value"],0))    
        
	#StreamManager.BLOCK_SUFFIX = struct.pack('<I',int(json_defs[10]["value"],0))
        suffix_value = filter( lambda x: x['type']=='suffix',json_defs)[0]['value']
	StreamManager.BLOCK_SUFFIX = struct.pack('<I',int(suffix_value,0))
        
	#Opens file in RAW mode
        self.stream = io.FileIO(filename,'r')
        #Verify the stream format prefix is correct by checking the first 4 bytes
        prefix = self.stream.read(4)
        if prefix == StreamManager.BLOCK_PREFIX:
            print("OK!")
        else:
            raise NameError("No valid block prefix found!")
            
        #Reset the stream pointer
        self.stream.seek(0)
    
    def end_of_file(self):
        if len(self.stream.read(1)) == 0:
            #EOF
            return True
        else:
            #Return to proper place
            self.stream.seek(-1,io.SEEK_CUR)
            return False
        
    
    def is_valid_block_prefix(self,possible_prefix):
        if possible_prefix == StreamManager.BLOCK_PREFIX:
            return True
        return False
    
    def is_valid_block_suffix(self,possible_suffix):
        if possible_suffix == StreamManager.BLOCK_SUFFIX:
            return True
        return False
    
    def find_next_block(self):
        print "Searching"
	invalid_blocks = 0
        while True:
	    #Count for number of invalid blocks to search, we limit to 1000	
            #invalid_blocks = 0
	    #Check for EOF
            next_byte = self.stream.read(1)
            if len(next_byte) == 0:
                return False
            #print "Reading..."
            if  next_byte == StreamManager.BLOCK_PREFIX[0]:
                print("Found one")
                #Check to see if its a proper block, go back one byte
                self.stream.seek(-1,io.SEEK_CUR)
                possible_prefix = self.stream.read(4)
                if self.is_valid_block_prefix(possible_prefix):
                    	#We have a prefix we're ready to parse
                    	print("Found a prefix")
                    	#Reset the seek pointer
                    	self.stream.seek(-4,io.SEEK_CUR)
                    	return True
    		else:
			if invalid_blocks == 10000:
				break
			else:
				print(invalid_blocks)
				invalid_blocks +=1
			 		
    def read_in_block(self):
        #Verify block is valid, again
        if self.is_valid_block_prefix(self.stream.read(4)):
            print("Continuing...")
            #Based on the struct definitions
            block = DataBlock(self.stream.read(data_block_prototype.size()))
	    possible_suffix = self.stream.read(4)
	        #unpack as 4 bytes little endian		
            val = struct.unpack('<BBBB',possible_suffix)
            if self.is_valid_block_suffix(possible_suffix):
                print("Block was valid")
            else:
                raise NameError("Block not valid")
            return block 
                
@click.command()
@click.option('--i', default='robot-sd.img', help='Input file or device i.e /dev/sdc defaults to robot-sd.img')
@click.option('--o', default='sd.json', help='Output file default sd.json')
def main(i,o):       
    """Reads an SD card or an image file of an SD card as defined by definitions.json, outputs json""" 	                     	
    #Default input file, i, is robot-sd.img
    sm = StreamManager(i)    
    sm.find_next_block()
    number_of_blocks = 0
    data_blocks = []	
    while sm.find_next_block():
         number_of_blocks+=1
         print(number_of_blocks)
         data_blocks.append(sm.read_in_block().data())
    print("Done")
    #write to file
    with open(o, 'w') as outputfile:
		json.dump(data_blocks,outputfile,indent=4)
main()    
