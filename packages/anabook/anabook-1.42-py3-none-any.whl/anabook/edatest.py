# Programado por Freddy Alvarado - 2022/03/01
# freddy.alvarado.b1@gmail.com
#------------------------------------------------------------
import unittest
import pandas as pd
import eda as eda

class TestDescribe2(unittest.TestCase):
    def test_describe2(self):
        # Crear DataFrame de prueba
        data = {
            'A': [1.0, 2.0, 3.0, 4.0, 5.0,1.0,1.0,1.0],
            'B': [6.0, 7.0, 8.0, 9.0, 10.0,1.0,1.0,1.0],
            'C': [11.0, 12.0, 13.0, 14.0, 15.0,1.0,1.0,1.0],
            'D': [11.0, 12.0, 13.0, 14.0, 15.0,1.0,1.0,1.0],
            'E': [11.0, 2.0, 3.0, 12.0, 1.0,1.0,1.0,1.0],
            'F': [11.0, 1.0, 1.0, 1.0, 5.0,1.0,1.0,1.0],
            'G': [11.0, 2.0, 23.0, 4.0, 13.0,1.0,1.0,1.0],
            'H': [11.0, 10.0, 13.0, 10.0, 12.0,1.0,1.0,1.0]
            
        }
        df = pd.DataFrame(data)
        
        # Llamar a la función describe2
        eda.continuos(df)
        

if __name__ == '__main__':
    unittest.main()