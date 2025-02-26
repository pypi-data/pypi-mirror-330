import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from mag_tools.bean.base_data import BaseData
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat

from reservoir_info.model.grid_type import GridType


@dataclass
class PrimaryParams(BaseData):
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    number_of_grid: Optional[int] = field(init=False, default=None, metadata={'description': '网络数'})
    max_poro_vol: Optional[float] = field(init=False, default=None, metadata={'description': '最大poro值'})
    min_poro_vol: Optional[float] = field(init=False, default=None, metadata={'description': '最小poro值'})
    number_of_active_grid: Optional[int] = field(init=False, default=None, metadata={'description': '活动的网格数'})
    number_of_permeable_grid: Optional[int] = field(init=False, default=None, metadata={'description': '透水网络数'})
    grid_type: Optional[GridType] = field(init=False, default=None, metadata={'description': '网络类型'})
    length_of_tpfa: Optional[int] = field(init=False, default=None, metadata={'description': 'TPFA连接表大小'})
    nnc_of_tpfa: Optional[int] = field(init=False, default=None, metadata={'description': 'TPFA连接表NNC'})
    cost_of_tpfa: Optional[float] = field(init=False, default=None, metadata={'description': 'TPFA连接表构建时间'})
    number_of_wells: Optional[int] = field(init=False, default=None, metadata={'description': '井数'})
    number_of_branches: Optional[int] = field(init=False, default=None, metadata={'description': '分支数'})
    total_segments: Optional[int] = field(init=False, default=None, metadata={'description': '总井段数'})
    well_reservoir_connection_num : Optional[int] = field(init=False, default=None, metadata={'description': '油井到油藏连接数'})

    @classmethod
    def from_block(cls, block_lines: List[str]):
        clazz = cls()

        if len(block_lines) >= 6:
            map_ = cls.__block_to_map(block_lines)

            tpfa_value = ListUtils.pick_line(block_lines, 'Build TPFA connection')
            if tpfa_value:
                tpfa_map = cls.__get_tpfa(tpfa_value)
                map_['length_of_tpfa'] = tpfa_map.get('length')
                map_['nnc_of_tpfa'] = tpfa_map.get('nnc')
                map_['cost_of_tpfa'] = tpfa_map.get('cost')
                map_['grid_type'] = tpfa_map.get('grid_type')

            for key, value in map_.items():
                if hasattr(clazz, key):
                    field_type = cls.__annotations__[key]
                    if value and field_type in [Optional[int], Optional[float]]:
                        value = int(value) if field_type == Optional[int] else float(value)
                    setattr(clazz, key, value)

        return clazz

    def to_block(self):
        attribute_map = self.to_map
        if 'length_of_tpfa_connection_list' in attribute_map:
            attribute_map['Build TPFA connection list for Cartesian grid, length'] = attribute_map.pop('length_of_tpfa_connection_list')

        boundary = '----------------------------------------------------------------------'
        lines = [boundary,
                 StringFormat.pad_value('PRE-PROCESSING', len(boundary), JustifyType.CENTER),
                 f' Number of grid = {self.number_of_grid}; max poro vol = {self.max_poro_vol}; min poro vol = {self.min_poro_vol}',
                 f' Number of active grid = {self.number_of_active_grid}; number of permeable grid = {self.number_of_permeable_grid}',
                 f' Build TPFA connection list for {self.grid_type.code}, length = {self.length_of_tpfa} ({self.cost_of_tpfa} ms)',
                 f' Number of wells = {self.number_of_wells}, number of branches = {self.number_of_branches}, total segments = {self.total_segments}',
                 f' Number of well-to-reservoir connections = {self.well_reservoir_connection_num}',
                 boundary]

        return lines


    @classmethod
    def __block_to_map(cls, block: List[str]):
        map_ = {}
        for line in block:
            if '----------------' not in line and 'PRE-PROCESSING' not in line and 'Build TPFA connection' not in line:
                items = re.split(r'[;,]', line)
                for item in items:
                    if '=' in item:
                        key, value = item.split('=')
                        key = key.strip().replace(' ', '_').replace('-', '_').lower()
                        map_[key] = value.strip()
        return map_

    @classmethod
    def __get_tpfa(cls, s: str) -> dict:
        result = {}
        if 'CPG' in s:
            result['grid_type'] = GridType.CPG
        elif 'Cartesian' in s:
            result['grid_type'] = GridType.CARTESIAN
        elif 'GPG' in s:
            result['grid_type'] = GridType.GPG

        length_match = re.search(r'length\s*=\s*(\d+)', s)
        nnc_match = re.search(r'NNC\s*=\s*(\d+)', s)
        time_match = re.search(r'\(([\d.]+)\s*ms\)', s)

        if length_match:
            result['length'] = int(length_match.group(1))
        if nnc_match:
            result['NNC'] = int(nnc_match.group(1))
        if time_match:
            result['cost'] = float(time_match.group(1))

        return result

    def __to_tpfa(self):
        return f'{self.length_of_tpfa} ({self.cost_of_tpfa if self.cost_of_tpfa else ''})'


if __name__ == '__main__':
    # source_str = '''
# ----------------------------------------------------------------------
#                             PRE-PROCESSING
#  Number of grid = 2660; max poro vol = 85856.6; min poro vol = 1038.37
#  Number of active grid = 1761; number of permeable grid = 1761
#  Build TPFA connection list for CPG, length = 4713, NNC = 45 (0.3985 ms)
#  Number of wells = 5, number of branches = 5, total segments = 12
#  Number of well-to-reservoir connections = 12
# ----------------------------------------------------------------------
# '''
    source_str = '''
----------------------------------------------------------------------
                            PRE-PROCESSING
 Number of grid = 1122000; max poro vol = 35.6215; min poro vol = 7.1243e-05
 Number of active grid = 1094421; number of permeable grid = 1094421
 Build TPFA connection list for Cartesian grid, length = 3191860 (39.8693 ms)
 Number of wells = 5, number of branches = 5, total segments = 425
 Number of well-to-reservoir connections = 414
----------------------------------------------------------------------
'''
    pre_processing = PrimaryParams.from_block(source_str.split('\n'))

    block_ = pre_processing.to_block()
    print('\n'.join(block_))