## 概要
特定Backlogプロジェクトの課題のうち
- 実行時刻から1週間以内に更新された
- 特定のステータスで
- 特定の種別である  

ものをTrelloの特定ボード・特定レーンでカード化する

## 実行環境
- LambdaFunction
  - Python3.8 

## 準備
- serverlessファイルの設定
```
$ cp serverless_sample.yml serverless.yml
$ vi serverless.yml
```

# 必要なモジュールのインストール
- pipでのインストール
```
pip install -t ./ -r requirements.txt
```

- Serverless Frameworkのインストール
```
npm install -g serverless
```
