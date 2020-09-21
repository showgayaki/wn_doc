# wn_doc

## URL
https://wn-doc-2240.an.r.appspot.com/

## local実行
### 環境構築

`$ git clone https://github.com/showgayaki/wn_doc.git`

`$ cd wn_doc`

`$ python -m venv .venv`

(環境によっては`$ python3 -m venv .venv`)

`$ pip install -r requirements.txt`

(環境によっては`$ pip3 install -r requirements.txt`)


### local_settings.py
1. `settings.py`と同じディレクトリに`local_settings.py`を作成する。
2. `local_settings.py`に以下の内容を記載して保存する。

```
import os


DEBUG = True
os.environ['SECRET_KEY'] = 'secret_key'
os.environ['GITHUB_API_KEY'] = 'bearer github_api_key'
```
※注

secret_keyとgithub_api_keyを自身のものに置き換える。
- secret_keyは、[このあたり](https://qiita.com/frosty/items/bb5bc1553f452e5bb8ff)を参考に作成すれば大丈夫だと思う(実際にはやっていない)。
- github_api_keyは、[こちら](https://github.com/settings/tokens)からPersonal access tokenを作成([参考](https://qiita.com/yh1224/items/6705c2bb52ab917e4b45))。

### local実行
1. staticフォルダを、wn_doc/wn_docフォルダ直下にまるごとコピーする。
2. 仮想環境に入る
   - Windowsの場合：`$ .venv\Scripts\activate`
   - Macなどの場合：`$ source .venv/bin/activate`
3. `$ python manage.py runserver`

(環境によっては`$ python3 manage.py runserver`)

[http://127.0.0.1:8000](http://127.0.0.1:8000)にアクセスして表示されればOK。

## GAEにデプロイ
### env.yaml作成
以下の内容でenv.yamlを作成。

secret_key、github_api_keyは、local_settings.pyに記載したものと同じ。
```
env_variables:
  SECRET_KEY: 'secret_key'
  GITHUB_API_KEY: 'bearer github_api_key'
```

### clone
どうにかしてGCPに登録してプロジェクトを作成し、GAEを作成する。
1. GCPにログイン、該当のプロジェクトに移動し、Cloud Shellを起動する。
   ![cloud_shell](https://user-images.githubusercontent.com/47170845/93742419-0a024100-fc29-11ea-8670-0688fd6586db.png)
2. Cloud Shell上で、`$ git clone https://github.com/showgayaki/wn_doc.git`を実行


### env.yamlをアップロード
Cloud Shellが起動したら、app.yamlと同じディレクトリにenv.yamlをアップロードする。
![upload](https://user-images.githubusercontent.com/47170845/93742501-2bfbc380-fc29-11ea-86fc-57d35ef21b36.png)

### デプロイ
`$ gcloud app deploy`

で、デプロイ。

## ファイル更新時
staticファイル(cssとかjsとか)の編集は、コピーしたフォルダ(wn_doc/wn_doc/static)内のファイルを編集する。
編集が終わったら以下実行。

`$ python manage.py collectstatic`

(環境によっては`$ python3 manage.py collectstatic`)

あとは、addしてcommitしてpush。