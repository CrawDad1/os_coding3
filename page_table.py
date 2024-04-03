"""
    Create a representation of a paging system. Entry point in main()

    codeauthor : Devon Crafword
"""
import os
from typing import List

# globals
physical_memory = {}

class memory_manager:
    """Class for modeling a paging system. """
    addr_length: int
    page_num_length: int
    block_size: int
    capacity: int
    logical_addresses: list
    page_table: dict
    
    def __init__(self, _addr_length: int = 4, _block_size: int = 1) -> None:
        """
            Initializes a new instance of the memory_manager class.

            :param _addr_length: The length of the address in bytes.
            :param _block_size: The size of a block in bytes.
            :param _capacity: The capacity of the paging system.
        """
        self.addr_length = _addr_length
        self.page_num_length = self.addr_length - 2
        self.block_size = _block_size
        self.capacity = pow(16, self.page_num_length)
        self.page_table = {}
        self.logical_addresses = []
    
    def divide_block(self, block: str) -> List[str]:
        """Return a list of sub-block elements of self.block_size from the given block."""
        return [block[i:i+self.block_size] for i in range(0, len(block), self.block_size)]
    
    def save_to_physical_memory(self,  data: str) -> None:
        """Populates the physical memory with data."""

        # ensure data is str
        if not isinstance(data, str):
            data = str(data)

        logical_table = self.create_logical_memory(data)
        print("printing addresses for physical memory")
        print(" addr | page_num | offset | phys_addr | block")

        for addr, block in logical_table.items():
            page_num = addr[2:][:self.page_num_length]
            offset = addr[2:][self.page_num_length:]
            if not self.page_table.get(page_num):
                self.page_table[page_num] = rand_hex(self.page_num_length)
            phys_addr = self.page_table.get(page_num) + offset
            physical_memory[phys_addr] = block

            print(f"{addr} | {page_num} | {offset} | {phys_addr} | {block}")

    def create_logical_memory(self, data: str) -> dict:
        """Create logical memory with address and data to prepare for storage."""
        logical_table = {}
        sub_blocks = self.divide_block(data)
        for sub_block in sub_blocks:
            if not logical_table:
                logical_table = {rand_hex(self.addr_length): sub_block}
                continue
            
            if len(logical_table) > self.capacity:
                print("page capacity reached")
                break # table is full
           
            addr = max(logical_table.keys())
            # cast addr to hex string
            addr = hex(int(addr, 16) + self.block_size)
            logical_table[addr] = sub_block
        
        self.logical_addresses.extend([x for x in logical_table.keys()])
        return logical_table

    def translate_all_logical_address(self) -> str:
        """Demonstrate how to translate logical addresses to physical addresses."""
        print("Translating logical addresses...")
        print("logical address| page number | physical address | data")
        for addr in self.logical_addresses:
            page_number = addr[2:][:self.page_num_length]
            offset = addr[2:][self.page_num_length:]
            physical_addr = self.page_table.get(page_number) + offset
            data = physical_memory.get(physical_addr)
            print(f" {addr} -> {page_number} -> {physical_addr} -> {data}")
        print()
    
    def translate_logical_address(self, addr: str) -> str:
        """Translates a given logical address to physical address and retrieve data block."""
        if addr not in self.logical_addresses:
            print("logical address not found")
            print("Please enter a valid address from the following list:")
            print(self.logical_addresses)
            return ""

        # addr found in logical addresses
        print("logical address found")
        print("logical address| page number | physical address | data")
        page_number = addr[2:][:self.page_num_length]
        offset = addr[2:][self.page_num_length:]
        physical_addr = self.page_table.get(page_number) + offset
        data = physical_memory.get(physical_addr)
        print(f" {addr} -> {page_number} -> {physical_addr} -> '{data}'")
        return data

    
    def cat(self) -> str:
        """concatenate all memory values tanslated from logical -> page -> phisical -> data."""
        print("Concatenating memory values...")
        output = ""
        for addr in self.logical_addresses:
            page_number = addr[2:][:self.page_num_length]
            offset = addr[2:][self.page_num_length:]
            physical_addr = self.page_table.get(page_number) + offset
            output += physical_memory.get(physical_addr)
        print(output + "\n")
        return output
    
    def print_tables(self) -> None:
        """Prints the logical, page, and physical memory tables."""
        print("printing logical addresses...")
        print(self.logical_addresses)
        print()
    
        print("Priting page table...")
        for addr, block in self.page_table.items():
            print(f"{addr} : {block}")
        
        print()
        print("printing physical memory...")
        for addr, block in physical_memory.items():
            print(f"{addr} : {block}")
        
    
def rand_hex(length: int) -> str:
    return '0x'+ os.urandom(int(length/2)).hex()

def main() -> None:
    mmu = memory_manager(4, 4)
    mmu.save_to_physical_memory("this is a big block")
    # mmu.print_tables()
    mmu.translate_all_logical_address()
    print("\n\n Begining input loop...")
    while True:
        print("enter an address, or 'cat' to concatenate all memory values, or 'exit' to exit")
        print("Please enter a valid address from the following list:")
        print(mmu.logical_addresses)
        print("\n\n")
        try:
            addr = input("Logical address: ")
            match addr:
                case "exit":
                    break
                case 'cat':
                    mmu.cat()
                case _:
                    mmu.translate_logical_address(addr)
            print("\n")
        except ValueError:
            print("value error. please try again")
            continue

if __name__ == "__main__":
    main()
