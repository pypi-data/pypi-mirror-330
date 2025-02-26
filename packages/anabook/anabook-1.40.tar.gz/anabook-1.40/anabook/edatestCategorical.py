# Programado por Freddy Alvarado - 2022/03/01
# freddy.alvarado.b1@gmail.com
#------------------------------------------------------------
import random
import unittest
import pandas as pd
import eda as eda

class TestCategorical(unittest.TestCase):
    
    def test_categorical(self):
        
        # Definir los nombres de las variables categ�ricas
        variable_names = ['Cat' + str(i) for i in range(1, 9)]

        # Definir las categor�as posibles
        categories = ['A', 'B', 'C', 'D']
        

        # Generar datos categ�ricos aleatorios
        data = []
        for _ in range(100):
            data.append([random.choice(categories) for _ in range(8)])

        # Crear el DataFrame con los datos categ�ricos
        df = pd.DataFrame(data, columns=variable_names)

        eda.categorical(df,True)
        

if __name__ == '__main__':
    unittest.main()