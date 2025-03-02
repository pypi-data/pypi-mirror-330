from .AIHandleRule import AIHandleRule

class AIHandleRuleFactory(AIHandleRule):
  
  @classmethod
  def create(cls,scenario=''):
    if scenario == 'rewrite':
      return AIHandleRule(max_title_len=28,min_title_len=5,max_content_len=500,min_content_len=150,max_retry_count=3)
    elif scenario == 'comment':
      return AIHandleRule(max_title_len=28,min_title_len=5,max_content_len=500,min_content_len=150,max_retry_count=3)
    else:
      return AIHandleRule()
