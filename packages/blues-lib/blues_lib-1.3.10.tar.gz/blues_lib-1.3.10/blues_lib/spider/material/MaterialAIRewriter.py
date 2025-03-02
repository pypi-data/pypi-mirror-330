import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from spider.crawler.CrawlerHandler import CrawlerHandler
from spider.deco.MaterialDeco import MaterialDeco
from ai.handler.AITextHandler import AITextHandler
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesURL import BluesURL 

class MaterialAIRewriter(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__rewrite(request)
    
  def __get_article(self,material):
    body_text = material.get('material_body_text')
    if not body_text:
      return None
    paras = json.loads(body_text)
    return ''.join(paras)

  def __rewrite(self,request):
    material = request.get('material')
    article = self.__get_article(material)
    if not article:
      return

    handler = AITextHandler(article,'doubao')
    # {AIQAResponse}
    response = handler.comment()

    if response:
      # save the original value to the ori field
      material['material_ori_title'] = material['material_title']
      material['material_ori_body_text'] = material['material_body_text']
      # use ai firstly
      material['material_title'] = response.title
      material['material_body_text'] = response.content
    else:
      # keep the columen as the same
      material['material_ori_title'] = ''
      material['material_ori_body_text'] = ''


