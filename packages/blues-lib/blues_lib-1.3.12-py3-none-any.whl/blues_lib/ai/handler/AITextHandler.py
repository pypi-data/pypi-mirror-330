import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from ai.AIQAFactory import AIQAFactory
from ai.handler.AIHandleQuestion import AIHandleQuestion
from ai.handler.rule.AIHandleRuleFactory import AIHandleRuleFactory
from util.BluesConsole import BluesConsole

class AITextHandler():
  '''
  This class writer the input news
  '''
  
  def __init__(self,article,ai_name='doubao'):
    '''
    Paramters:
      ai {str} : The ai name 
    '''
    # {str}
    self.ai_name = ai_name
    # {str}
    self.article = article
    # {int}
    self.retry_count = 0

  def rewrite(self):
    self.retry_count = 0
    # {AIHandleRule}
    rule = AIHandleRuleFactory.create('rewrite')
    # {str} 
    question = AIHandleQuestion.get_rewrite_q(self.article,rule)
    # {AIQA}
    ai = AIQAFactory.create(self.ai_name,question)
    return self.__retry(ai,rule)
    
  def comment(self):
    self.retry_count = 0
    # {AIHandleRule}
    rule = AIHandleRuleFactory.create('comment')
    # {str} 
    question = AIHandleQuestion.get_comment_q(self.article,rule)
    # {AIQA}
    ai = AIQAFactory.create(self.ai_name,question)
    return self.__retry(ai,rule)
    
  def __console(self,response):
    stat = 'successful' if response else 'failure'
    BluesConsole.info('The qa was %s' % stat)

  def __retry(self,ai,rule,response=None):
    if rule.is_response_valid(response):
      self.__console(response)
      return response 

    if self.retry_count > rule.max_retry_count:
      self.__console(None)
      return None

    if self.retry_count>1:
      BluesConsole.info('The response is invalid, retry: %s' % self.retry_count)
    response = ai.execute()
    self.retry_count+=1
    return self.__retry(ai,rule,response)
