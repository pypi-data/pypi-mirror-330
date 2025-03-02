class AIHandleQuestion():

  @classmethod
  def get_rewrite_q(cls,article,rule):
    '''
    param {str} article
    param {AIHandleRule} rule
    '''
    values = (rule.max_content_len,rule.max_title_len)
    q_list = [
      '按如下要求重写文章',
      '1.文章长度不超过%s字' % rule.max_content_len,
      '2.采用夸张演绎手法',
      '3.与原文相似度低于百分之二十',
      '4.提供一个夸张风格标题',
      '5.标题长度不超过%s字' % rule.max_title_len,
      '6.英文字母和符号算0.5个字符',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q

  @classmethod
  def get_comment_q(cls,article,rule):
    '''
    param {str} article
    param {AIHandleRule} rule
    '''
    values = (rule.max_content_len,rule.max_title_len)
    q_list = [
      '按如下要求发表评论',      
      '1.评论长度不超过%s字' % rule.max_content_len,
      '2.使用阴阳怪、负能量的语气',
      #'3.评论前先用一句话总结新闻（包括时间）',
      '3.每个段落长度不要超过200字',
      '4.提供一个评论标题',
      '5.标题长度不超过%s字' % rule.max_title_len,
      '6.英文字母和符号算0.5个字符',
      '文章如下',
    ]
    q = '，'.join(q_list)+'：'+article
    return q