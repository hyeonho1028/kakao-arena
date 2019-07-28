import warnings
warnings.filterwarnings(action='ignore')
import gc

print('train start\n')
print('preprocess1 start\n')
import preprocess.preprocess
print('preprocess2 start\n')
import preprocess.preprocess2
print('preprocess complete\n')

gc.collect()
print('createmarch model start\n')
import model.createmarch
print('mfmodel model start\n')
#import model.mfmodel
print('follow model start\n')
import model.followmodel
print('wrmodel start\n')
import model.wrmodel
print('train complete')
