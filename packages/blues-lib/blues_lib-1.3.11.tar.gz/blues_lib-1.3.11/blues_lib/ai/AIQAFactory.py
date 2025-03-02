from .DouBaoQA import DouBaoQA
from .DouBaoImgGen import DouBaoImgGen

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
    else:
      return DouBaoQA(question)