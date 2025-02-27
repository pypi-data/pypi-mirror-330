from dataclasses import dataclass

from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.simulate.perform_statistics import PerformStatistics
from reservoir_info.model.simulate_type import SimulateType
from reservoir_info.bean.simulate.simulate_log import SimulateLog
from reservoir_info.bean.simulate.stage import Stage


@dataclass
class BlkLog(SimulateLog):
    @classmethod
    def from_block(cls, block_lines):
        log = cls(simulate_type=SimulateType.BLK)

        stages_lines = ListUtils.pick_tail(block_lines, '---  TIME =')
        if len(stages_lines) >= 10:
            stage_blocks = ListUtils.split_by_keyword(stages_lines, '---  TIME =')
            for stage_block in stage_blocks:
                stage = Stage.from_block(stage_block)
                log.stages.append(stage)

        log.performance_statistics = PerformStatistics(time_steps=len(log.stages), newton_steps=log.__get_nr_steps())

        return log

    def to_block(self) ->list[str]:
        lines = list()
        for stage in self.stages:
            lines.extend(stage.to_block())
            lines.append('')
        return lines

    def __get_nr_steps(self):
        step_num = 0
        for stage in self.stages:
            step_num += stage.nr_step_num
        return step_num

if __name__ == '__main__':
    data_file = 'D:\\HiSimPack\\data\\blk.log'
    with open(data_file, 'r') as f:
        lines_ = [line.strip() for line in f.readlines()]
        log_ = BlkLog.from_block(lines_)
        print('\n'.join(log_.to_block()))