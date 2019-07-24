# excute gawnghan
print('train 시작')


# excute hyeonho
print('preprocess 시작')
import preprocess.preprocess
print('preprocess 완료')
print('createmarch model 실행')
print('예상시간 : 10분')
import model.createmarch
print('createmarch model 완료')
print('mfmodel model 실행')
print('예상시간 : 5시간')
import model.mfmodel
print('train 완료')
