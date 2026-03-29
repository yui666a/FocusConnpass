# アーキテクチャルール

## レイヤー構成と依存方向

依存は常に外側→内側の一方向。内側のレイヤーは外側を知らない。

```
tools / infrastructure → usecase → domain
```

## domain/

- 標準ライブラリと pydantic のみ許可（他のサードパーティimport禁止）
- エンティティは pydantic.BaseModel で定義（frozen=True）
- リポジトリ・ゲートウェイは ABC で定義（具象実装を持たない）

## usecase/

- domain/ のみに依存する
- 具象クラス（ConnpassClient等）を直接importしない
- 入出力は dto/request.py, dto/response.py で定義（pydantic.BaseModel）

## infrastructure/

- usecase/ と domain/ に依存する
- api/: 外部API通信の実装
- dao/: ローカルデータアクセスの実装
- domain/ のABCを実装する

## tools/

- MCPツール定義（controller相当）
- UseCaseを呼び出し、結果を返す
- ビジネスロジックを持たない

## server.py

- DI組み立て（具象クラスのインスタンス化とUseCaseへの注入）
- FastMCPサーバーの起動
