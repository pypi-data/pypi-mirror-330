import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from ai.AIQAResponse import AIQAResponse
from util.BluesConsole import BluesConsole

class AIHandleRule():

  def __init__(self,max_title_len=28,min_title_len=5,max_content_len=500,min_content_len=150,max_retry_count=3):
    self.max_title_len = max_content_len
    self.min_title_len = min_title_len
    self.max_content_len = max_content_len
    self.min_content_len = min_content_len
    self.max_retry_count = max_retry_count

  def is_response_valid(self,response) :
    type_error = self.__get_type_error(response)
    if type_error:
      BluesConsole.error(type_error)
      return False

    title_error = self.__get_len_error(response.title,self.max_title_len,self.min_title_len)
    if title_error:
      BluesConsole.error(title_error)
      return False

    '''
    content_error = self.__get_len_error(response.content,self.max_content_len,self.min_content_len)
    if content_error:
      BluesConsole.error(content_error)
      return False
    '''

    return True

  def __get_type_error(self,response):
    error = ''
    if not isinstance(response,AIQAResponse):
      error = 'The response is not a instance of AIQAResponse'
    return error
    
  def __get_len_error(self,text,max_len,min_len):
    error = ''
    text_len = self.__get_length(text)
    if text_len > max_len:
      error = 'The text exceeds the maximum length (%s/%s)' % (text_len,max_len)
    elif text_len < min_len:
      error = 'The text does not reach the minimum length (%s/%s)' % (text_len,min_len)
    return error
  
  def __get_length(self,text):
    length = 0
    for char in text:
      # 判断是否为中文字符（Unicode范围）
      if '\u4e00' <= char <= '\u9fff':
        length += 1
      # 非中文字符（包括英文、数字、标点符号等）
      else:
        length += 0.5
    return length