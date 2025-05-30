# 画像処理テストツールキット

JPEGとPNG形式の包括的なバリエーション画像を生成し、画像変換ツールの品質評価を行うためのPythonツールキットです。

## 📋 目次

- [プロジェクトの目的](#プロジェクトの目的)
- [機能概要](#機能概要)
- [セットアップ](#セットアップ)
- [基本的な使い方](#基本的な使い方)
- [詳細な使用方法](#詳細な使用方法)
- [生成される画像バリエーション](#生成される画像バリエーション)
- [開発者向け情報](#開発者向け情報)
- [ライセンス](#ライセンス)

## 🎯 プロジェクトの目的

このツールキットは、**画像変換ライブラリやツールの品質評価**を目的として開発されました。

### 主な用途

- **画像変換ツールの性能評価**: 異なる変換ツール間での品質比較
- **回帰テスト**: 変換ツールのアップデート時の品質維持確認  
- **形式適合性検証**: 生成された画像が仕様を満たしているかの自動検証
- **研究・開発**: 画像処理アルゴリズムの研究用テストデータ作成

### 解決する課題

- 多様な画像形式バリエーションの手動作成が困難
- 画像変換品質の客観的評価が難しい
- 大量の画像処理における品質管理の自動化が必要

## ✨ 機能概要

### 🔧 主要機能

1. **元画像生成**: JPEG・PNG形式の理想的なテスト画像を生成
2. **バリエーション作成**: 56種類の異なる形式バリエーションを自動生成
3. **画像比較**: ディレクトリ間での画像品質比較（PSNR・SSIM計算）
4. **仕様適合性検証**: 生成画像が期待する仕様を満たすかの自動検証

### 📊 対応形式

- **JPEG**: 25種類のバリエーション（色空間、品質、エンコーディング、メタデータ等）
- **PNG**: 33種類のバリエーション（色タイプ、ビット深度、透明度、圧縮等）

## 🛠️ セットアップ

### 必要な環境

- **Python**: 3.8以上
- **ImageMagick**: 画像変換処理に必要
- **OS**: Windows、macOS、Linux対応

### 1. Pythonの確認

```bash
python --version
# または
python3 --version
```

Python 3.8以上がインストールされていることを確認してください。

### 2. ImageMagickのインストール

**macOS (Homebrew使用):**
```bash
brew install imagemagick
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install imagemagick
```

**Windows:**
[ImageMagick公式サイト](https://imagemagick.org/script/download.php#windows)からダウンロードしてインストール

### 3. プロジェクトのダウンロード

```bash
# GitHubからクローン（例）
git clone <リポジトリURL>
cd py-test-image-toolkit

# または、ZIPファイルをダウンロードして解凍
```

### 4. Python依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. インストール確認

```bash
python toolkit.py --help
```

正常にヘルプが表示されれば準備完了です。

## 🚀 基本的な使い方

### ステップ1: 元画像の生成

```bash
python toolkit.py generate-original --test-compliance
```

**実行結果:**
- `output/test_original.jpg` - JPEG テスト画像
- `output/test_original.png` - PNG テスト画像

### ステップ2: バリエーション画像の生成

```bash
python toolkit.py generate-variations --test-compliance
```

**実行結果:**
- `output/jpeg/` - 25種類のJPEGバリエーション
- `output/png/` - 33種類のPNGバリエーション

### ステップ3: 画像の比較

```bash
# 同一ディレクトリの比較例
python toolkit.py compare-directories output/jpeg output/png

# CSV形式で結果保存
python toolkit.py compare-directories output/jpeg output/png --output-format csv --output-file comparison.csv
```

### ステップ4: 仕様適合性の検証

```bash
python toolkit.py validate-variations --report-file validation_report.json
```

**実行結果:**
- コンソールに検証結果表示
- `validation_report.json` - 詳細な検証レポート

## 📚 詳細な使用方法

### コマンドライン オプション

#### `generate-original` - 元画像生成

```bash
python toolkit.py generate-original [オプション]
```

**オプション:**
- `--test-compliance`: 生成画像の仕様適合性をテスト
- `--output-dir DIR`: 出力ディレクトリ（デフォルト: output）

#### `generate-variations` - バリエーション生成

```bash
python toolkit.py generate-variations [オプション]
```

**オプション:**
- `--source-dir DIR`: 元画像ディレクトリ（デフォルト: output）
- `--output-dir DIR`: 出力ディレクトリ（デフォルト: output）
- `--test-compliance`: 生成バリエーションの仕様適合性をテスト

#### `compare-directories` - ディレクトリ比較

```bash
python toolkit.py compare-directories DIR_A DIR_B [オプション]
```

**オプション:**
- `--output-format {table,json,csv}`: 出力形式（デフォルト: table）
- `--output-file FILE`: 結果をファイルに保存

#### `validate-variations` - 仕様適合性検証

```bash
python toolkit.py validate-variations [オプション]
```

**オプション:**
- `--output-dir DIR`: 検証対象ディレクトリ（デフォルト: output）
- `--report-file FILE`: 検証レポートをファイルに保存

### 実用的な使用例

#### 例1: 画像変換ツールの評価

```bash
# 1. テスト画像を生成
python toolkit.py generate-original

# 2. 変換ツールAで変換
your-conversion-tool-a output/ converted_a/

# 3. 変換ツールBで変換  
your-conversion-tool-b output/ converted_b/

# 4. 品質比較
python toolkit.py compare-directories output converted_a --output-file tool_a_quality.csv
python toolkit.py compare-directories output converted_b --output-file tool_b_quality.csv
python toolkit.py compare-directories converted_a converted_b --output-file a_vs_b.csv
```

#### 例2: バッチ処理の品質管理

```bash
# 1. バリエーション画像を生成
python toolkit.py generate-variations

# 2. バッチ処理を実行
your-batch-processor output/jpeg processed_jpeg/

# 3. 処理結果の検証
python toolkit.py compare-directories output/jpeg processed_jpeg --output-format json --output-file batch_quality_report.json
```

## 📋 生成される画像バリエーション

### JPEG バリエーション (25種類)

| カテゴリ | ファイル名 | 説明 |
|----------|------------|------|
| **色空間** | `colorspace_rgb.jpg` | RGB色空間 |
| | `colorspace_cmyk.jpg` | CMYK色空間 |
| | `colorspace_grayscale.jpg` | グレースケール |
| **品質** | `quality_20.jpg` | 低品質（高圧縮） |
| | `quality_50.jpg` | 中品質 |
| | `quality_80.jpg` | 高品質 |
| | `quality_95.jpg` | 最高品質 |
| **エンコーディング** | `encoding_baseline.jpg` | ベースラインJPEG |
| | `encoding_progressive.jpg` | プログレッシブJPEG |
| **サブサンプリング** | `subsampling_444.jpg` | 4:4:4（高品質） |
| | `subsampling_422.jpg` | 4:2:2（中品質） |
| | `subsampling_420.jpg` | 4:2:0（圧縮優先） |
| **メタデータ** | `metadata_none.jpg` | メタデータなし |
| | `metadata_basic_exif.jpg` | 基本EXIF |
| | `metadata_gps.jpg` | GPS情報付き |
| | `metadata_full_exif.jpg` | 完全EXIF |
| **ICCプロファイル** | `icc_none.jpg` | プロファイルなし |
| | `icc_srgb.jpg` | sRGBプロファイル |
| | `icc_adobergb.jpg` | Adobe RGBプロファイル |
| **サムネイル** | `thumbnail_none.jpg` | サムネイルなし |
| | `thumbnail_embedded.jpg` | 埋め込みサムネイル |
| **複合パターン** | `critical_cmyk_lowquality.jpg` | CMYK + 低品質 |
| | `critical_progressive_fullmeta.jpg` | プログレッシブ + 完全メタデータ |
| | `critical_thumbnail_progressive.jpg` | サムネイル + プログレッシブ |

### PNG バリエーション (33種類)

| カテゴリ | ファイル名 | 説明 |
|----------|------------|------|
| **色タイプ** | `colortype_grayscale.png` | グレースケール |
| | `colortype_palette.png` | パレット色 |
| | `colortype_rgb.png` | RGB（透明度なし） |
| | `colortype_rgba.png` | RGBA（透明度あり） |
| | `colortype_grayscale_alpha.png` | グレースケール + 透明度 |
| **ビット深度** | `depth_1bit.png` | 1ビット（白黒） |
| | `depth_8bit.png` | 8ビット（標準） |
| | `depth_16bit.png` | 16ビット（高精度） |
| **圧縮レベル** | `compression_0.png` | 無圧縮 |
| | `compression_6.png` | 標準圧縮 |
| | `compression_9.png` | 最大圧縮 |
| **透明度** | `alpha_opaque.png` | 不透明 |
| | `alpha_semitransparent.png` | 半透明 |
| | `alpha_transparent.png` | 透明領域あり |
| **インターレース** | `interlace_none.png` | 通常 |
| | `interlace_adam7.png` | Adam7インターレース |
| **フィルタータイプ** | `filter_none.png` | フィルターなし |
| | `filter_sub.png` | Subフィルター |
| | `filter_up.png` | Upフィルター |
| | `filter_average.png` | Averageフィルター |
| | `filter_paeth.png` | Paethフィルター |
| **メタデータ** | `metadata_none.png` | メタデータなし |
| | `metadata_text.png` | テキストチャンク |
| | `metadata_compressed.png` | 圧縮テキスト |
| | `metadata_international.png` | 国際化テキスト |
| **補助チャンク** | `chunk_gamma.png` | ガンマ補正 |
| | `chunk_background.png` | 背景色指定 |
| | `chunk_transparency.png` | 透明色指定 |
| **複合パターン** | `critical_16bit_palette.png` | 16ビット → パレット変換 |
| | `critical_alpha_grayscale.png` | RGBA → グレースケール変換 |
| | `critical_maxcompression_paeth.png` | 最大圧縮 + Paethフィルター |
| | `critical_interlace_highres.png` | インターレース + 高解像度 |

## 🔍 比較・分析機能

### 出力される指標

| 指標 | 説明 | 値の範囲 | 判断基準 |
|------|------|----------|----------|
| **ファイルサイズ** | バイト単位のファイルサイズ | - | 圧縮効率の指標 |
| **サイズ比率** | サイズの比率 | 1.0 = 同じ | 圧縮率の変化 |
| **解像度** | 画像の幅×高さ | width×height | 解像度の維持確認 |
| **PSNR** | 画質劣化指標（高いほど良い） | 20-50dB (∞=同一) | >40dB: 高品質<br>30-40dB: 中品質<br><30dB: 低品質 |
| **SSIM** | 構造類似度（高いほど良い） | 0.0-1.0 (1.0=完全一致) | >0.95: 非常に類似<br>0.8-0.95: 類似<br><0.8: 異なる |

### レポート形式

#### テーブル形式（コンソール表示）
```
================================================================================
IMAGE COMPARISON REPORT
================================================================================
Directory A: output/jpeg (25 files)
Directory B: converted_jpeg (25 files)
Common files: 25

DETAILED COMPARISON
--------------------------------------------------------------------------------
Filename                       Size A     Size B     Ratio    PSNR     SSIM    
--------------------------------------------------------------------------------
quality_80.jpg                 209.2KB    195.4KB    0.93     38.5     0.952
quality_95.jpg                 561.8KB    523.1KB    0.93     42.1     0.978
...
```

#### JSON形式（プログラム処理用）
```json
{
  "summary": {
    "total_tested": 25,
    "total_passed": 24,
    "success_rate": 96.0
  },
  "detailed_results": [
    {
      "filename": "quality_80.jpg",
      "size_a": 214297,
      "size_b": 200123,
      "psnr": 38.5,
      "ssim": 0.952
    }
  ]
}
```

## 👨‍💻 開発者向け情報

### プロジェクト構造

```
py-test-image-toolkit/
├── toolkit.py              # メインエントリーポイント
├── requirements.txt         # Python依存関係
├── README.md               # このファイル
├── LICENSE                 # MITライセンス
├── src/                    # ソースコード
│   ├── __init__.py
│   ├── image_generator.py   # 元画像生成
│   ├── variation_generator.py # バリエーション生成
│   ├── image_comparator.py  # 画像比較・分析
│   ├── variation_validator.py # 仕様適合性検証
│   └── utils.py            # 共通ユーティリティ
├── tests/                  # テストコード
└── output/                 # 生成画像出力先
    ├── jpeg/               # JPEGバリエーション
    └── png/                # PNGバリエーション
```

### 依存関係

- **pillow**: 基本的な画像操作
- **numpy**: 数値計算と画像配列操作
- **opencv-python**: 高度な画像処理と16ビット画像対応
- **scikit-image**: 画質指標計算（PSNR、SSIM）
- **matplotlib**: 可視化
- **scipy**: 科学計算
- **noise**: Perlinノイズ生成
- **piexif**: EXIF データ操作
- **pandas**: データ分析とCSV出力

### カスタマイズ

#### 新しいバリエーションの追加

`src/variation_generator.py`で新しい変換パターンを定義できます：

```python
def _convert_new_variation(source, output_dir, parameter):
    """新しいバリエーションの変換関数"""
    output_file = os.path.join(output_dir, f"new_variation_{parameter}.jpg")
    cmd = ["convert", source, "-your-imagemagick-options", output_file]
    _run_imagemagick_command(cmd)
```

#### 検証ルールの追加

`src/variation_validator.py`で新しい検証ルールを追加できます：

```python
# 新しい仕様を追加
new_specs = {
    'new_variation_test.jpg': {'your_property': 'expected_value'}
}
```

### トラブルシューティング

#### ImageMagickが見つからない

```bash
# インストール確認
convert -version

# macOSでパスが通らない場合
export PATH="/opt/homebrew/bin:$PATH"
```

#### メモリ不足エラー

大きな画像での処理時は、ImageMagickのメモリ制限を調整：

```bash
export MAGICK_MEMORY_LIMIT=2GB
export MAGICK_MAP_LIMIT=2GB
```

#### Python依存関係エラー

```bash
# 仮想環境の使用を推奨
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🤝 貢献

プロジェクトへの貢献を歓迎します！

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 課題・要望

GitHub Issuesで課題報告や機能要望をお願いします。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- ImageMagick開発チーム
- OpenCV開発チーム  
- Python画像処理コミュニティ

---

**更新日**: 2025年5月31日  
**バージョン**: 1.0.0