#!/usr/bin/env python

import struct

CONFIG_ARM_VEXPRESS_RAMBASE = 0x60000000
PT_LVL1_SHIFT     = 30
PT_LVL2_SHIFT     = 21
PT_LVL3_SHIFT     = 12
PT_ENTRY_SIZE     = 8


def pt_lvl_offset(lvl, addr):
  if lvl == 1:
    return ((addr >> PT_LVL1_SHIFT) & 0x003) << 3
  elif lvl == 2:
    return ((addr >> PT_LVL2_SHIFT) & 0x1FF) << 3
  elif lvl == 3:
    return ((addr >> PT_LVL3_SHIFT) & 0x1FF) << 3


# Type
PT_ENTRY_TABLE    = 0x3
PT_ENTRY_BLOCK    = 0x1

# Upper block attributes
PT_ENRTY_ATTR_XN  = (1 << 54)
PT_ENTRY_ATTR_PXN = (1 << 53)
PT_ENTRY_ATTR_CN  = (1 << 52)

# Lower block attributes
PT_ENTRY_ATTR_NG = (1 << 11)
PT_ENTRY_ATTR_AF = (1 << 10)
PT_ENTRY_ATTR_SH = (1 <<  8)
PT_ENTRY_ATTR_AP = (1 <<  6)
PT_ENTRY_ATTR_NS = (1 <<  5)
PT_ENTRY_ATTR_AI = (1 <<  0)


class Hypervisor:
  def __init__(self, name, phys_base, virt_base):
    self.name = name
    self.phys_base = phys_base
    self.virt_base = virt_base

class Mapping:
  def __init__(self, name, phys_base, virt_base, size):
    self.name = name
    self.phys_base = phys_base
    self.virt_base = virt_base
    self.size = size

class PTable:
  def __init__(self, hypervisor):
    # Base address of the pagetable
    self.base = 0x68000000
    self.mappings = []

  def add(self, mapping):
    self.mappings.append(mapping)

  def create(self):
    pt_lvl1_base = 0x0
    pt_lvl2_base = 0x1000
    pt_lvl3_base = 0x2000

    ptbin = open('hyp_ptable', 'wb')

    #ptbin.seek(0x18, 0)
    #ptbin.write(struct.pack("<Q", 0x2))

    for mapping in self.mappings:
      # We handle 1G mappings here
      if mapping.size >= (1 << 30):
        pos = self.base + (entry.phys_base >> PT_LVL1_SHIFT)

      # We handle 2M mappings here
      elif mapping.size > (1 << 20):
        pass

      # We handle 4K mappings here
      elif mapping.size >= (1 << 12):
        
        #### Create lvl1 entry

        print("Virtual address: %x\n" % mapping.virt_base)
        
        pos_l1 = pt_lvl1_base + pt_lvl_offset(1, mapping.virt_base)
        entry = ((self.base + pt_lvl2_base) | PT_ENTRY_TABLE)
        print("pos_l1: %x" % pos_l1)
        print("entry:  %x\n" % entry) 
        ptbin.seek(pos_l1, 0)
        ptbin.write(struct.pack("<Q", entry))

        #### Create lvl2 entry

        pos_l2 = pt_lvl2_base + pt_lvl_offset(2, mapping.virt_base)
        entry = ((self.base + pt_lvl3_base) | PT_ENTRY_TABLE)
        print("pos_2: %x" % pos_l2)
        print("entry: %x\n" % entry)
        ptbin.seek(pos_l2, 0)
        ptbin.write(struct.pack("<Q", entry))
       
        #### Create lvl3 entry

        pos_l3 = pt_lvl3_base + pt_lvl_offset(3, mapping.virt_base)
        entry = ((0x10009000 & 0xFFFFF000) | PT_ENTRY_TABLE)
        print("pos_l3: %x" % pos_l3)
        print("entry: %x" % entry)
        ptbin.seek(pos_l3, 0)
        ptbin.write(struct.pack("<Q", entry))


class PTEntryTable:

  def __init__(self, type):
    pass

  def format(self):
    return "<Q"
    #1 00 00 0000000 000000000000    11

class PTEntry:
  def __init__(self, type = "table"):
    self.type = type


vh1 = Hypervisor("vh1", CONFIG_ARM_VEXPRESS_RAMBASE + 0x8000,  0xf6000000)

ptable = PTable(vh1)
ptable.add(Mapping("uart0", 0x10009000, 0xf7000000, 0x1000))
#ptable.add(Mapping("gicv2", 0x0, 0xf7002000, 0x1000))

ptable.create()
