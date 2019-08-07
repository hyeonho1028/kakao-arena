# Description
#### path

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
│   ├── read_data_sort.csv(압축을 푸는 과정에서 파일 순서가 자동으로 섞이는데, 파일 순서를 보존하기 위해 sort를 저장했습니다.)
│   └── 0222_0301_1000_recommend.txt(카카오 기본 추천 파일)
├── pretrained
│   └── mf_test.csv
└── inference
​```
```



#### 0222_0301_1000_recommend.txt(카카오 기본 추천 파일)

```
$> python mostpopular.py --from-dtm 2019020100 --to-dtm 2019030100 recommend ./res/predict/dev.users recommend.txt -> 카카오에서 제공한 방법
$> python mostpopular.py —from-dtm 2019022200 —to-dtm 2019030100 recommend ./res/predict/dev.users recommend.txt -> using code
https://github.com/kakao-arena/brunch-article-recommendation
```

   

#### mf_test.csv(pre-trained model)

```
mf model output

https://www.kaggle.com/hyeonho/mf-based-popular
```





```
## **실행 방법**
​```bash
default directory
./kakao-arena/

$> python train1.py
$> python train2.py
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

- follow based popular
- article based model
- march focus model
- mf model
