from collections import Counter
from tabulate import tabulate
from operator import itemgetter
from binary_tree import Node

class Algorithm():
    def __init__(self, input_string = ''):
        self.input_string = input_string
        self.char_dictionary_array = []
        self.huffman_codes = {}
        
    # Gets probability of each character
    def _get_probability(self, occurrences): 
        p_of_o = 100 / (len(self.input_string) / occurrences) # p_of_o = orobability_of_occurence
        return round(p_of_o, 5)

    # Creates sorted array from a dictionary using 'itemgetter'
    def _create_sorted_array(self, dict, rev=True):
        return sorted(dict, key=itemgetter('occurrences'), reverse=rev)

    # Gets the occurrence of each letter using 'Counter'
    def get_occurrences(self):
        counter_str = Counter(self.input_string)
        counter_str_keys = counter_str.keys()

        array = []
        for i in counter_str_keys:
            probability = self._get_probability(counter_str[i])
            array.append({'character': i, 'occurrences': counter_str[i], 'probability': probability})

        self.char_dictionary_array = self._create_sorted_array(array)

    # Creates a list from given dictionary using only given keys
    def _create_array_from_dict(self, array, key):
        result_array = []
        for element in array:
            result_element = []
            for j in key:
                result_element.append(element[j])
            result_array.append(result_element)
        return result_array

    # Creates a binary tree using the 'binary_tree' class
    def _create_binary_tree(self):
        array = self.char_dictionary_array
        array = self._create_array_from_dict(array, ['character', 'occurrences'])
        array_of_nodes = []

        # For each element in our character array (that is for each character)
        # A new instance of the class 'binary_tree' will be created (Node)
        for element in array:
            node = Node(element[0], element[1])
            array_of_nodes.append(node)

        # Empties the list 'array_of_nodes' untill there is only one element left
        # That element represents the root of our binary tree
        while (len(array_of_nodes) != 1):
            # Pop index represents the index of the Node that should be removed from the list
            pop_index = -1 
            left = array_of_nodes[-2]
            right = array_of_nodes[-1]
            
            # Used to check if there are better combinations, that is if our current Node should
            # connect with the left or the right node
            if (len(array_of_nodes) > 3):
                if (right.occurrences + left.occurrences > left.occurrences + array_of_nodes[-3].occurrences):
                    left = array_of_nodes[-3]
                    right = array_of_nodes[-2]
                    pop_index = -2
            
            # Removing two elements at 'pop_index' index (-2 or -1)
            array_of_nodes.pop(pop_index)
            array_of_nodes.pop(pop_index)
            
            # Creating a 'top' Node, that is the parent of two previously removed nodes
            # It contains the combination of the charactes and sum of its occurrences
            top = Node(left.char + right.char, left.occurrences + right.occurrences, left, right)
            array_of_nodes.append(top)

        # Now, we need to create array_of_characters because we want to go through our binary tree in the next step
        array_of_characters = self._create_array_from_dict(self.char_dictionary_array, ['character'])
        self._calculate_huffman(array_of_nodes[0], array_of_characters)

    # Calculates the huffman code for each letter using the 'binary_tree' class method 'order_tree_by_root'
    def _calculate_huffman(self, node, characters):
        result_array = Node.order_tree_by_root(node, characters)
                
        for i in range(len(result_array)):
            self.char_dictionary_array[i]['huffman_code'] = result_array[i]
            self.huffman_codes[self.char_dictionary_array[i]['character']] = result_array[i]
    
    def _to_binary(self, string):
        l, m = [], []
        for i in string:
            l.append(ord(i))
        for i in l:
            m.append(bin(i)[2:])
        return m
    
    # Method for creating CHARACTERxHUFFMAN_CODE header, used for files
    def _get_header(self):
        result_array = []
        characters = list(self.huffman_codes.keys())
        
        for i in range(len(self.huffman_codes)):
            result_array.append(characters[i] + 'x' + self.huffman_codes[characters[i]])
        
        return result_array
            
    def encode_string(self, input = ''):
        if(input == ''):
            input = self.input_string 
        else:
            self.input_string = input
            self.get_occurrences()
            self._create_binary_tree()
               
        result_array = []
               
        for i in self.input_string:
            result_array.append(self.huffman_codes[i])
        
        return result_array
    
    def decode_string(self, header):
        pass
    
    def _print_result(self, encoded, binary):
        encoded_size = encoded.st_size
        binary_size = binary.st_size
        
        diff = binary_size - encoded_size
        diff_percentage = f'{round((encoded_size / binary_size) * 100)}'
        
        data = [['Binarni kod', binary_size], ['Huffman-ov algoritam', encoded_size], ['Razlika', diff], ['(U procentima)', diff_percentage]]
        col_names = ['', 'Velicina datoteke (u bitovima)']
        print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
            
    def create_encoded_file(self, filename = 'default'):
        import os
        encoded_string = self.encode_string()
        header = self._get_header()
        file = open(f"{os.getcwd()}\{filename}.hfm", "w")
        file.writelines((f"{' '.join(header)}\n", f"{' '.join(encoded_string)}\n"))
        file.close()
        
        file_coded_stat = os.stat(f"{os.getcwd()}\{filename}.hfm")
                
        binary_string = self._to_binary(self.input_string)
        file = open(f"{os.getcwd()}\{filename}.txt", "w")
        file.writelines(' '.join(binary_string))
        file.close()
        
        file_binary_stat = os.stat(f"{os.getcwd()}\{filename}.txt")
        
        self._print_result(file_coded_stat, file_binary_stat)
    
    # Used to create tables for showing the data on screen using 'tabulate'
    def create_table(self, step=0):
        if(step == 0):
            data = self._create_array_from_dict(self.char_dictionary_array, ['character', 'occurrences', 'probability'])
            col_names = ['Simbol', 'Broj pojavljivanja', 'Verovatnoca pojavljivanja']
            print(tabulate(data, headers=col_names, tablefmt="fancy_grid", floatfmt='.5f'))
        if(step == 1):
            data = self._create_array_from_dict(self.char_dictionary_array, ['character', 'huffman_code'])
            col_names = ['Simbol', 'Huffman-ov kod']
            print(tabulate(data, headers=col_names, tablefmt="fancy_grid", floatfmt='.5f'))

    def print_example(self):
        self.create_table()
        self._create_binary_tree()
        self.create_table(1)
        self.create_encoded_file()
        
    def print(self):
        #self.create_table()
        self._create_binary_tree()
        self.create_encoded_file()