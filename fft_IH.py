import numpy as np
from scipy import fftpack
import pandas as pd
import os
os.chdir('C://Users\Owner\Documents\Python Scripts\Data_set1')

import matplotlib.pyplot as plt

# フーリエ変換をする関数
def calc_fft(data, samplerate):
    spectrum = fftpack.fft(data)                                     # 信号のフーリエ変換
    amp = np.sqrt((spectrum.real ** 2) + (spectrum.imag ** 2))       # 振幅成分
    amp = amp / (len(data) / 2)                                      # 振幅成分の正規化（辻褄合わせ）
    phase = np.arctan2(spectrum.imag, spectrum.real)                 # 位相を計算
    phase = np.degrees(phase)                                        # 位相をラジアンから度に変換
    freq = np.linspace(0, samplerate, len(data))                     # 周波数軸を作成
    return spectrum, amp, phase, freq

# csvから列方向に順次フーリエ変換を行い保存する関数
def csv_fft(in_file, out_file):
    df = pd.read_csv(in_file, encoding='SHIFT-JIS')    # ファイル読み込み
    #dtつまり時間の１メモリつまり時間分解能、微分の幅
    dt = df.T.iloc[0,1]                                              # 時間刻み
    print("flamelate is {}sec".format(dt))
    # データフレームを初期化
    df_amp = pd.DataFrame()
    df_phase = pd.DataFrame()
    df_fft = pd.DataFrame()

    # 列方向に順次フーリエ変換（DFT）をするコード
    for i in range(len(df.T)-1):
        print("shape is".format(df.T))
        data = df.T.iloc[i+1]                                        # フーリエ変換するデータ列を抽出
        print("data is".format(data))
        spectrum, amp, phase, freq = calc_fft(data.values, 1/dt)     # フーリエ変換をする関数を実行(1/dtは１秒あたりにあるデータの個数)
        df_amp[df.columns[i+1] + '_amp'] = pd.Series(amp)            # 列名と共にデータフレームに振幅計算結果を追加
        df_phase[df.columns[i+1] + '_phase[deg]'] = pd.Series(phase) # 列名と共にデータフレームに位相計算結果を追加

    df_fft['freq[Hz]'] = pd.Series(freq)                             # 周波数軸を作成
    df_fft = df_fft.join(df_amp).join(df_phase)                      # 周波数・振幅・位相のデータフレームを結合
    df_fft = df_fft.iloc[range(int(len(df)/2) + 1),:]                # ナイキスト周波数でデータを切り捨て
    df_fft.to_csv(out_file)                                          # フーリエ変換の結果をcsvに保存

    return df, df_fft

# 関数を実行してcsvファイルをフーリエ変換するだけの関数を実行
df, df_fft = csv_fft(in_file='signals.csv', out_file='fft.csv')

# ここからグラフ描画-------------------------------------
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(121)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')
ax2 = fig.add_subplot(222)
ax2.yaxis.set_ticks_position('both')
ax2.xaxis.set_ticks_position('both')
ax3 = fig.add_subplot(224)
ax3.yaxis.set_ticks_position('both')
ax3.xaxis.set_ticks_position('both')

# 軸のラベルを設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Amplitude')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Phase[deg]')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Amplitude')

# スケールの設定をする。
ax2.set_yticks(np.arange(-180, 181, 90))
ax2.set_ylim(-180, 180)
#ax3.set_yscale('log')

# データプロットの準備とともに、ラベルと線の太さ、凡例の設置を行う。
size = len(df.T)-1
for i in range(size):
    ax1.plot(df.T.iloc[0], df.T.iloc[i+1], label=df.columns[i+1], lw=1)
    ax2.plot(df_fft.T.iloc[0], df_fft.T.iloc[i+size], label=df_fft.columns[i+size], lw=1)
    ax3.plot(df_fft.T.iloc[0], df_fft.T.iloc[i+1], label=df_fft.columns[i+1], lw=1)
ax1.legend()
#ax2.legend()
ax3.legend()

# レイアウト設定
fig.tight_layout()

# グラフを表示する。
plt.show()
plt.close()
# ---------------------------------------------------