from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat


@dataclass
class ProcessStep:
    nr_step: Optional[int] = field(init=False, default=0, metadata={'description': '迭代步数序号'})
    max_mbe: float = field(init=False, default=0, metadata={'description': '最大均方误差'})
    avg_mbe: float = field(init=False, default=0, metadata={'description': '平均均方误差'})
    msw_mbe: float = field(init=False, default=0, metadata={'description': 'MSW均方误差'})
    stab_test: int = field(init=False, default=0, metadata={'description': '稳定性测试'})
    flash: int = field(init=False, default=0, metadata={'description': '闪蒸计算'})
    lin_itr: Optional[int] = field(init=False, default=0, metadata={'description': '线性求解次数'})

    @classmethod
    def from_text(cls, text: str, titles: List[str]):
        step = cls()
        values = text.split()

        if 'NRStep' in titles:
            step.nr_step = int(values[titles.index('NRStep')])
        if 'MAXMBE' in titles:
            step.max_mbe = float(values[titles.index('MAXMBE')])
        if 'AVGMBE' in titles:
            step.avg_mbe = float(values[titles.index('AVGMBE')])
        if 'MSWMBE' in titles:
            step.msw_mbe = float(values[titles.index('MSWMBE')])
        if 'StabTest/Flash' in titles:
            stab_test, flash = map(int, values[titles.index('StabTest/Flash')].split('/'))
            step.stab_test = stab_test
            step.flash = flash
        if 'Lin_itr' in titles:
            step.lin_itr = int(values[titles.index('Lin_itr')])
        return step

    def to_text(self) -> str:
        values = []
        if self.nr_step is not None:
            values.append(self.nr_step)
        if self.max_mbe is not None:
            values.append(self.max_mbe)
        if self.avg_mbe is not None:
            values.append(self.avg_mbe)
        if self.msw_mbe is not None:
            values.append(self.msw_mbe)
        if self.stab_test is not None:
            values.append(f'{self.stab_test}/{self.flash}')
        if self.lin_itr is not None:
            values.append(self.lin_itr)

        return StringFormat.pad_values(values, 13, JustifyType.RIGHT)