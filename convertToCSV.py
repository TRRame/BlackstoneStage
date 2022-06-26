import pandas as pd

read_file = pd.read_csv (r'/home/tristan/Stage/EtudeLogiciels/ExplicationBlackstone/BordenvUSA/BordenvUSA_Kagan.txt')
read_file.to_csv (r'/home/tristan/Stage/EtudeLogiciels/ExplicationBlackstone/BordenvUSA/BordenvUSA_Kagan.csv', index=None)