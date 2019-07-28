# Description
<<<<<<< HEAD
```
​```bash
.
├── rawdata
│   ├── predict
│   │   └── test.users
│   ├── read
│   │   ├── 20181000100_2018...
│   │   └── ...
│   ├── magazine.json
│   ├── metadata.json
│   ├── users.json
│   ├── read_data_sort.csv(압축을 푸는 과정에서 파일 순서가 자동으로 섞이는데, 
│   │                       파일 순서를 보존하기 위해 sort를 저장했습니다.)
│   └── 0222_0301_1000_recommend.txt(카카오 기본 추천 파일)
├── pretrained
│   └── mf_test.csv
└── inference
​```
```



#### 0222_0301_1000_recommend.txt(카카오 기본 추천 파일)

```
$> python mostpopular.py --from-dtm 2019020100 --to-dtm 2019030100 recommend ./res/predict/dev.users recommend.txt

> https://github.com/kakao-arena/brunch-article-recommendation
```

   

#### mf_test.csv

```
mf model output

> https://www.kaggle.com/hyeonho/mf-based-popular
```





```
## **실행 방법**
​```bash
$> python train.py
$> python inference.py
​```
```



```
## **최종 결과물**
​```bash
inference/recommend.txt
​```
```



## 모델 설명

- popular
- sdf
- march model
- mf model
=======

*bug발견*

*1.0 주의 train 모델 중 tqdm을 사용한 부분들이 잦은 에러가 발견되므로 수정중에 있습니다.*


---
- 실행방법
0. python train.py
1. python inference.py
---
0. train.py가 실행된 후 생성되는 파일
   - 전처리파일들이 data/에 생성됩니다.
1. inference.py가 실행된 후 생성되는 파일
   - 최종 예측 파일으로서 data/inference/recommend.csv가 생성됩니다.
---
0. raw data 폴더에 json file을 넣습니다.
1. train.py file을 실행시킵니다.
2. inference.py file을 실행시킵니다.
---
![image](https://user-images.githubusercontent.com/40379485/61761597-211d8700-ae0a-11e9-8e10-773620df3c4b.png)
>>>>>>> 13df0e5a71134bfffeed2e5a1ee9394db402e93c
