import socket
from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.bean.sys.memory_module import MemoryModule
from mag_tools.bean.sys.cpu import Cpu
from mag_tools.bean.sys.disk import Disk
from mag_tools.bean.sys.memory import Memory
from mag_tools.bean.sys.mother_board import Motherboard
from mag_tools.model.computer_type import ComputerType
from mag_tools.utils.security.digest import Digest


@dataclass
class Computer:
    """
    计算机类
    """
    type: ComputerType = field(default=None, metadata={"description": "计算机类型"})
    id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    name: Optional[str] = field(default=None, metadata={"description": "计算机名"})
    description: Optional[str] = field(default=None, metadata={"description": "描述"})
    cpu: Optional[Cpu] = field(default=None, metadata={"description": "CPU信息"})
    memory: Optional[Memory] = field(default=None, metadata={"description": "内存信息"})
    memory_modules: List[MemoryModule] = field(default_factory=list, metadata={"description": "内存条信息"})
    disks: List[Disk] = field(default_factory=list, metadata={"description": "磁盘信息"})
    mother_board: Optional[Motherboard] = field(default_factory=list, metadata={"description": "主板信息"})

    @classmethod
    def get_info(cls):
        """
        获取当前系统的CPU、内存和磁盘信息，并返回一个Computer实例
        """
        pc = cls(type=ComputerType.DESKTOP,
                 name=socket.gethostname(),
                 cpu=Cpu.get_info(),
                 memory=Memory.get_info(),
                 memory_modules=MemoryModule.get_info(),
                 disks=Disk.get_info(),
                 mother_board=Motherboard.get_info())

        pc.__set_id()
        return pc

    def __str__(self):
        """
        返回计算机参数的字符串表示
        """
        parts = [f"Computer(type='{self.type}'"]
        for attr, value in self.__dict__.items():
            if value is not None:
                parts.append(f"{attr}='{value}'")
        parts.append(")")
        return ", ".join(parts)

    def __set_id(self):
        modules_uuid = ''.join([module.hash for module in self.memory_modules])
        disks_uuid = ''.join([disk.hash for disk in self.disks])
        self.id = Digest.md5(f'{self.name}{self.type}{self.cpu.hash}{modules_uuid}{disks_uuid}{self.mother_board}')

        self.cpu.computer_id = self.id
        self.mother_board.computer_id = self.id

        for disk in self.disks:
            disk.computer_id = self.id
        for module in self.memory_modules:
            module.computer_id = self.id


if __name__ == "__main__":
    pc_ = Computer.get_info()
    print(pc_.id)
