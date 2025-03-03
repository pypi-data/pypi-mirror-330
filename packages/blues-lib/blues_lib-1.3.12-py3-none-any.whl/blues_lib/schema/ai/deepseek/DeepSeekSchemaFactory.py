import sys,os,re,json
from .DeepSeekQASchema import DeepSeekQASchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AISchemaFactory import AISchemaFactory

class DeepSeekSchemaFactory(AISchemaFactory):

  def create_qa(self):
    return DeepSeekQASchema()
