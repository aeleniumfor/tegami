# tegami

HTTPベースのシンプルなメッセージキュー

# 使い方

メッセージの登録

```bash
curl -X POST -H "Content-Type: application/json" -d '<JSONデータ>' <ホスト>/api/message
```

メッセージの取得

```bash
curl <ホスト>/api/message
```
