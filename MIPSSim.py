STARTING_MEMORY_ADDRESS = 260
memory = []
disassembled_memory = []
registerFile = []
data_memory_pointer = 0


def readFileLineByLine(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    itemList = []
    for line in Lines:
        itemList.append(line.strip())
    file1.close()
    return itemList


def write_deassembled_code_to_file(memory, decoded_memory):
    open('dout.txt', 'w').close()
    with open('dout.txt', 'a') as the_file:
        for word in memory:
            the_file.write(memory + "\n")


memory = readFileLineByLine("sample.txt")
print(memory)
