STARTING_MEMORY_ADDRESS = 260
memory = []
decoded_memory = []
registerFile = []

def readFileLineByLine(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    itemList = []
    for line in Lines:
        itemList.append(line.strip())
    file1.close()
    return itemList


memory = readFileLineByLine("sample.txt")
print(memory)