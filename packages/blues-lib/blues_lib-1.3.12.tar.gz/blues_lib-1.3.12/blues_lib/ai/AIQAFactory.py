from .DouBaoQA import DouBaoQA
from .DouBaoImgGen import DouBaoImgGen
from .DeepSeekQA import DeepSeekQA

class AIQAFactory():

  @classmethod
  def create(self,name,question):
    '''
    Get a AIQA instance
    param {str} name : the ai name
    param {str} question : the ai's input str
    '''
    if name == 'doubao':
      return DouBaoQA(question)
    elif name == 'doubao_img_gen':
      return DouBaoImgGen(question)
    elif name == 'deepseek':
      return DeepSeekQA(question)
    else:
      return DouBaoQA(question)