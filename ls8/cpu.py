"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.fl = 0b00000000
        self.pc = 0

    def load(self, path):
        """Load a program into memory."""

        address = 0

        # Loads program from ls8.py
        program = []
        try:
            with open(path) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num != "":
                        program.append(int(num, 2))
                        

        except FileNotFoundError:
            print(f"{path} not found")
            sys.exit(2)


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "SUB": 
            self.registers[reg_a] -= self.registers[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            command = self.ram_read(self.pc)

            if command == 0b00000001: #HALT
                running = False
                self.pc += 1
                print("Halted")
                sys.exit(1)
            
            elif command == 0b10000010: #LDI
                reg = self.ram_read(self.pc + 1)
                num = self.ram_read(self.pc + 2)
                self.registers[reg] = num
                self.pc += 3

            elif command == 0b01000111: #PRN
                reg = self.ram_read(self.pc + 1)
                num = self.registers[reg]
                print(num)
                self.pc += 2

            elif command == 0b10100010: #MUL
                reg_a = self.registers[self.ram_read(self.pc + 1)]
                reg_b = self.registers[self.ram_read(self.pc + 2)]
                self.registers[self.ram_read(self.pc + 1)] = reg_a * reg_b
                self.pc += 3

            elif command == 0b01010100: #JMP
                reg = self.ram_read(self.pc + 1)
                self.pc = self.registers[reg]
            
            elif command == 0b10100111: #CMP
                # clear flags from last time cmp ran
                self.fl = 0b00000000
                # get values from ram
                reg_1 = self.ram_read(self.pc + 1)
                reg_2 = self.ram_read(self.pc + 2)
                val_1 = self.registers[reg_1]
                val_2 = self.registers[reg_2]
                # make comparisons
                if val_1 == val_2:
                    self.fl = 0b00000001 #Equal
                elif val_1 < val_2:
                    self.fl = 0b00000100 #Greater Than
                elif val_1 > val_2:
                    self.fl = 0b00000010 #Less Than
                self.pc += 3
            
            elif command == 0b01010101: #JEQ
                if self.fl == 0b00000001:
                    reg = self.ram_read(self.pc + 1)
                    self.pc = self.registers[reg]
                else:
                    self.pc += 2

            elif command == 0b01010110: #JNE
                if self.fl == 0b00000100 or self.fl == 0b00000010:
                    reg = self.ram_read(self.pc + 1)
                    self.pc = self.registers[reg]
                else:
                    self.pc += 2


            else:
                print(f"Unkown command {command}")
                self.pc += 1
                print(self.pc)
        

