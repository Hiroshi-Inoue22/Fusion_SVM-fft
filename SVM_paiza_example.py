import numpy as np
import librosa
import librosa.display
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import svm

speakers = {'kirishima' : 0, 'suzutsuki' : 1, 'belevskaya' : 2}

# 特徴量を返す
def get_feat(file_name):
  #aは振幅の数値の列(nnumpyの配列)、srはサンプリングレート /sごとの取る数
    a, sr = librosa.load(file_name)
    #ファイル内の最小サンプル数(周波数)に合わせる
    return a[0:5000]

# 特徴量と分類のラベル済みのラベルの組を返す
def get_data(dir_name):
    data_X = []
    data_y = []
    for file_name in sorted(os.listdir(path=dir_name)):
      #名前でいったん_として切り取るindexで_が入るまでを切り取り話者として代入
        speaker = file_name[0:file_name.index('_')]
        #dirnameとfile_nameを組み合わせプログラムファイルを個別に呼び出す。
        data_X.append(get_feat(os.path.join(dir_name, file_name)))
        '''
        辞書の中の名前と合致しているとkeyからvalue呼びだされて
        名前と合致した数値がdata_yに格納されて、その隣にファイルの名前が来る
        '''
        data_y.append((speakers[speaker], file_name))
#data_xには48人分で5000個の周波数、data_yには48人分、分類とファイル名が記録される
    return (np.array(data_X), np.array(data_y))

# 音声データを読み込む
print("read...")
data_X, data_y = get_data('voiceset')
print("done")

# 教師データとテストデータに分ける
train_X, test_X, train_y, test_y = train_test_split(data_X, data_y, random_state=11813)
#データの分割割合を確認
print("{}=>{},{}".format(len(data_x),len(train_x),len(test_x)))

# 学習させる
clf = svm.SVC(gamma =0.0001, C=1)
#yの0番目を'.T[0]'で呼び出して学習　つまりXの周波数とYの番号クラスを学習
clf.fit(train_X, train_y.T[0])

ok_count = 0

for X, y in zip(test_X, test_y):
    actual = clf.predict(np.array([X]))[0]
    #正解となるクラス番号(0~3)
    expected = y[0]
    file_name = y[1]
    ok_count += 1 if actual == expected else 0
    result = 'o' if actual == expected else 'x'
    print("{} file: {}, actual: {}, expected: {}".format(result, file_name, actual, expected))

print("{}/{}".format(ok_count, len(test_X)))

'''
os.listdir(path=dir_name)
この表記方法は、pathに埋め込んだあるディレクトリのパスを起点にその下にあるファイルを読み込むために使う https://note.nkmk.me/python-listdir-isfile-isdir/

上記のコードでは、voicesetディレクトリの中にあるwavファイルをos.listdirでpathによって指定されているディレクトリから開きソートして

index('~')
これは、' ~ 'が出てくる番号(n番目)の数字を取得するメソッドであり、上記のプログラムでは、＿より以前に声優に名前が書いてあるため[0:file_name.index('_')]で名前のを切り取りspeakerに代入できる。 これを上にあるspeakersの辞書型に登録されているkeyとして使いvalue(0~3)を格納する。

zipメソッド
Pythonの組み込み関数zip()は複数のイテラブルオブジェクト（リストやタプルなど）の要素をまとめる関数。forループで複数のリストの要素を取得する際などに使う。

標準ライブラリitertoolsモジュールのzip_longest()を使うと、それぞれのリストの要素数が異なる場合に、足りない要素を任意の値で埋めることができる。

zip_longest(names, ages, fillvalue=20):のように対応する数字がない場合には指定した数で埋めて対応付けられる。

[ ]

'''

names = ['Alice', 'Bob', 'Charlie']
ages = [24, 50, 18]

for name, age in zip(names, ages):
    print(name, age)

points = [100, 85, 90]

print('----------------')

for name, age, point in zip(names, ages, points):
    print(name, age, point)


from itertools import zip_longest

names = ['Alice', 'Bob', 'Charlie', 'Dave']
ages = [24, 50, 18]

for name, age in zip_longest(names, ages):
    print(name, age)