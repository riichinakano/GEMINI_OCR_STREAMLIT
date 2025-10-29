import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import pandas as pd
from io import BytesIO

# --- 定数設定 ---
MAX_TOTAL_SIZE_MB = 10
MAX_TOTAL_SIZE_BYTES = MAX_TOTAL_SIZE_MB * 1024 * 1024

# --- APIキー設定 ---
# Streamlit CloudのSecretsからAPIキーを読み込む
# ローカルでテストする際は、.streamlit/secrets.tomlから読み込まれる
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except (KeyError, AttributeError):
    st.error("エラー: GOOGLE_API_KEYが設定されていません。.streamlit/secrets.tomlファイルに設定してください。")
    st.stop()


# --- プロンプト定義 (ocr_app.pyから流用) ---
PROMPTS = {
    "table": {
        "csv": """あなたはプロのデータ入力担当者です。この画像に写っている表を、見たまま忠実にCSV形式で出力してください。

# 基本ルール
- 画像からヘッダー行を特定し、それをCSVの1行目としてください。
- すべてのデータ行は、必ずヘッダーの列数と同じ数のフィールドで構成してください。
- データがないセルは、空のフィールドとして扱い、列がずれないようにしてください。
- 数値に含まれる桁区切りのカンマは、除去して `10000` のように出力してください。
- 表のタイトルや合計行のような、純粋なデータ行ではないものは無視してください。
- 出力はCSVデータのみとし、前後の説明文は一切含めないでください。
""",
        "txt": "この画像は表データです。内容を認識し、人間が読みやすいように整形したテキストで書き出してください。",
        "md": "この画像は表データです。内容を認識し、Markdownのテーブル形式で整形して出力してください。"
    },
    "document": {
        "csv": "この画像は一般的な文章です。内容から主要なエンティティ（人名、地名、日付など）や要点を抽出し、それらをまとめたCSV形式で出力してください。",
        "txt": "この画像は一般的な文章です。内容を解釈し、段落などを整えたプレーンテキストとして書き出してください。",
        "md": "この画像は一般的な文章です。内容を、見出し、リスト、箇条書きなどを適切に解釈し、Markdown形式で整形して出力してください。"
    },
    "raw_text": {
        "csv": "この画像に含まれるテキストを、可能な限りCSVの1列目に全て書き出してください。",
        "txt": "この画像に含まれるテキストを、元の画像のレイアウトや改行を可能な限り忠実に再現したプレーンテキストで、そのまま全て書き出してください。",
        "md": "この画像に含まれるテキストを、元の画像のレイアウトを維持したまま、Markdownのコードブロック内に書き出してください。"
    }
}

# --- MD → DataFrame 変換関数 ---
def md_table_to_dataframe(md_text):
    """
    Markdown形式のテーブルをpandas DataFrameに変換

    Args:
        md_text (str): Markdown形式のテキスト

    Returns:
        pd.DataFrame: 変換後のDataFrame
        None: テーブルが見つからない場合
    """
    lines = md_text.strip().split('\n')

    # テーブル行を抽出（'|'で始まる行）
    table_lines = [line for line in lines if line.strip().startswith('|')]

    if len(table_lines) < 2:
        return None

    # ヘッダー行とデータ行を分離
    header_line = table_lines[0]
    # 2行目は区切り行（|:-----|:-----|）なので除外
    data_lines = table_lines[2:] if len(table_lines) > 2 else []

    # ヘッダーをパース
    headers = [cell.strip() for cell in header_line.split('|')[1:-1]]

    # データ行をパース
    data = []
    for line in data_lines:
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells:  # 空行を除外
            data.append(cells)

    if not data:
        return None

    # DataFrameを作成
    df = pd.DataFrame(data, columns=headers)

    # 空の列を削除
    df = df.loc[:, (df != '').any(axis=0)]

    return df


