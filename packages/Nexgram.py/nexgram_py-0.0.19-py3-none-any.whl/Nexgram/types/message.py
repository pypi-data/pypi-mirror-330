class Message:
  def __init__(
    self,
    id: int,
    from_user,
    chat,
    text: str = None,
  ):
    pass
  def __str__(self):
    return json.dumps(self.__dict__)