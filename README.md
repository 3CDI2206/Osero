# Osero

## 実行方法

この作品は `main_menu.py` を起動して使用します。

以下のコマンドを実行してください：
python main_menu.py


## 実装上の工夫・ポイント

この作品では、以下の2点を自分で考えて実装しました。

### 1. 挟んで反転させる処理の実装

まずオセロでは、石を置いたときに相手の石を自分の石で挟むと、その間の石を自分の色に反転させる必要があります。

この処理を実現するために、以下の2つの関数に分けて実装しました。

#### ・check_direction(x, y, dx, dy, color)
指定された座標 (x, y) に石を置いたときに、方向 (dx, dy) に向かって見ていったときに、
その方向で「相手の石を自分の石で挟めるかどうか」を判定する関数です。

1マス進んで相手の石があればさらにその先へ進み、
最終的に自分の石が出てくるまで相手の石が続いていれば「挟める」とみなします。

#### ・flip_stones(x, y, dx, dy, color)
check_direction() で「挟める」と判定された方向に対して、
実際に相手の石を自分の石に反転させる処理を行います。

具体的には、(x, y) から (dx, dy) の方向に1マスずつ進みながら、
相手の石を自分の色に置き換えていきます。

#### ・place_stone(x, y, color)
上記2つの関数を使い、石を置いたときに8方向すべてに対して
「挟めるかチェック → 反転」を繰り返すようにしています。

このように、1方向ずつ分けて処理することで、ロジックが明確になり、動作のバグも発見しやすくなっています。


### 2. 勝敗の個数を数える処理
ゲーム終了時に、盤面上の石の数をカウントして勝敗を判定しています。
盤面は2次元リストで管理しており、`row.count(BLACK)` や `row.count(WHITE)` を使って行ごとに数え、
`sum()` で全体の合計を出すようにしています。

処理や考え方はこちら参考にしました。
https://daeudaeu.com/tkinter-othello/


### 3. AI対戦で初心者ボタンを3回押すと...
AI対戦で初心者ボタンを3回押すと...
