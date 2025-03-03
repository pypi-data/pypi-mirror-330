import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.DeepSeekLoginerSchemaFactory import DeepSeekLoginerSchemaFactory
from loginer.factory.LoginerFactory import LoginerFactory
from loginer.OnceLoginer import OnceLoginer   
from loginer.PersistentLoginer import PersistentLoginer   
from loginer.form.AccountLoginerForm import AccountLoginerForm   

class DeepSeekLoginerFactory(LoginerFactory):

  def create_once_account(self):
    factory = DeepSeekLoginerSchemaFactory()
    schema = factory.create_account()
    form = AccountLoginerForm(schema)
    return OnceLoginer(schema,form)

  def create_persistent_account(self):
    factory = DeepSeekLoginerSchemaFactory()
    schema = factory.create_account()
    form = AccountLoginerForm(schema)
    return PersistentLoginer(schema,form)




