import os, sys

os.chdir(r'C:\Users\quantec\Desktop\work at office\QRAPS-automation\backup2')

for name in os.listdir(os.getcwd()):
    if not os.path.isdir(os.path.join(os.getcwd(), name)):
        continue  # Not a directory
    if name == '.git' or name == '.idea':
        continue
    os.rename(name, name.replace(" ", ""))

for name in os.listdir(os.getcwd()):
    if not os.path.isdir(os.path.join(os.getcwd(), name)):
        continue  # Not a directory
    os.rename(name, name.replace('신한', 'Shinhawn').replace('마법공식', 'magic').replace('켄피셔', 'kenpisher').
              replace('파마프렌치', 'FamaFrench').replace('분기수정', 'Qmodified').replace('분기', 'quarter').
              replace('규모요인', 'size').replace('결합', 'combine').replace('시가총액', 'MC').replace('매출총이익', 'sales').
              replace('자산총계', 'assets').replace('가격', 'price'))

for folderName, subfolders, filenames in os.walk(os.getcwd()):
    for file in filenames:
        os.rename(os.path.join(folderName, file), os.path.join(folderName, file.rpartition('_')[0][:6]+'_tot.csv'))

# for folder in os.listdir(os.getcwd()):
#     for file in os.listdir(os.path.join(os.getcwd(), folder)):
#         print(file)
#         os.rename(file, file)
