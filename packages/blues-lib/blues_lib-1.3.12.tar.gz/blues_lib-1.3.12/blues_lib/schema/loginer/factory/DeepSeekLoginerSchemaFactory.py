import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.LoginerSchemaFactory import LoginerSchemaFactory
from schema.loginer.deepseek.DeepSeekAccountLoginerSchema import DeepSeekAccountLoginerSchema

class DeepSeekLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account(self):
    return DeepSeekAccountLoginerSchema()


