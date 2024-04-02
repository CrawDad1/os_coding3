# create a representation of a paging system
# entry point in main()
import os
from typing import List

# globals
physical_memory = {}

class memory_manager:
    addr_length: int
    page_num_length: int
    block_size: int
    capacity: int
    logical_addresses: list
    page_table: dict
    
    def __init__(self, _addr_length: int = 4, _block_size: int = 1) -> None:
        self.addr_length = _addr_length
        self.page_num_length = self.addr_length - 2
        self.block_size = _block_size
        self.capacity = pow(16, self.page_num_length)
        self.page_table = {}
        self.logical_addresses = []
    
    def divide_block(self, block: str) -> List[str]:
        return [block[i:i+self.block_size] for i in range(0, len(block), self.block_size)]
    
    def save_to_physical_memory(self,  data: str) -> None:
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

    def translate_logical_address(self) -> str:
        print("Translating logical address...")
        print("logical address| page number | physical address | data")
        for addr in self.logical_addresses:
            page_number = addr[2:][:self.page_num_length]
            offset = addr[2:][self.page_num_length:]
            physical_addr = self.page_table.get(page_number) + offset
            data = physical_memory.get(physical_addr)
            print(f" {addr} -> {page_number} -> {physical_addr} -> {data}")
        print()
    
    def cat(self) -> str:
        print("Concatenating memory values...")
        output = ""
        for addr in self.logical_addresses:
            page_number = addr[2:][:self.page_num_length]
            offset = addr[2:][self.page_num_length:]
            physical_addr = self.page_table.get(page_number) + offset
            output += physical_memory.get(physical_addr)
        
        print(output)
        return output
    
    def print_tables(self) -> None:
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
    mmu.translate_logical_address()
    mmu.cat()

if __name__ == "__main__":
    main()
