class SomeFns():
  @staticmethod
  def testFunction():
    return 'hello'
"""
pytest-mock is a plugin provides a 'mocker' fixture 
which is a thin-wrapper around the patching API provided by the mock package:
"""
def test_mocking_constant(mocker):
  # import pdb; pdb.set_trace()
  mocker.patch.object(SomeFns, 'testFunction', return_value='hello2')
  assert SomeFns.testFunction() == 'hello2'
