# Gemini OCR アプリケーション

Googleの生成AIモデル「Gemini」の強力な多モーダル機能を活用した、高機能OCR（光学文字認識）Webアプリケーションです。 Streamlitをフレームワークとして使用しています。

![アプリケーションのスクリーンショット](https://storage.googleapis.com/gemini-prod/images/84768393527a4192a6c891392631a0fe)
*(注: 上の画像パスはサンプルです。ご自身のスクリーンショット画像のパスに置き換えてください)*

## 概要

このアプリケーションは、ユーザーがアップロードした画像（請求書、文書、スクリーンショットなど）からテキストを抽出し、指定された形式（CSV, TXT, Markdown）で出力します。画像の特性（表、文章など）に合わせて最適化されたプロンプトを使用することで、高精度な文字起こしを実現します。

## 主な機能

- **複数ファイルのアップロード**: 複数の画像ファイル（PNG, JPG, BMP）を一度に処理できます。
- **柔軟な入力/出力設定**:
    - **入力の種類**: 「表・伝票」「一般的な文章」「レイアウト維持」から選択し、最適なOCR処理を実行します。
    - **出力形式**: 「CSV」「TXT」「Markdown」から目的に合った形式で結果を取得できます。
- **結果のプレビューと編集**: 抽出されたテキストをWeb画面上で直接確認し、必要に応じて編集できます。
- **結果のダウンロード**: 編集後のテキストを、指定した形式のファイルとしてダウンロードできます。（CSVはExcelでの文字化けを防ぐBOM付きUTF-8で出力）
- **Excel出力機能（NEW）**: Markdown形式でOCR実行時、テーブルを直接Excelファイル（xlsx）として保存できます。表・伝票のデータをExcelの集計表に転記する際に便利です。
- **モデルのカスタマイズ**: `gemini-2.5-flash` を使用していますが、コード内のモデル名を変更することで、他のGeminiファミリーモデルに切り替えることも可能です。

## 必要なもの

- Python 3.8 以降
- Google APIキー

## セットアップと実行方法

1.  **リポジトリをクローンします**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **必要なライブラリをインストールします**
    ```bash
    pip install -r requirements.txt
    ```

3.  **APIキーを設定します**
    プロジェクト内に `.streamlit` というディレクトリを作成し、その中に `secrets.toml` というファイルを作成します。ファイルに以下の内容を記述してください。

    ```toml
    # .streamlit/secrets.toml
    GOOGLE_API_KEY = "ここにあなたのGoogle APIキーを貼り付けてください"
    ```

4.  **Streamlitアプリケーションを起動します**
    ```bash
    streamlit run streamlit_app.py
    ```

5.  ブラウザで表示されたURL（通常は `http://localhost:8501`）にアクセスし、アプリケーションを使用します。

## 使用技術

- **バックエンド**: Python
- **AIモデル**: Google Gemini (`gemini-2.5-flash`)
- **Webフレームワーク**: Streamlit
- **ライブラリ**: `google-generativeai`, `Pillow`, `pandas`, `openpyxl`

## 使い方

1. 画像ファイル（PNG, JPG, BMP）をアップロード
2. 入力データの種類を選択（表・伝票、一般的な文章、レイアウト維持）
3. 出力形式を選択（CSV, TXT, MD）
4. 「文字起こしを実行」ボタンをクリック
5. 結果を確認・編集
6. ファイルとしてダウンロード
   - 選択した形式でダウンロード
   - **MD形式の場合**: Excelファイル（xlsx）としても保存可能