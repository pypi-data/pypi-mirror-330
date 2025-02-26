# Programado por Freddy Alvarado - 2022/03/01
# freddy.alvarado.b1@gmail.com
#------------------------------------------------------------

from operator import index
from scipy import stats
from statistics import median
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import scipy.stats as scs

#------------------------------------------------------------
# FUCNIONES para el analisis exploratorio de datos
#------------------------------------------------------------

# Hacer este método privado

def __simetria(column):
  kurt = 0.00
  skew = 0.00
  kurt = stats.kurtosis(column)
  skew = stats.skew(column)
  return kurt, skew

def __graficosxy(df):
  df.plot(
      kind='line',
      subplots=True,
      layout =(8,3),
      figsize=(10,12)
  )
  plt.tight_layout()
  plt.show()
  
def __histograma(df):
  
  nrows = len(df.columns)
  npar = nrows%2
  if (npar==1):
    nrows+=1
  nrows = nrows//2
  nh = nrows * 3
  
    
  # Setting up the figure and axes
  fig, axs = plt.subplots(nrows, 2, figsize=(8,nh))
  plt.subplots_adjust(hspace=0.5,wspace=0.3)
  
  # Plotting data
  columns = df.columns

  for i, column in enumerate(columns):
        
        if(nrows==1):
           ax = axs[i]
        else:
           ax = axs[i//2, i%2]
        
        # Plot histogram and KDE
        ax = sns.histplot(df[column], kde=True, ax=ax, color='#b5b5ff', bins=15, line_kws={'linewidth': 1})
        try:
            ax.lines[0].set_color('darkblue')
        except:
            pass
            
        # Plot average
        mean_value = df[column].mean()
        std_value = df[column].std()
        ax.axvline(mean_value, color='r', linestyle='--')

        ax.set_title(f"Campo: {column} - Media: {mean_value:.2f}", fontsize=10)

        # Setting x and y labels
        ax.set_xlabel('')
        ax.set_ylabel("Frecuencia")


  plt.tight_layout()
  plt.show()

def __dispersion_index(df):
  
  nrows = len(df.columns)
  npar = nrows%2
  if (npar==1):
    nrows+=1
  nrows = nrows//2
  nh = nrows * 3
  ncols = len(df.columns)
   
  # Setting up the figure and axes
  fig, axs = plt.subplots(nrows, 2, figsize=(8,nh))
  plt.subplots_adjust(hspace=0.5,wspace=0.5)
  
  # Plotting data
  columns = df.columns

  for i, column_name in enumerate(columns):
               
      if(nrows==1):
           ax = axs[i]
      else:
           ax = axs[i//2, i%2]
                  
      row_index = i // ncols
      col_index = i % ncols

      ax.scatter(df.index, df[column_name])

      ax.set_title(column_name)
      # ax.set_xlabel('Index')
      ax.set_ylabel('Value')    


  plt.tight_layout()
  plt.show() 
 
def __areaTrazadoBoxPlot(qcol):
  # Setea el area de dibujo
  nw = 0
  nh = 0
  if (qcol==1):
     nw= 1.5
     nh= 4.5       
  elif (qcol > 1 and qcol<=3):
    nw= 3.5
    nh= 6
  elif (qcol > 3 and qcol<=5):
    nw= 8
    nh= 6
  elif (qcol > 5 and qcol<=8):
    nw= 14
    nh= 6
  elif (qcol > 8):
    nw= 18
    nh= 8

  plt.rcParams['figure.figsize']=(nw,nh)
  return (nw,nh)
  
def __boxplot(df, inputs):
    num_inputs = len(inputs)
    fig, axs = plt.subplots(1, num_inputs, figsize=__areaTrazadoBoxPlot(num_inputs))
    axs = np.array(axs)   
    len_mayor_longitud = len(max(inputs, key=len))
    rotar=False
    
    if (len_mayor_longitud>=12):
        rotar=True
    
    for i, (ax, curve) in enumerate(zip(axs.flat, inputs), 1):
        sns.boxplot(y=df[curve], ax=ax, color='cornflowerblue', showmeans=True,
                meanprops={"marker":"o",
                           "markerfacecolor":"white",
                           "markeredgecolor":"black",
                          "markersize":"10"},
               flierprops={'marker':'o',
                          'markerfacecolor':'darkgreen',
                          'markeredgecolor':'darkgreen'})
        if(rotar):
          ax.set_title(inputs[i-1], rotation=15)
        else:
           ax.set_title(inputs[i-1])
        ax.set_ylabel('')

    plt.subplots_adjust(hspace=0.15, wspace=1.25)
    plt.show()   

#------------------------------------------------------------
# EDA
#------------------------------------------------------------

def categorical(df,varint=False):
  
  import warnings 
  warnings.filterwarnings('ignore')
  from tabulate import tabulate
  from datetime import datetime
  
  if df.shape[1] < 1:
     print("El DataFrame debe tener al menos una variable.")
     return

  colCat = []
  oIndex = []
  
  # Sólo variables string o integer
  
  if (varint==True):
      for i in df.columns:
        if df[i].dtype.kind in {'O', 'i'}:
            colCat.append(i)
  else:
     for i in df.columns:
        if df[i].dtype.kind in 'O':
            colCat.append(i)

  # Convierte todas las variables a string
  df = df[colCat]          
  df = df.astype(str)

  # Calculo del numero de filas necesario basado en el numero de columnas categoricas
  num_col = 2  # Numero de columnas por fila en la grilla
  num_filas = np.ceil(len(colCat) / num_col).astype(int)

  # Crear una figura y un conjunto de subgraficos
  fig, axes = plt.subplots(num_filas, num_col, figsize=(8, 3*num_filas))

  # Aplanar el array de axes para facilitar su uso en un loop
  axes = axes.flatten()
 
  print('\033[1mANALISIS DE VALORES NULOS\033[0m')
  df_info = pd.DataFrame({'type': df.dtypes,
                        'nulos': df.isnull().sum(),
                        'no_nulos': df.notnull().sum()})
  table = tabulate(df_info, headers='keys', tablefmt='fancy_grid')
  print(table)
  print('') 
  

  print('')
  print('\033[1mMODA POR CATEGORIAS\033[0m')
  dfModas = df.mode().T
  dfModas['Moda'] = dfModas[0]
  table = tabulate(dfModas['Moda'],  tablefmt='fancy_grid')
  print(table)
  print('') 

  print('\033[1mGRAFICOS DE BARRAS\033[0m')
  print('')
  
  arrayFrecuencia = []
  tofile = False
  nRows = 0

  for i, columna in enumerate(colCat):
    # Contar la frecuencia de cada categoria en la columna actual
    frecuencia = df[columna].value_counts()
    arrayFrecuencia.append(frecuencia)
    
    # nRows debe ser igual al numero de filas de frecuencia
    nRows += len(frecuencia)

    # Crear el grafico de barras en el subplot correspondiente
    frecuencia.plot(kind='bar', ax=axes[i])
    axes[i].set_ylabel('Frecuencia')
    axes[i].set_xlabel('')
    axes[i].set_title(columna)
    
    # Verificar la cantidad de etiquetas del eje X
    if len(frecuencia) > 18:
        # Si hay mas de 18 etiquetas, ocultarlas porque se vuelve ilegible
        axes[i].set_xticklabels([])
    else:
        # Si hay 18 etiquetas o menos, rotarlas para mejor legibilidad
        axes[i].tick_params(axis='x', rotation=45)

  # Ocultar los axes adicionales si el numero de columnas categoricas no llena la ultima fila
  for j in range(i+1, num_filas * num_col):
    fig.delaxes(axes[j])
    
  plt.tight_layout()  # Ajustar automaticamente los parametros de la subtrama
  plt.show()
  
  print('')
  print('\033[1mTABLAS DE DATOS\033[0m')
  print('')
  
  if (nRows>=500):
     tofile = True
     
  if not(tofile):
     for i in arrayFrecuencia:
        print(tabulate(i.to_frame(), headers='keys', tablefmt='fancy_grid'))
        print('')
  else:    
     nombre_archivo = datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.txt'  
     print('Se obtuvieron Tablas extensas, los resultados se guardaron en el archivo: ', nombre_archivo)
     with open(nombre_archivo, 'w') as f:
        for i in arrayFrecuencia:
           f.write('\n')
           f.write(tabulate(i.to_frame(), headers='keys', tablefmt='simple'))
           f.write('\n')
     print('')
     
  
def continuos(df, varint=False ):
  import warnings 
  warnings.filterwarnings('ignore')
  from tabulate import tabulate
  
  if df.shape[1] < 1:
     print("El DataFrame debe tener al menos una variable.")
     return
  
  pd.set_option('display.float_format', lambda x: '%.3f' % x)
  oLista = []
  oIndex = []
  nCol = 0
  
  # Variables decimal o float
  colNum = []
  
  if (varint==True):
      for i in df.columns:
        # int, decimal o float
        if (df[i].dtype.kind in 'idf'):
            colNum.append(i)
  else:
      for i in df.columns:
        # decimal o float
        if (df[i].dtype.kind in 'df'):
            colNum.append(i)
        
  # Selecciona solo las columnas numericas
  df = df[colNum]

  for i in df.columns:

    nCol +=1
    describe = df[i].describe()

    for j in range(len(describe)):
        varNum = describe.iloc[j:j+1].values[0]
        describe[describe.index[j]] = '{:.5f}'.format(varNum)

    dk = stats.kurtosis(df[i])
    ds = stats.skew(df[i])
    dmedian = median(df[i])

    stat, p = scs.normaltest(df[i])

    describe['median']= '{:.5f}'.format(dmedian)
    describe['kurt']= '{:.5f}'.format(dk)
    describe['skew']= '{:.5f}'.format(ds)
    describe['test_stat']= '{:.5f}'.format(stat)
    describe['p-value']= '{:.5f}'.format(p)

    # H0, tiene dist normal
    # H1, no tiene dist normal
    if (float(p) < float(0.05)):
        # Se rechaza H0
        describe['dist-norm']= 'no'
    else:
        #Se acepta H0
        describe['dist-norm']= 'si'

    oLista.append(describe)
      # Indices
    oIndex.append(i)     
    #end if  
      
   #end for

  dfEstat = pd.DataFrame(oLista, index=oIndex)
  
  print('\033[1mANALISIS EXPLORATORIO DE DATOS PARA VARIABLES CONTINUAS\033[0m')
  print('')
  print('\033[1mESTADISTICOS DESCRIPTIVOS UNIVARIADOS\033[0m')
  table = tabulate(dfEstat.T, headers='keys', tablefmt='fancy_grid')
  print(table)
  print('')
  
  print('\033[1mANALISIS DE VALORES NULOS\033[0m')
  df_info = pd.DataFrame({'type': df.dtypes,
                        'nulos': df.isnull().sum(),
                        'no_nulos': df.notnull().sum()})
  
  table = tabulate(df_info, headers='keys', tablefmt='fancy_grid')
  print(table)

  plt.rcParams['figure.figsize']=(4,3)
  # Mapa de Calor
  sns.heatmap(df.isnull())
  plt.show()

  print('')
  print('\033[1mHISTOGRAMAS\033[0m')
  __histograma(df)
  
  print('')
  print('\033[1mGRAFICOS BOXPLOT\033[0m')
  __boxplot(df, df.columns)

  print('')
  print('\033[1mGRAFICOS DE DISPERSION\033[0m')
  __dispersion_index(df)

  print('')
  print('\033[1mGRAFICOS XY\033[0m')
  __graficosxy(df)
  plt.show()
  plt.rcParams['figure.figsize']=(6,6)

#------------------------------------------------------------
# ANALISIS BIVARIADO (solo variables numericas)
#------------------------------------------------------------

def bivariado(df):
  
  # Variables float64
  colNum = []
  for i in df.columns:
    if (df[i].dtype.kind in 'fi'):
        colNum.append(i)
        
  # Setea solo las columnas numericas
  df = df[colNum]

  print('\033[1mANALISIS BIVARIADO\033[0m')
  print('')
  dispersion(df)
  correlograma(df)

def dispersion(df):
  nrows = len(df.columns)
  nDim =0
  if (nrows<= 6 ):
    nDim = 10
  elif (nrows <= 12):
    nDim = 16
  else:
    nDim = 20
    
  print('\033[1mGRAFICOS DE DISPERSION POR CADA PAR DE CAMPOS\033[0m')
  # pairplot = sns.pairplot(df)  
  pairplot = sns.pairplot(df, height=nDim/len(df.columns))
  plt.gcf().set_size_inches(nDim, nDim)

  pairplot.fig.subplots_adjust(right=0.5, bottom=0.5)
  plt.show()
  
def correlograma(df):
  nrows = len(df.columns)
  nw =0
  nh=0
  if (nrows<= 6 ):
    nw = 4
    nh = 3
  elif (nrows <= 12):
    nw = 8
    nh = 6
  else:
    nw = 10
    nh = 8

  print('')
  print('\033[1mGRAFICO CORRELOGRAMA\033[0m')
  plt.rcParams['figure.figsize'] = (nw, nh)
  # Correlograma
  df_corr = df.corr()
  sns.heatmap(df_corr,
            xticklabels = df_corr.columns,
            yticklabels = df_corr.columns,
            cmap='coolwarm',
            annot=True)
  plt.show()
  #------------------------------------------------------------