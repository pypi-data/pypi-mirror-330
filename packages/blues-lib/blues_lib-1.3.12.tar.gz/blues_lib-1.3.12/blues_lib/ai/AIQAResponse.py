import json

class AIQAResponse:

  def __init__(self,title,content):
    # {str}
    self.title = title if title else ''
    # {str}
    self.content = content if content else ''
    
  def to_string(self):
    entity = {
      'title':self.title,
      'content':self.content,
    }
    return json.dumps(entity,ensure_ascii=False) 