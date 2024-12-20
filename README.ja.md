# nuitrack-touchdesigner-bridge

[Nuitrack SDK](https://github.com/3DiVi/nuitrack-sdk)を使用して取得したスケルトンデータをOSCプロトコルを介して送信するPythonスクリプトです。

## インストール

1. 必要なPythonパッケージをインストールします。

   ```bash
   pip install -r requirements.txt
   pip install [*.whl] # replace with filepath or URL for Nuitrack whl file

   # example
   # pip install https://github.com/3DiVi/nuitrack-sdk/raw/65662c9067a831c928e7300e427651e0dbe2ed9c/PythonNuitrack-beta/pip_packages/dist/windows/py_nuitrack_windows_python3.10-0.1.0-py3-none-any.whl
   ```

   whlファイルは[こちら](https://github.com/3DiVi/nuitrack-sdk/tree/master/PythonNuitrack-beta/pip_packages/dist)からダウンロードできます。

1. `.env.sample`ファイルをコピーして`.env`ファイルを作成し、必要な情報を入力します。

   ```bash
   cp .env.sample .env
   ```

   `.env`ファイルには以下の情報を含めます：

   ```
   REALSENSE_SERIAL_NUMBER="あなたのカメラのシリアル番号"
   NUITRACK_API_KEY="あなたのNuitrack APIキー"
   ```

## 使用方法

1. スクリプトを実行します。

   ```bash
   python nuitrack.py
   ```

1. デフォルトでは、すべての関節のデータを含んだOSCメッセージが`127.0.0.1:12345`に送信されます。  
必要に応じて、`-ip`,`-port`,`-j`オプションを使用して変更できます。  

   ```bash
   python nuitrack.py -ip 192.168.1.10 -port 9000 -j head neck left_hand
   ```

1. スクリプトを終了するには、`Ctrl+C`を押します。

## OSCメッセージの仕様

OSCメッセージは以下の形式で構成されています：

- **アドレスパターン**: `/p{user_id}/{joint_name}:{axis}`
  - `user_id`: スケルトンのユーザーID
  - `joint_name`: 関節の名前（例: `head`, `neck`, `left_hand`など）
  - `axis`: 座標軸（`tx`, `ty`, `tz`）

- **引数**: 各関節の位置データ（x, y, z座標）をメートル単位で送信します。

例:
```
/p1/head:tx 0.5
/p1/head:ty 1.2
/p1/head:tz 0.8
```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。

```
MIT License

Copyright (c) 2024 @nariakiiwatani, @funatsufumiya (Anno Lab. Inc.)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```