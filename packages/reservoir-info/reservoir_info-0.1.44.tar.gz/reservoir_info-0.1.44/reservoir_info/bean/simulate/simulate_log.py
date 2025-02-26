from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from mag_tools.bean.common.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils

from bean.simulate.comp_log import CompLog

from bean.simulate.blk_log import BlkLog
from reservoir_info.bean.simulate.performance_statistics import PerformanceStatistics
from reservoir_info.bean.simulate.model_params import ModelParams
from reservoir_info.bean.simulate.stage import Stage
from reservoir_info.model.simulate_type import SimulateType


@dataclass
class SimulateLog(BaseData):
    simulate_type: SimulateType = field(default=None, metadata={"description": "模拟方式"})
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    # 头描述信息
    version: str = field(init=False, default=2023.1, metadata={'description': '程序版本'})
    bits: str = field(init=False, default=2023.1, metadata={'description': '程序位数'})
    compile_date: str = field(init=False, default='Oct 16 2024', metadata={'description': '编译日期'})
    corp_name: str = field(init=False, default='Ennosoft company of China', metadata={'description': '公司名称'})
    case_file: Optional[str] = field(default=None, metadata={"description": "模型方案文件"})
    console_path: Optional[str] = field(default=None, metadata={"description": "模型模拟程序"})
    start_time: Optional[datetime] = field(default=None, metadata={"description": "模型模拟开始时间"})
    #
    stages: List[Stage] = field(init=False, default_factory=list, metadata={'description': '模拟阶段列表'})
    model_params: Optional[ModelParams] = field(init=False, default=None, metadata={'description': '模型参数'})
    performance_statistics: Optional[PerformanceStatistics] = field(init=False, default=None, metadata={'description': '性能统计信息'})

    def set_id(self, computer_id: str, uuid: str):
        self.computer_id = computer_id
        self.uuid = uuid

        if self.model_params:
            self.model_params.uuid = uuid

        if self.performance_statistics:
            self.performance_statistics.uuid = uuid

        for stage in self.stages:
            stage.uuid = uuid

    @classmethod
    def builder(cls, log: str, simulate_type: SimulateType):
        block_lines = log.split('\n')
        if simulate_type == SimulateType.COMP:
            return CompLog.from_block(block_lines)
        elif simulate_type == SimulateType.BLK:
            return BlkLog.from_block(block_lines)
        return None