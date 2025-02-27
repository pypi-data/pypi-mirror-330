from dataclasses import dataclass, field
from typing import Optional

import psutil

from mag_tools.model.fs_type import FsType

@dataclass
class DiskPartition:
    computer_id: Optional[str] = field(default=None, metadata={"description": "所属计算机的标识"})
    device: Optional[str] = field(default=None, metadata={"description": "设备"})
    fs_type: Optional[FsType] = field(default=None, metadata={"description": "文件系统"})
    mount_point: Optional[str] = field(default=None, metadata={"description": "驱动装载点"})
    opts: Optional[str] = field(default=None, metadata={"description": "挂载选项"})

    @classmethod
    def get_info(cls):
        partition_infos = []

        partitions = psutil.disk_partitions()
        for partition in partitions:
            info = cls(device=partition.device,
                       fs_type=FsType.of_code(partition.fstype),
                       mount_point=partition.mountpoint,
                       opts=partition.opts)
            partition_infos.append(info)

        return partition_infos

    def __str__(self):
        """
        返回磁盘分区参数的字符串表示
        """
        attributes = [f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}" for attr in vars(self) if getattr(self, attr) is not None]
        return ", ".join(attributes)