import warnings
warnings.filterwarnings(action='ignore')
<<<<<<< HEAD
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
=======

print('train 시작\n')
print('preprocess1 시작\n')
import preprocess.preprocess
print('preprocess1 끝\npreprocess2 시작')
import preprocess.preprocess2
print('preprocess2 완료\n')

print('createmarch model 실행')
print('예상시간 : 10분')
import model.createmarch
print('createmarch model 완료')
print('mfmodel model 실행')
print('예상시간 : 5시간')
#import model.mfmodel
print('train 완료')
>>>>>>> 13df0e5a71134bfffeed2e5a1ee9394db402e93c
