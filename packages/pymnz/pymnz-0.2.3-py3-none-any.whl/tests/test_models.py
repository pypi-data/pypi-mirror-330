from pymnz.models import Script

def test_models_script():
  def soma(a, b):
    raise Exception('Teste de execução')

  try:
    script = Script('Script de teste', soma, a=1, b=2)
    script.code(1, 2)
    script.run(False)
  except Exception as e:
    assert str(e) == 'Teste de execução'
