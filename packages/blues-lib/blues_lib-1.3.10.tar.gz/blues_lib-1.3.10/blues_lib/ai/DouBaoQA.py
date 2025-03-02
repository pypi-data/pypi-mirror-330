import sys,os,re,json
from .AIQA import AIQA
from .AIQAResponse import AIQAResponse
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.DouBaoModelFactory import DouBaoModelFactory
from loginer.factory.DouBaoLoginerFactory import DouBaoLoginerFactory   
from util.BluesConsole import BluesConsole

class DouBaoQA(AIQA):
  
  def __init__(self,question):
    # { AIQASchema }
    material = {'question':question}
    model = DouBaoModelFactory().create_qa(material)
    # { Loginer } set loginer for relogin
    loginer = DouBaoLoginerFactory().create_persistent_mac()

    super().__init__(model,loginer)

  def extract(self,text):
    '''
    Extract format fields from the copied text
    '''
    # content is text copy from the clip board
    paras = self.__get_para_list(text)
    
    # the first line is the title
    title_para = paras.pop(0)
    title = self.__get_title(title_para)

    # content convert to json
    content = json.dumps(paras,ensure_ascii=False) if paras else ''

    return AIQAResponse(title,content)

  def __get_para_list(self,text):
    body = text.replace('"',"'")
    paras = re.split(r'[\n\r]', body)
    para_list = []
    for para in paras:
      text = para.strip()
      if text:
        para_list.append(text)
    return para_list

  def __get_title(self,title):
    patterns = [
      r'标题\s*[:：]?\s*(.+)', # 标题: xxx
      r'《(.+)》', # 标题：《xxx》
      r'\*+(.+)\*+', # **xxx**
    ]

    text = title
    for pattern in patterns:
      matches = re.findall(pattern,text)
      if matches:
        text = matches[0]

    # patter : ** xxx ** ; # xxxx
    return re.sub(r'[#*]', '', text).strip()

