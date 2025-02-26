import re


class NumberUtil:
  @staticmethod
  def find_percent(source:str, fallbackValue:int = 0) -> int:
    find = re.search(r'\d+%', source)
    return int(find.group().replace('%','')) if find is not None else fallbackValue
  
  @staticmethod
  def find_area(source:str) -> float:
    search = re.search(r'\d{0,}.\d+\s{0,1}(?=㎡)', source)
    return (float(search.group().replace(',','')), 0)[0]