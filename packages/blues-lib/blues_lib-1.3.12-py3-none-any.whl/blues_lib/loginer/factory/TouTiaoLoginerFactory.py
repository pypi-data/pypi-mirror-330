import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.factory.TouTiaoLoginerSchemaFactory import TouTiaoLoginerSchemaFactory
from loginer.factory.LoginerFactory import LoginerFactory
from loginer.OnceLoginer import OnceLoginer   
from loginer.PersistentLoginer import PersistentLoginer   
from loginer.form.MACLoginerForm import MACLoginerForm   

class TouTiaoLoginerFactory(LoginerFactory):

  def create_once_mac(self):
    factory = TouTiaoLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return OnceLoginer(schema,form)

  def create_persistent_mac(self):
    factory = TouTiaoLoginerSchemaFactory()
    schema = factory.create_mac()
    form = MACLoginerForm(schema)
    return PersistentLoginer(schema,form)




