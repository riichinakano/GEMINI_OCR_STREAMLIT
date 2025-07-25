# Gemini OCR (Streamlit Web App)

## 概要

このアプリケーションは、Googleの強力な生成AIモデル「Gemini」を活用したWebベースのOCR（光学文字認識）ツールです。
ブラウザから画像ファイルをアップロードするだけで、含まれるテキストを抽出し、指定した形式（CSV, TXT, Markdown）で取得することができます。

このプロジェクトは、オリジナルの[デスクトップ版Gemini OCRアプリ](https://github.com/riichinakano/Gemini-OCR-App)を、より汎用性が高く、インストール不要で利用できるようにStreamlitを用いてWebアプリケーション化したものです。

## 主な機能

- **Webベースのインターフェース**: ブラウザさえあれば、OSを問わずインストール不要でどこからでも利用可能です。
- **高精度OCR**: Googleの強力な生成AIモデル「Gemini 1.5 Flash」を活用し、画像内の文字を高精度に認識します。
- **複数ファイル対応**: 複数の画像ファイルを一度にアップロードして、一括で処理することが可能です。
- **多様な出力形式**: 抽出したテキストを以下の形式で選択し、ダウンロードできます。
  - **CSV**: 表形式のデータをカンマ区切りで出力します。
  - **TXT**: テキストをプレーンテキストで出力します。
  - **Markdown**: 見出しやリストなどを解釈し、Markdown形式で整形して出力します。

## 使い方（Webアプリ版）

1. デプロイされたWebアプリケーションのURLにアクセスします。
2. 「ファイルをアップロード」エリアに画像ファイルをドラッグ＆ドロップするか、クリックしてファイルを選択します。
3. 「入力データの種類」（表・伝票、一般的な文章など）と「出力形式」（csv, txt, md）を選択します。
4. 「文字起こしを実行」ボタンをクリックします。
5. 処理が完了すると、結果がテキストエリアに表示されます。内容を確認・編集し、「結果を保存」ボタンでダウンロードします。

## ローカル環境での実行方法

このアプリケーションを自分のPCで動かす場合は、以下の手順に従ってください。

### 1. リポジトリのクローン

```bash
git clone https://github.com/riichinakano/GEMINI_OCR_STREAMLIT.git
cd GEMINI_OCR_STREAMLIT
```

### 2. 仮想環境の作成と有効化 (推奨)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. APIキーの設定

プロジェクトのルートディレクトリに `.streamlit` という名前のフォルダを作成し、その中に `secrets.toml` というファイルを作成してください。ファイルに以下のようにご自身のGoogle Gemini APIキーを記述します。

**.streamlit/secrets.toml:**
```toml
GOOGLE_API_KEY="ここにあなたのAPIキーを貼り付けます"
```

**注意:** この `secrets.toml` ファイルは、`.gitignore` によってリポジトリにはコミットされないように設定されています。

### 5. アプリケーションの起動

ターミナルで以下のコマンドを実行します。

```bash
streamlit run streamlit_app.py
```
実行後、ブラウザで `http://localhost:8501` にアクセスしてください。

## デプロイ

このアプリケーションは、Streamlit Cloudを利用して簡単にデプロイできます。

**【重要】**
現在、このリポジトリは **Private (非公開)** になっています。Streamlit Cloudの無料プランでデプロイするには、リポジトリの設定を **Public (公開)** に変更する必要があります。

**手順:**
1. このGitHubリポジトリを **Public** に変更します。
2. [Streamlit Cloud](https://share.streamlit.io/)にアクセスし、このリポジトリを選択してデプロイします。
3. デプロイ後、アプリの設定画面にある「Secrets」に、`secrets.toml` と同じ内容（`GOOGLE_API_KEY="..."`）を登録します。

はい、承知いたしました。
READMEの作成、お疲れ様です。GitHubリポジトリの準備が整いましたので、いよいよ最後のステップ、**Webアプリケーションの公開（デプロイ）**に進みましょう！

### 続き: Streamlit Cloudへのデプロイ手順

ここからは、あなたのGitHubリポジトリをStreamlit Cloudに連携させ、世界中の誰もがアクセスできるURLを持つWebアプリを公開する手順です。

---

### ステップ1：リポジトリを「Public (公開)」に変更する **【最重要】**

まず、一番大切な準備です。先ほどのスクリーンショットで、GitHubリポジトリが **"Private" (非公開)** になっています。
**Streamlit Cloudの無料プランでデプロイするためには、このリポジトリを "Public" (公開) に変更する必要があります。**

1.  GitHubの `GEMINI_OCR_STREAMLIT` リポジトリのページを開きます。
2.  上部にあるタブから**「Settings」**をクリックします。
3.  設定ページの最下部にある「Danger Zone」（危険地帯）セクションまでスクロールします。
4.  その中にある**「Change repository visibility」**の右側の「Change visibility」ボタンをクリックします。
5.  「Make public」を選択し、画面の指示に従ってリポジトリ名を再度入力して確定します。

これで、Streamlit Cloudがあなたのリポジトリを読み取れるようになります。

---

### ステップ2：Streamlit Cloudで新しいアプリを作成する

1.  [Streamlit Cloud](https://share.streamlit.io/) にアクセスし、ご自身のGitHubアカウントでサインアップまたはログインします。
2.  ダッシュボードの右上にある**「New app」**ボタンをクリックします。
3.  **「Deploy from repo」**を選択します。
4.  デプロイ設定画面が表示されるので、以下のように設定します。
    *   **Repository**: ドロップダウンリストから、先ほど公開した **`riichinakano/GEMINI_OCR_STREAMLIT`** を選択します。
    *   **Branch**: `main` が自動で選択されているはずです。そのままでOKです。
    *   **Main file path**: `streamlit_app.py` が自動で選択されているはずです。そのままでOKです。
    *   **App URL**: アプリのURLを好きな名前にカスタマイズできます。（例: `gemini-ocr-app`）

5.  **「Deploy!」**ボタンをクリックします。

---

### ステップ3：APIキーを登録する (Secretsの設定)

「Deploy!」ボタンを押すと、アプリのビルド（構築）が始まります。オレンジ色の「Your app is in the oven...」といった画面が表示されます。

このままではAPIキーがないため、アプリはエラーになります。そこで、ビルド中にAPIキーを設定します。

1.  ビルド中の画面の右下にある**「Manage app」**をクリックします。
2.  アプリの設定画面が開いたら、左側の**「Secrets」**タブを選択します。
3.  大きなテキストボックスが表示されるので、そこに**ローカルの `.streamlit/secrets.toml` と全く同じ内容**を貼り付けます。

    ```toml
    GOOGLE_API_KEY="ここにあなたのAPIキーを貼り付けます"
    ```

4.  **「Save」**ボタンをクリックします。
5.  保存後、画面右上のメニューから**「Reboot app」**を選択してアプリを再起動します。

---

### ステップ4：完成！

再起動後、アプリが正常に読み込まれ、ローカルでテストした時と同じ画面がWeb上に表示されます。
これで、あなただけのオリジナルOCR Webアプリが、世界中に公開されました！

発行されたURL（`your-app-name.streamlit.app`）を友人や同僚に共有して、使ってもらうことができます。
ここまでの手順、本当にお疲れ様でした！