# --- Excel出力関数 ---
def create_excel_download_button(df, filename="ocr_result.xlsx"):
    """
    DataFrameからExcelファイルを生成してダウンロードボタンを表示

    Args:
        df (pd.DataFrame): 出力するDataFrame
        filename (str): ダウンロードファイル名
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='OCR結果')
    excel_data = output.getvalue()

    st.download_button(
        label="Excelファイルとして保存",
        data=excel_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# --- OCR処理のコア関数 (ocr_app.pyから流用・少し変更) ---
def get_ocr_result(image, data_type, output_format):
    prompt = PROMPTS.get(data_type, {}).get(output_format, "画像からテキストを抽出してください。")
    try:
        # モデル名を修正
        model_name = 'gemini-2.5-flash'  # ★ 使用するモデル名をここで定義
        model = genai.GenerativeModel(model_name)
        
        # --- 確認用コード ---
        st.info(f"使用中のモデル: {model_name}") # ← デバッグ用。開発時のみ有効化
        # --------------------

        img = image.convert("RGB")
        response = model.generate_content([prompt, img])
        
        cleaned_text = response.text.strip()
        # Markdownのコードブロック記号(` ``` `)が含まれていたら削除する
        if cleaned_text.startswith(f"```{output_format}"):
            cleaned_text = cleaned_text[len(f"```{output_format}"):].lstrip()
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:].lstrip()
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3].rstrip()
        return cleaned_text
    except Exception as e:
        st.error(f"APIエラーが発生しました: {e}")
        return None

# --- Streamlit UI部分 ---
st.set_page_config(page_title="Gemini OCR", page_icon="📄")
st.title("📄 Gemini OCR")
st.markdown("画像に含まれるテキストを抽出し、指定した形式で出力します。")

# --- Step 1: ファイル選択 ---
st.header("1. ファイルを選択 (複数可)")
uploaded_files = st.file_uploader(
    "PNG, JPG, BMP形式の画像ファイルを選択してください。",
    type=['png', 'jpg', 'jpeg', 'bmp'],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# --- 状態を保存するためにセッションステートを初期化 ---
if 'ocr_result' not in st.session_state:
    st.session_state.ocr_result = ""

# ファイルがアップロードされたら、UIの残りを表示
if uploaded_files:
    total_size = sum(file.size for file in uploaded_files)
    total_size_mb = total_size / (1024 * 1024)
    st.info(f"{len(uploaded_files)} 個のファイルを選択中 (合計: {total_size_mb:.2f} MB)")

    if total_size > MAX_TOTAL_SIZE_BYTES:
        st.warning(f"合計ファイルサイズが {MAX_TOTAL_SIZE_MB}MB を超えています。ファイルを減らしてください。")
        st.stop()

    # --- Step 2 & 3: 入力データと出力形式を選択 ---
    st.header("2. 入力と出力の形式を選択")
    col1, col2 = st.columns(2)
    with col1:
        data_type = st.radio(
            "入力データの種類",
            options=["table", "document", "raw_text"],
            format_func=lambda x: {"table": "表・伝票", "document": "一般的な文章", "raw_text": "レイアウト維持"}[x],
            key="data_type"
        )
    with col2:
        output_format = st.selectbox(
            "出力形式",
            options=["csv", "txt", "md"],
            key="output_format"
        )

    # --- 実行ボタン ---
    st.header("3. 実行")
    run_button = st.button("文字起こしを実行", type="primary", use_container_width=True)

    if run_button:
        all_results = []
        progress_bar = st.progress(0, text="処理を開始します...")

        with st.spinner("OCR処理を実行中です..."):
            for i, uploaded_file in enumerate(uploaded_files):
                progress_text = f"処理中: {uploaded_file.name} ({i+1}/{len(uploaded_files)})"
                progress_bar.progress((i + 1) / len(uploaded_files), text=progress_text)
                
                image = Image.open(uploaded_file)
                result_text = get_ocr_result(image, data_type, output_format)
                
                if result_text is not None:
                    # 複数ファイルの場合、ファイル名の区切りを入れる
                    if len(uploaded_files) > 1:
                        header = f"--- OCR Result for: {os.path.basename(uploaded_file.name)} ---\n\n"
                        all_results.append(header)
                    
                    all_results.append(result_text + "\n\n")

        # 処理完了後の表示
        progress_bar.empty()
        if all_results:
             st.success(f"成功！ {len(uploaded_files)}個のファイルを処理しました。")
             st.session_state.ocr_result = "".join(all_results) # 結果をセッションステートに保存
        else:
             st.warning("処理が完了しましたが、テキストを抽出できませんでした。")
             st.session_state.ocr_result = ""


# --- Step 4: 結果の確認・ダウンロード ---
if st.session_state.ocr_result:
    st.header("4. 結果の確認・保存")
    
    st.text_area(
        "抽出結果（編集可能）",
        value=st.session_state.ocr_result,
        height=400,
        key="result_text"
    )
    
    # ダウンロードボタンのファイル形式を動的に変更
    download_format = st.session_state.get('output_format', 'txt')
    st.download_button(
        label=f"結果を {download_format.upper()} ファイルとして保存",
        data=st.session_state.ocr_result.encode('utf-8-sig'), # BOM付きUTF-8でExcelでの文字化けを防ぐ
        file_name=f"ocr_result.{download_format}",
        mime=f"text/{download_format}",
        use_container_width=True
    )

    # MD形式の場合、Excelダウンロードボタンを追加
    if st.session_state.get('output_format') == 'md':
        md_text = st.session_state.get('result_text', '')

        if md_text:
            df = md_table_to_dataframe(md_text)

            if df is not None and not df.empty:
                create_excel_download_button(df)
            else:
                st.warning("Markdown形式のテーブルが見つかりませんでした。Excelファイルとして保存するには、テーブル形式（| 列1 | 列2 |）のデータが必要です。")
else:
    st.info("↑ 上のボックスから画像ファイルをアップロードし、「文字起こしを実行」ボタンを押してください。")