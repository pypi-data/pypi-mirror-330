from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.bean.common.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils

from reservoir_info.model.simulate_type import SimulateType
from reservoir_info.bean.simulate.process_step import ProcessStep

@dataclass
class Stage(BaseData):
    # 公共
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    simulate_type: Optional[SimulateType] = field(default=None, metadata={"description": "模拟方式"})
    percent: float = field(init=False, default=0, metadata={'description': '当前阶段的完成率'})
    time: float = field(init=False, default=0, metadata={'description': '当前阶段的时间，单位：天'})
    timestep: float = field(init=False, default=0, metadata={'description': '时间步长，单位：天'})
    nr_step_num: int = field(init=False, default=0, metadata={'description': '本阶段牛顿迭代步数'})
    # 组分模型参数
    timestep_sn: int = field(init=False, default=0, metadata={'description': '时间步序号'})
    dp: float = field(init=False, default=0, metadata={'description': '时间步目标压力变化'})
    ds: float = field(init=False, default=0, metadata={'description': '时间步目标饱和度变化量'})
    dc: float = field(init=False, default=0, metadata={'description': '时间步目标溶解气油比、挥发油气比'})
    cfl: float = field(init=False, default=0, metadata={'description': '时间步收敛难易度'})
    process_steps: List[ProcessStep] = field(init=False, default_factory=list, metadata={'description': '当前阶段的迭代步骤'})
    max_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的最大均方误差'})
    avg_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的平均均方误差'})
    msw_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的MSW均方误差'})
    # 黑油模型参数
    oil: float = field(default=None, metadata={"description": "油压"})
    water: float = field(default=None, metadata={"description": "水压"})
    gas: float = field(default=None, metadata={"description": "气压"})

    @classmethod
    def from_block(cls, block_lines):
        if ListUtils.find(block_lines, 'Percent '):
            simulate_type = SimulateType.COMP
            return cls.__from_block_comp(block_lines, simulate_type)
        elif ListUtils.find(block_lines, '---  TIME '):
            simulate_type = SimulateType.BLK
            return cls.__from_block_blk(block_lines, simulate_type)
        return None

    def to_block(self):
        if self.simulate_type == SimulateType.COMP:
            return self.__to_block_comp()
        elif self.simulate_type == SimulateType.BLK:
            return self.__to_block_blk()
        return None

    @classmethod
    def __from_block_blk(cls, block_lines: List[str], simulate_type: SimulateType):
        block_lines = ListUtils.trim(block_lines)

        stage = cls(simulate_type=simulate_type)
        time_line = ListUtils.pick_line(block_lines, 'TIME =')
        stage.time = StringUtils.pick_number(time_line)

        timestep_line = ListUtils.pick_line(block_lines, 'TIMESTEP =')
        numbers = StringUtils.pick_numbers(timestep_line)
        stage.timestep = numbers[0]
        stage.nr_step_num = numbers[1]

        balance_line = ListUtils.pick_line(block_lines, 'MATERIAL BALANCE')
        numbers = StringUtils.pick_numbers(balance_line)
        stage.oil = numbers[0]
        stage.water = numbers[1]
        stage.gas = numbers[2]

        return stage

    def __to_block_blk(self) -> list[str]:
        lines = list()
        lines.append(f'---  TIME =      {self.time} DAYS')
        lines.append(f'      TIMESTEP =      {self.timestep} DAYS           {self.nr_step_num} NEWTON ITERATIONS')
        lines.append(f'      MATERIAL BALANCES : OIL  {self.oil}  WATER  {self.water}  GAS  {self.gas}')

        return lines

    @classmethod
    def __from_block_comp(cls, block_lines: List[str], simulate_type: SimulateType):
        stage = cls(simulate_type=simulate_type)

        if len(block_lines) >= 4:
            block_lines = ListUtils.trim(block_lines)

            first_line_values = StringUtils.pick_numbers(block_lines[0])
            stage.percent = first_line_values[0]/100
            stage.time = first_line_values[1]
            stage.timestep = first_line_values[2]
            stage.timestep_sn = first_line_values[3]

            end_map = {k: v for k, v in (item.split('=') for item in block_lines[-1].strip().split(' '))}
            stage.dp = StringUtils.to_value(end_map['DP'], float)
            stage.ds = StringUtils.to_value(end_map['DS'], float)
            stage.dc = StringUtils.to_value(end_map['DC'], float)
            stage.cfl = StringUtils.to_value(end_map['CFL'], float)

            second_to_last = [item.strip() for item in block_lines[-2].strip().split(' ') if item.strip() != '']
            stage.max_mbe_of_stage = StringUtils.to_value(second_to_last[0], float)
            stage.avg_mbe_of_stage = StringUtils.to_value(second_to_last[1], float)
            stage.msw_mbe_of_stage = StringUtils.to_value(second_to_last[2], float)

            block_lines = block_lines[2:-2]
            for line in block_lines:
                step = ProcessStep.from_text(line)
                stage.process_steps.append(step)
            stage.nr_step_num = len(stage.process_steps)

        return stage

    def __to_block_comp(self):
        lines = [f' Percent   {self.percent * 100}%  Time {self.time} DAY  DT {self.timestep} DAY  TStep {self.timestep_sn}',
                 ' NRStep        MAXMBE        AVGMBE        MSWMBE   Lin_itr']

        for step in self.process_steps:
            lines.append(step.to_text())

        lines.append(f'                  {self.max_mbe_of_stage}     {self.avg_mbe_of_stage}   {self.msw_mbe_of_stage}')
        lines.append(f' DP={self.dp} DS={self.ds} DC={self.dc} CFL={self.cfl}')

        return lines

if __name__ == '__main__':
    stage_comp = '''
 Percent   0.15%  Time 3 DAY  DT 0.7 DAY  TStep 14
 NRStep        MAXMBE        AVGMBE        MSWMBE   Lin_itr
     61      0.493904   0.000893267   0.000413943         8
     62       3.23041    0.00028123    0.00260284         7
     63      0.718315   3.05874e-05   1.05274e-05         6
     64      0.648658   1.46931e-06   3.41263e-07         6
     65     0.0176386   6.34713e-08    5.2575e-08         5
     66    0.00248242   1.21076e-08   9.09077e-09         5
           0.00130985   5.09723e-09   1.50634e-09
 DP=274.738 DS=0.099191 DC=0 CFL=220.947    
    '''

    stage_ = Stage.from_block(stage_comp.split('\n'))
    print('以下是组分模型：')
    print('\n'.join(stage_.to_block()))

    stage_blk = """
---  TIME =      2.000 DAYS
  TIMESTEP =      1.000 DAYS           2 NEWTON ITERATIONS
  MATERIAL BALANCES : OIL  1.00  WATER 10.00  GAS  1.00"""

    stage_ = Stage.from_block(stage_blk.split('\n'))
    print('\n以下是黑油模型：')
    print("\n".join(stage_.to_block()))