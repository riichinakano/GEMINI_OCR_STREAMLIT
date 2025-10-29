# Gemini OCR アプリ バージョンアップ実装指示書

## 概要
Streamlit製のGemini OCRアプリに、Markdown形式のOCR結果をExcelファイル（xlsx）として出力する機能を追加する。

## 現状
- 画像からOCR処理を行い、CSV/TXT/MD形式で出力可能
- 「表・伝票」タイプの画像をCSV出力するとカンマ区切りでズレが発生
- MD形式では正確にテーブルを認識できている
- 最終的にExcelの集計表に転記する必要がある

## 実装する機能
MD形式のOCR結果をExcelファイル（xlsx）として保存できるボタンを追加する。

### UI変更点
**場所**: 「4. 結果の確認・保存」セクション（streamlit_app.py 156-174行目）

**追加するボタン**:
- 既存のダウンロードボタン（168-174行目）の直後に配置
- ボタンラベル: 「Excelファイルとして保存」
- 表示条件: MD形式を選択した場合のみ表示（`st.session_state.output_format == 'md'`）

### 処理フロー
1. ユーザーが「Excelファイルとして保存」ボタンをクリック
2. テキストエリア（`st.session_state.result_text`）のMD内容を取得
   - このテキストエリアは159-164行目で定義されており、ユーザーが編集可能
3. MDテーブルをpandas DataFrameに変換
4. DataFrameをxlsx形式で出力
5. st.download_buttonでダウンロード提供

## 技術仕様

### 必要なライブラリ
```python
import pandas as pd
import io
from io import BytesIO
```

### MD → DataFrame 変換方法
Markdownのテーブルをpandasで読み込むには以下の方法を使用:
```python
# 方法1: pandasのread_csv with StringIO
df = pd.read_csv(io.StringIO(md_table_text), sep='|', skipinitialspace=True)

# 方法2: 手動パース（より確実）
lines = md_text.split('\n')
# テーブル部分を抽出してDataFrame化
```

### Excel出力方法
```python
# BytesIOを使用してメモリ上でExcelファイルを作成
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='OCR結果')
excel_data = output.getvalue()

# ダウンロードボタン
st.download_button(
    label="Excelファイルとして保存",
    data=excel_data,
    file_name="ocr_result.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
```

## 実装時の注意点

### 1. MD形式の判定
- ユーザーが選択した出力形式がMD以外の場合、Excelボタンを表示しない、または警告を表示
- `st.session_state.output_format == 'md'` で判定

### 2. テーブル検出
- MD内容に`|`で区切られたテーブルが含まれているか確認
- テーブルが見つからない場合はエラーメッセージを表示

### 3. ヘッダー行の処理
- MDテーブルの2行目（`|:-----|:-----|`のような区切り行）を除外
- 1行目をヘッダーとして扱う

### 4. データのクリーニング
- セルの前後の空白を削除（strip）
- 空の列を削除
- カンマ区切りの数値（例: 32,725）を適切に処理

### 5. 日本語対応
- openpyxlはデフォルトで日本語対応
- フォント設定は不要

## ファイル構成

### 修正対象ファイル
- `streamlit_app.py`: メインアプリケーションファイル

### 追加する関数（推奨）
```python
def md_table_to_dataframe(md_text):
    """
    Markdown形式のテーブルをpandas DataFrameに変換
    
    Args:
        md_text (str): Markdown形式のテキスト
        
    Returns:
        pd.DataFrame: 変換後のDataFrame
        None: テーブルが見つからない場合
    """
    # 実装内容
    pass

def create_excel_download_button(df, filename="ocr_result.xlsx"):
    """
    DataFrameからExcelファイルを生成してダウンロードボタンを表示
    
    Args:
        df (pd.DataFrame): 出力するDataFrame
        filename (str): ダウンロードファイル名
    """
    # 実装内容
    pass
```

## テストケース

### 1. 正常系
- MD形式のテーブルが正しくExcel化されること
- 日本語が文字化けしないこと
- 数値が正しく認識されること

### 2. 異常系
- MD形式以外を選択した場合の挙動
- テーブルが含まれないMDテキストの場合
- 空のテキストエリアの場合

## サンプルデータ
以下のMD形式データでテストを実施:

```markdown
| 椪番 | 品名 | 長さ | 径級一本数        | 本数 | 玉順 | 材積(m³) | 市売単価(円) | 売上金額(円) | 備考        |
|:-----|:-----|:-----|:------------------|-----:|:-----|---------:|-------------:|-------------:|:------------|
| 600  | 桧   | 3    | 16-4              | 4    |      | 0.308    | 15,000       | 4,620        | 買番:188    |
| 601  | 桧   | 3    | 16-25             | 25   |      | 1.925    | 17,000       | 32,725       | 買番:117    |
```

## 実装の優先順位
1. **HIGH**: MD → DataFrame変換関数の実装
2. **HIGH**: Excel出力ボタンの追加
3. **MEDIUM**: エラーハンドリング
4. **LOW**: UI改善（ボタンデザイン、配置など）

## 既存機能への影響
- 既存のCSV/TXT/MDダウンロード機能には影響しない
- セッションステートの使用方法は既存と同じ
- UI構造は最小限の変更

## 参考情報
- 現在使用しているモデル: `gemini-2.5-flash`
- Streamlitバージョン: 最新版を想定
- 必須ライブラリ追加: `requirements.txt`に`pandas`と`openpyxl`を追加
- 既存のダウンロードボタンは動的にラベルが変わる仕様（`結果を {format} ファイルとして保存`）

## 実装後の確認事項
- [ ] MD形式でOCR実行後、Excelボタンが表示される
- [ ] Excelボタンクリックでxlsxファイルがダウンロードできる
- [ ] Excelファイルを開いて表が正しく表示される
- [ ] 日本語が文字化けしていない
- [ ] 数値が適切にフォーマットされている
- [ ] 既存のMDダウンロード機能が正常に動作する

## 備考
- ユーザーは木材売上伝票のOCR処理を主な用途としている
- 最終的にExcelの集計表に転記するため、Excel出力は重要な機能
- CSV形式はカンマ区切りでズレが発生するため、MD経由のExcel出力が最適解
