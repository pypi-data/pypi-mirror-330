import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO     

class AIHandleMaterial:

  def get_article(self,material_id=''):
    if material_id:
      conditions = [
        {'field':'material_id','comparator':'=','value':id}, # ifeng.com_8dZIWYbSBUs 
        {'field':'material_body_text','comparator':'!=','value':''}, 
      ]
      response = BluesMaterialIO.get('*',conditions)
    else:
      response = BluesMaterialIO.random()

    content = self.__get_material_content(response)
    if not content:
      BluesConsole.error('There are no available material : %s' % response)
    return content
  
  def __get_material_content(self,response):
    if not response['data']:
      return None

    ori_body_text = response['data'][0]['material_ori_body_text']
    body_text = response['data'][0]['material_body_text']

    text = ori_body_text if ori_body_text else body_text
    if not text:
      return None

    paras = json.loads(text)
    content = ''
    for para in paras:
      content+=para
    return content
    


