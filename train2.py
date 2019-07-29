import warnings
warnings.filterwarnings(action='ignore')
import gc

gc.collect()
print('createmarch model start\n')
import model.createmarch
print('follow model start\n')
import model.followmodel
print('wrmodel start\n')
import model.wrmodel
print('train complete')
