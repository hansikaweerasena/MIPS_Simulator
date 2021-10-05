import sys

STARTING_MEMORY_ADDRESS = 260
disassembled_memory = []
registerFile = [0]*32
data_memory_pointer = sys.maxsize
instruction_pointer = 0
program_counter = 0


def read_file_line_by_line(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    itemList = []
    for line in Lines:
        itemList.append(line.strip())
    file1.close()
    return itemList


def get_instruction_address(int_pointer):
    return str(STARTING_MEMORY_ADDRESS + instruction_pointer * 4)


def get_instruction_str(instruction):
    instruction_str = instruction[0] + " "
    for component in instruction[1:-1]:
        instruction_str += component + ", "
    if len(instruction) > 1:
        instruction_str += instruction[-1]
    return instruction_str


def write_disassembled_code_to_file(memory, decoded_memory):
    open('disassembly.txt', 'w').close()
    with open('disassembly.txt', 'a') as the_file:
        for index, word in enumerate(memory):
            the_file.write(word + "\t")
            the_file.write(str(STARTING_MEMORY_ADDRESS + index*4) + "\t")
            if index < data_memory_pointer:
                the_file.write(get_instruction_str(decoded_memory[index]))
            else:
                the_file.write(str(decoded_memory[index]))
            the_file.write("\n")


def bin_to_int(binary_str):
    return int(binary_str, 2)


def twos_complement_int(binary_str):
    if binary_str[0] == '0':
        return bin_to_int(binary_str)
    else:
        return int(binary_str[1:], 2) - (int(binary_str[0], 2) << (len(binary_str) - 1))


def disassemble_cat_one_i(word, idx):
    op_code = word[3:6]
    inst_data = word[6:]
    if op_code == '000':
        inst_index = bin_to_int("{:032b}".format((idx + 1)*4 + STARTING_MEMORY_ADDRESS)[:4]) << 28 | bin_to_int(inst_data) << 2
        return ['J', '#' + str(inst_index)]
    elif op_code == '001':
        offset = bin_to_int(inst_data[10:]) << 2
        return ['BEQ', 'R' + str(bin_to_int(inst_data[:5])), 'R' + str(bin_to_int(inst_data[5:10])), '#' + str(offset)]
    elif op_code == '010':
        offset = bin_to_int(inst_data[10:]) << 2
        return ['BNE', 'R' + str(bin_to_int(inst_data[:5])), 'R' + str(bin_to_int(inst_data[5:10])), '#' + str(offset)]
    elif op_code == '011':
        offset = bin_to_int(inst_data[10:]) << 2
        return ['BGTZ', 'R' + str(bin_to_int(inst_data[:5])), '#' + str(offset)]
    elif op_code == '100':
        return ['SW', 'R' + str(bin_to_int(inst_data[5:10])), str(twos_complement_int(inst_data[10:])) + "(R" + str(bin_to_int(inst_data[:5])) + ")"]
    elif op_code == '101':
        return ['LW', 'R' + str(bin_to_int(inst_data[5:10])), str(twos_complement_int(inst_data[10:])) + "(R" + str(bin_to_int(inst_data[:5])) + ")"]
    elif op_code == '110':
        global  data_memory_pointer
        data_memory_pointer = idx + 1
        return ['BREAK']
    else:
        raise ValueError("Invalid Op Code for Category 1")


def disassemble_cat_two_i(word):
    op_code = word[3:6]
    dest = 'R' + str(bin_to_int(word[6:11]))
    src1 = 'R' + str(bin_to_int(word[11:16]))
    src2 = 'R' + str(bin_to_int(word[16:21]))
    if op_code == '000':
        return ["ADD", dest, src1, src2]
    elif op_code == '001':
        return ["SUB", dest, src1, src2]
    elif op_code == '010':
        return ["AND", dest, src1, src2]
    elif op_code == '011':
        return ["OR", dest, src1, src2]
    elif op_code == '100':
        return ["SRL", dest, src1, src2]
    elif op_code == '101':
        return ["SRA", dest, src1, src2]
    elif op_code == '110':
        return ["MUL", dest, src1, src2]
    else:
        raise ValueError("Invalid Op Code for Category 2")

def disassemble_cat_three_i(word):
    # Check 2's oparend or not for every instruction
    op_code = word[3:6]
    dest = 'R' + str(bin_to_int(word[6:11]))
    src1 = 'R' + str(bin_to_int(word[11:16]))
    imd_val = '#' + str(bin_to_int(word[16:]))
    if op_code == '000':
        return ['ADDI', dest, src1, imd_val]
    elif op_code == '001':
        return ['ANDI', dest, src1, imd_val]
    elif op_code == '010':
        return ['ORI', dest, src1, imd_val]
    else:
        raise ValueError("Invalid Op Code for Category 3")


def disassemble_instruction(word, idx):
    if word[0:3] == '000':
        return disassemble_cat_one_i(word, idx)
    elif word[0:3] == '001':
        return disassemble_cat_two_i(word)
    else:
        return disassemble_cat_three_i(word)


def disassemble_data(word):
    return twos_complement_int(word)


def dissemble_word(word, idx):
    if data_memory_pointer > idx:
        return disassemble_instruction(word, idx)
    else:
        return disassemble_data(word)


def disassemble_memory(memory, dissembled_memory):
    for index, word in enumerate(memory):
        dissembled_memory.append(dissemble_word(word, index))


def write_status_to_file(file, cycle):
    file.write("--------------------" + "\n")
    file.write("Cycle " + str(cycle) + ":\t" + get_instruction_address(instruction_pointer) + "\t")
    file.write(get_instruction_str(disassembled_memory[instruction_pointer]))
    file.write("\n\n")
    file.write("Registers\n")
    index_r = 0
    for index, register in enumerate(registerFile):
        if index % 8 == 0:
            file.write("R" + "{:02d}".format(index) + ":\t")
        file.write(str(register))
        if (index+1) % 8 == 0:
            file.write("\n")
        else:
            file.write("\t")
        index_r = index
    if (index_r+1) % 8 != 0:
        file.write("\n")
    index_d = 0
    file.write("\nData\n")
    for index, data in enumerate(disassembled_memory[data_memory_pointer:]):
        if index % 8 == 0:
            file.write(str(STARTING_MEMORY_ADDRESS + (data_memory_pointer + index)*4) + ":\t")
        file.write(str(data))
        if (index+1) % 8 == 0:
            file.write("\n")
        else:
            file.write("\t")
        index_d = index
    if (index_d+1) % 8 != 0:
        file.write("\n")


def simulate_instruction(instruction_pointer):
    pass



memory = read_file_line_by_line("sample.txt")
disassemble_memory(memory, disassembled_memory)
write_disassembled_code_to_file(memory, disassembled_memory)

filez = open("simulation.txt", 'w')
write_status_to_file(filez,1)