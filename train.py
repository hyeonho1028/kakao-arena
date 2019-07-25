import warnings
warnings.filterwarnings(action='ignore')

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
