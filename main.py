import huffman 

# wait = ''

# while(wait != 'N'):
#   text = input("Unesite tekst koji ce se kodirati: ")

#   l = huffman.Algorithm(list(text))

#   l.get_occurrences()

#   l.print_example()

#   wait = input('Ponovo? Y/N\n>>>')

x = huffman.Algorithm()

x.encode_string('''INPUT TEXT GOES HERE''')

x.print_example()