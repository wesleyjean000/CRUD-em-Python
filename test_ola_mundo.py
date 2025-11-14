import unittest
from ola_mundo import classificar_idade

class TesteClassificacaoIdade(unittest.TestCase):

    def test_classificar_crianca(self):
        
        self.assertEqual(classificar_idade(5), "criança")
        self.assertEqual(classificar_idade(12), "criança")

    def test_classificar_adolescente(self):
       
        self.assertEqual(classificar_idade(13), "adolescente")
        self.assertEqual(classificar_idade(17), "adolescente")

    def test_classificar_adulto(self):
        
        self.assertEqual(classificar_idade(18), "adulto")
        self.assertEqual(classificar_idade(50), "adulto")

    def test_limites_classificacao(self):
       
        self.assertEqual(classificar_idade(12), "criança", "A idade 12 deveria ser criança")
        self.assertEqual(classificar_idade(13), "adolescente", "A idade 13 deveria ser adolescente")
        self.assertEqual(classificar_idade(17), "adolescente", "A idade 17 deveria ser adolescente")
        self.assertEqual(classificar_idade(18), "adulto", "A idade 18 deveria ser adulto")

if __name__ == '__main__':
    unittest.main()