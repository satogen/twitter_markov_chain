# Twitter のユーザのテキストからマルコフ連鎖を用いてテキストを生成するプログラム

## 実行方法

下記でテキストを呼び出し

```
$ python tweet.py
```

下記でテキストを生成するコマンド

```
$ python ./text_model/learn.py
```

## カスタマイズ

`tweet.py` の最終行こちらの第二引数を任意のものに変更

```
user_timeline_search(200, '@example')
```

`./text_model/learn.py` の beginning を任意のものにすることで特定の単語からテキストを生成できます。

```
start_text_model = text_model.make_sentence_with_start(beginning="example")
```
