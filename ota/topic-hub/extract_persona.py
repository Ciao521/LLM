import json
import sys

# python scripts/extract_persona.py > data/persona_jp.jsonl


# Convert this to markdown table. Then extract "代 表 例" items as a Python list.
#
# ```
# (copy and paste the content of https://www.mhlw.go.jp/content/10700000/000513179.pdf)
# ```

occupations_mhlw = [
    "部長", "課長", "支店長", "工場長", "駅長", "区長",
    "研究機関の研究者", "大学の研究者", "企業の研究者", "研究所長",
    "電気設計技術員", "情報機器開発技術者", "半導体製品製造技術者", "電気工事技術者",
    "機械設計技術者", "プラント設計技術者", "機械技術士", "電気機械技術者", "配管技術者（機械）",
    "自動車設計技術者", "自動車製造技術者", "航空機技術者",
    "製鉄技術者", "製鋼技術者", "精錬技術者", "金属技術士",
    "工業化学技術者", "油脂化学技術者", "化学技術士",
    "建築士", "建築施工管理技術者", "建設設計技術者", "建築現場監督",
    "土木施工管理技術者", "土木現場監督", "建設技術士", "上下水道技術士", "道路技術者", "河川土木技術者",
    "測量士", "測量士補", "道路測量士",
    "システムコンサルタント", "システムアナリスト",
    "社内システムエンジニア", "プログラマー",
    "サーバー管理者", "セキュリティ技術者", "電気通信主任技術者",
    "作業環境測定士", "農業技術者", "食品化学技術者",
    "医師", "病院長（医師）", "診療所長（医師）",

    "歯科医師", "歯科医院長（歯科医師）",
    "獣医師", "動物病院長（獣医師）",
    "薬剤師",
    "保健師",
    "助産師",
    "看護師", "看護師長", "訪問看護師",
    "准看護師",
    "診療放射線技師", "診療エックス線技師",
    "臨床検査技師", "衛生検査技師",
    "理学療法士", "作業療法士", "言語聴覚士", "視能訓練士",
    "歯科衛生士",
    "歯科技工士",
    "栄養士", "管理栄養士", "栄養指導員",
    "臨床工学技士", "マッサージ師", "はりきゅう師", "柔道整復師",
    "保育士",
    "ケアマネージャー",
    "福祉相談指導専門員", "福祉施設指導専門員", "生活指導員", "職業指導員", "サービス管理責任者", "相談支援専門員（障害者施設）", "ソーシャルワーカー",
    "弁護士", "司法書士", "弁理士",
    "公認会計士", "会計士補", "税理士", "社会保険労務士", "経営コンサルタント",
    "幼稚園の園長", "幼稚園の教頭", "幼稚園の教諭", "幼稚園の講師", "保育教諭",
    "小学校の校長", "中学校の校長", "小学校の教頭", "中学校の教頭", "小学校の教諭", "中学校の教諭", "小学校の講師", "中学校の講師",
    "高等学校の校長", "中等教育学校の校長", "高等学校の教頭", "中等教育学校の教頭", "高等学校の教諭", "中等教育学校の教諭", "高等学校の講師", "中等教育学校の講師",
    "大学の教授", "大学院の教授", "短期大学の教授", "高専の教授", "医師（大学教授）", "歯科医師（大学教授）",
    "大学の准教授", "大学院の准教授", "短期大学の准教授", "高専の准教授",
    "大学の講師", "大学院の講師", "短期大学の講師", "高専の講師", "大学の助教", "大学院の助教", "短期大学の助教", "高専の助教",
    "各種学校教員", "専修学校教員", "特別支援学校教諭", "予備校教員", "自動車学校教員",
    "神父", "神主", "僧侶", "住職",
    "新聞記者", "編集員",
    "イラストレーター", "写真記者",
    "産業デザイナー（商品デザインなど）", "インテリアコーディネーター",
    "ピアニスト", "役者", "ダンサー", "ディレクター",
    "ピアノ個人教師", "塾講師（各種学校でないもの）",
    "行政書士", "不動産鑑定士", "検数員", "司書", "通訳",

    "庶務係事務員", "人事係事務員", "企画係事務員", "商品開発係事務員", "秘書", "受付・案内係事務員", "広報係事務員", "クラーク", "医療事務員", "企業情報管理士",
    "コールセンターオペレーター", "電話交換手", "テレフォンアポインター", "通信受付事務（電話）",
    "経理係事務員", "税理士事務所の事務員", "預貯金窓口事務員", "物品調達係事務員",
    "生産管理事務員", "出荷事務員",
    "販売伝票記録員", "営業事務員",
    "メーター検針員", "公共料金集金人", "市場調査員",
    "運行管理者", "配車係", "郵便窓口係員",
    "キーパンチャー", "データ・エントリー装置操作員", "電子計算機操作員", "ＯＣＲ機器操作員",

    "百貨店店員", "総合スーパー店員", "ショップ店員", "コンビニ店員", "小売・卸売店主",
    "街頭販売員", "訪問販売員（商品携行）",
    "不動産仲介人", "株式売買人", "保険代理業務員", "宝くじ販売人", "自動車販売代理店主",
    "自動車セールス員",
    "二輪車セールス員", "セールスエンジニア", "システム営業職員",
    "銀行外務員", "有価証券勧誘員",
    "保険セールス員", "保険契約外交員",
    "食料品ルートセールス員", "不動産セールス員", "医薬品販売外交員", "広告取り",

    "介護職員（医療、福祉施設）", "介護福祉士", "ケアワーカー", "生活支援員（障害者施設）",
    "ホームヘルパー",
    "看護助手", "看護補助者",
    "歯科助手", "動物看護師", "鍼灸師助手",
    "理容師", "美容師",
    "クリーニング職", "染み抜き工",
    "エステティシャン", "ネイリスト", "温泉浴場従事者",
    "飲食店の料理人", "給食調理人", "バーテンダー",
    "板前", "飲食店主（自ら飲食物の調理を行う）",

    "飲食店ホール係", "ウエイター", "ウエイトレス", "ファーストフード店店員", "飲食店主（自ら飲食物の調理を行わない）",
    "キャビンアテンダント", "フライトアテンダント",
    "旅館・ホテルの接客係", "客室係", "仲居",
    "動物園出札係", "パチンコ店店員", "キャディー", "映画館案内係", "娯楽場アナウンサー", "接客社交係",
    "マンションの管理人", "ビルの管理人", "駐車場の管理人", "駐車場誘導員",
    "レンタルショップ店員", "葬儀作業者", "トリマー", "旅行添乗員", "ビラ配り人", "ポスティング人", "保育補助者", "便利屋", "巫女",

    "守衛", "警備員", "夜警員",
    "交通誘導員", "建設現場誘導員", "プール監視員",
    "間伐作業者", "植林作業員", "漁師", "造園師",

    "製銑工", "精錬工", "製鋼工",
    "鋳物工", "鍛造工", "鋳造工", "鋳型工",
    "旋盤工", "フライス盤工",
    "金属プレス工",
    "鉄骨工", "橋りょう工", "製缶工",
    "板金工", "板金加工職",
    "めっき工", "研磨工", "バフ磨工",
    "アーク溶接工", "ガス溶接工",
    "針・ばね・金属ねじ製造工", "はんだ付工",
    "化学薬品製造工", "化学繊維製造工", "石油精製工", "紡糸工",
    "ガラス製品製造工", "陶器製造工", "石工", "石切工", "石積工", "コンクリートブロック製造工",
    "食料品・飲料・酒類製造工", "水産物処理加工者",

    "紡績工", "ねん糸工", "ミシン工", "精紡工", "仕立工",
    "チップ選別工", "家具製造工", "木型工", "建具工", "製紙工",
    "オフセット印刷工", "製本工", "製版工", "印刷写真工",
    "タイヤ製造・修理工", "タイヤ製造・修理工", "合成樹脂製品生計工",
    "がん具組立・加工作業員", "靴製造工", "靴修理工", "内張工", "かばん製造工", "バッグ製造工",
    "エンジン組立工", "機械調整工", "機械据付工",
    "発電機組立工", "電子回路基板製造工", "通信機組立工",
    "車体組立工", "部品組立工", "エンジン取付工",
    "電車組立工", "時計組立・調整工", "レンズ工", "計量計測機器・光学機器組立工",
    "電気機械修理工", "機械保全工", "機械分解工", "内燃機関修理工",
    "自動車整備工", "自動車修理工",
    "電車修理工", "自転車修理工", "時計修理工",
    "鋳物製品検査工", "金属製品検査工", "プレス検査工",
    "化学製品検査工", "繊維製品検査工", "検瓶工", "仕上検査工",
    "工作機械検査工", "ポンプ検査工", "電気製品検査工", "電気部品検査工", "自動車検査工", "時計検査工", "輸送機械検査工", "レンズ検査工",
    "アニメーター", "塗装工", "看板製作工", "自動車塗装工", "船体塗装工",
    "写真現像工", "製図工", "ＣＡＤオペレーター", "舞台照明係",

    "電車運転士", "モノレール運転士",
    "マイクロバス運転者",
    "タクシー運転者",
    "送迎運転者", "役員運転者", "代行運転者",
    "営業用大型トラック運転者", "ミキサー車運転者", "バキュームカー運転者", "トレーラー運転者", "タンクローリー運転者",
    "営業用普通トラック運転者", "塵芥収集車", "郵便運送自動車",
    "自家用トラック運転者",
    "宣伝カー運転者", "レッカー車運転者", "清掃車運転者",
    "パイロット", "航空機関士",
    "列車車掌", "バス車掌",
    "駅構内係", "フォークリフト運転者",
    "発電員", "変電員", "送電員", "発電保守員", "変電保守員",
    "クレーン運転操作工", "コンベアー運転工",

    "ドラグショベル運転工", "トラッククレーン運転工", "コンクリート舗装機械運転工",
    "エレベーター機械係", "クレーン合図員", "玉掛工", "リフト運転員", "ごみ処理プラント操作員",

    "型枠大工", "木製型枠工", "型枠解体工", "とび職", "杭打工", "取り壊し作業員", "鉄筋切断工", "鉄筋組立工",
    "大工", "宮大工",
    "配管工", "給排水衛生配管工", "冷暖房工",
    "左官", "壁塗り工", "モルタル塗り工", "屋根ふき工", "はつり工", "防水工", "保温工", "保冷工", "内装仕上工",
    "電気工事作業者", "通信線配線工", "電気工事士", "電気保安工", "電気設備工",
    "土木作業員", "コンクリート打工", "アスファルト舗装作業員", "線路工事作業者",
    "ダム・トンネル掘削工", "採石工", "発破員", "砂利採取員",

    "船内荷役作業者", "港湾荷役作業者", "上屋", "フォアマン",
    "引越作業員", "倉庫作業員", "リサイクル品回収人（回収のみ）", "牛乳配達人", "新聞配達人", "宅配配達人", "郵便配達員", "荷造工", "自動販売機商品補充員",
    "ビル清掃員", "建物ガラス拭き作業員", "床磨き作業員",
    "公園清掃員", "消毒作業員", "ごみ収集作業員", "列車清掃員",
    "ラッピング作業者", "ラベル貼り作業者", "箱詰作業者（包装）",
    "公園草取作業員", "学校用務員", "貨物自動車助手", "食器洗い人（調理見習いでないもの）",
]

# Here is a list of occupations. Extract items as a Python list.
#
# ```
# (copy and paste the content of https://ja.wikipedia.org/wiki/%E8%81%B7%E6%A5%AD%E4%B8%80%E8%A6%A7)
# ```

occupations_wikipedia = [
    "アイドル", "アーキビスト", "アクチュアリー", "アシスタントディレクター", "アスレティックトレーナー", "アーティスト", "アートディレクター",
    "アナウンサー", "アニメーター", "海人", "アメリカンフットボール選手", "アレンジャー", "あん摩マッサージ指圧師",
    "医師", "石工", "イタコ", "板前", "鋳物工", "イラストレーター", "医療監視員", "医療事務員", "医療従事者", "医療保険事務",
    "刺青師", "インストラクター", "インダストリアルデザイナー", "インタープリター (自然)", "インテリアコーディネーター", "インテリアデザイナー",
    "ウェディングプランナー", "ウェブデザイナー", "鵜飼い", "浮世絵師", "宇宙飛行士", "占い師", "運転士", "運転手", "運転代行",
    "映画監督", "映画スタッフ", "映画俳優", "映画プロデューサー", "営業員", "衛視", "衛生検査技師", "映像作家", "栄養教諭", "栄養士",
    "駅員", "駅長", "エクステリアデザイナー", "エグゼクティブ・プロデューサー", "絵師", "エステティシャン", "エディトリアルデザイナー",
    "絵本作家", "演歌歌手", "園芸家", "エンジニア", "演出家", "演奏家",
    "オートレース選手", "オプトメトリスト", "お笑い芸人", "お笑いタレント", "音楽家", "音楽評論家", "音楽プロデューサー",
    "音楽療法士", "音響監督", "音響技術者",

    "海技従事者", "会計士", "外交官", "外航客船パーサー", "介護ヘルパー", "海事代理士", "会社員", "海上自衛官", "海上保安官", "会長",
    "介助犬訓練士", "カイロプラクター", "カウンセラー", "画家", "学芸員", "科学者", "学者", "学生", "学長", "格闘家", "菓子製造技能士",
    "歌手", "歌人", "カスタマエンジニア", "楽器製作者", "学校事務職員", "学校職員", "学校用務員", "活動弁士", "家庭教師", "カーデザイナー",
    "歌舞伎役者", "カメラマン", "カラーコーディネーター", "カラーセラピスト", "為替ディーラー", "環境デザイナー", "環境計量士", "環境コンサルタント",
    "観光コンサルタント", "看護師", "看護助手", "鑑定人", "監督", "官房長官", "管理栄養士", "官僚",
    "議員", "機関士", "戯曲家", "起業家", "樵", "棋士 (囲碁)", "棋士 (将棋)", "記者", "騎手", "技術コンサルタント",
    "技術者", "気象予報士", "機長", "キックボクサー", "着付師", "客室乗務員", "脚本家", "キャビンアテンダント", "キャラクターデザイナー",
    "キャリア (国家公務員)", "キャリア・コンサルタント", "救急救命士", "救急隊員", "きゅう師", "給仕人", "厩務員", "キュレーター",
    "教育関係職員", "教員", "行政官", "行政書士", "競艇選手", "教頭", "教諭", "銀行員",
    "空間情報コンサルタント", "空間デザイナー", "グラウンドキーパー", "グラフィックデザイナー", "グランドスタッフ", "グランドホステス",
    "クリエイティブ・ディレクター", "クリーニング師", "クレーン運転士", "軍事評論家", "軍人",
    "ケアワーカー（介護士）", "経営コンサルタント", "経営者", "芸妓", "経済評論家", "警察官", "芸術家", "芸人", "芸能人",
    "芸能リポーター", "警備員", "刑務官", "警務官", "計量士", "競輪選手", "劇作家", "ケースワーカー", "ゲームクリエイター",
    "ゲームシナリオライター", "ゲームデザイナー", "ゲームライター", "検疫官", "研究員", "言語聴覚士", "検察官", "検察事務官",
    "建設コンサルタント", "現像技師", "建築家", "建築コンサルタント", "建築士",
    "校閲者", "航海士", "公共政策コンサルタント", "工業デザイナー", "航空管制官", "航空機関士", "皇宮護衛官", "航空自衛官",
    "航空従事者", "航空整備士", "工芸家", "講師 (教育)", "工場長", "交渉人", "講談師", "校長", "交通指導員", "高等学校教員",
    "公認会計士", "公務員", "校務員", "港湾荷役作業員", "国際公務員", "国連職員", "国税専門官", "国務大臣", "ゴーストライター",
    "国会議員", "国会議員政策担当秘書", "国会職員", "国家公務員", "コック", "コ・デンタル", "コピーライター", "コミッショナー",
    "コメディアン", "コ・メディカル", "コラムニスト", "顧問", "コンサルタント", "コンシェルジュ", "コンセプター", "コンピュータ技術者",

    "再開発プランナー・再開発コンサルタント", "裁判官", "裁判所職員", "裁判所調査官", "サウンドクリエイター", "左官", "作業療法士",
    "作詞家", "撮影監督", "撮影技師", "作家", "サッカー選手", "作曲家", "茶道家", "サラリーマン", "参議院議員",
    "指圧師", "自衛官", "シェフ", "歯科医師", "司会者", "歯科衛生士", "歯科技工士", "歯科助手", "士官", "指揮者",
    "司書", "司書教諭", "詩人", "システムアドミニストレータ", "システムエンジニア", "自然保護官", "質屋", "市町村長",
    "実業家", "自動車整備士", "児童文学作家", "シナリオライター", "視能訓練士", "司法書士", "事務員", "社会福祉士",
    "社会保険労務士", "車掌", "写真家", "写真ディレクター", "社長", "ジャーナリスト", "写譜屋", "獣医師", "衆議院議員",
    "臭気判定士", "柔道整復師", "守衛", "ジュエリーデザイナー", "塾講師", "手話通訳士", "准看護師", "准教授", "小学校教員",
    "上下水道コンサルタント", "証券アナリスト", "将校", "小説家", "消防官", "照明技師", "照明技術者", "照明士", "照明デザイナー",
    "書家", "助教", "助教授", "職人", "ショコラティエ", "助手 (教育)", "初生雛鑑別師", "書道家", "助産師", "シンガーソングライター",
    "神職", "審判員", "新聞記者", "新聞配達員", "心理カウンセラー", "診療放射線技師", "心理療法士", "森林コンサルタント", "樹医",
    "随筆家", "推理作家", "スカウト (勧誘)", "スクールカウンセラー", "寿司職人", "スタイリスト", "スタジオ・ミュージシャン",
    "スタント・パーソン", "スタントマン", "スチュワーデス", "スチュワード", "ストリートミュージシャン", "スパイ", "スーパーバイザー",
    "スポーツ選手", "スポーツドクター", "摺師",
    "製菓衛生師", "声楽家", "税関職員", "政治家", "聖職者", "整体師", "青年海外協力隊員", "整備士", "声優", "税理士",
    "セックスワーカー", "ゼネラルマネージャー", "セラピスト", "船員", "選挙屋", "船長", "戦場カメラマン", "染織家", "潜水士",
    "造園家/造園コンサルタント", "葬儀屋", "造形作家", "相場師", "操縦士", "装丁家", "僧侶", "測量士・測量技師", "ソーシャルワーカー",
    "速記士", "ソムリエ", "ソムリエール", "村議会議員",

    "大学教員", "大学教授", "大学職員", "大工", "大臣", "大道芸人", "大統領", "ダイバー", "殺陣師", "旅芸人",
    "タレント", "ダンサー", "探偵",
    "チェリスト", "知事", "地質コンサルタント", "チーフプロデューサー", "地方議会議員", "地方公務員", "中学校教員",
    "中小企業診断士", "調教師", "調香師", "彫刻家", "聴導犬訓練士", "著作家",
    "ツアーコンダクター", "通関士", "通信士", "通訳", "通訳案内士",
    "ディスクジョッキー", "ディスパッチャー", "ディーラー", "ディレクター", "テクニカルディレクター (スポーツ)",
    "テクニカルディレクター (テレビ)", "テクノクラート", "デザイナー", "デザインプロデューサー", "テニス選手",
    "テレビディレクター", "テレビプロデューサー", "電気工事士", "電車運転士", "添乗員", "電話交換手",
    "陶芸家", "投資家", "杜氏", "動物看護師", "動物管理官", "時計師", "登山家", "都市計画コンサルタント",
    "図書館司書", "鳶職", "トラックメイカー", "トリマー", "ドリラー", "トレジャーハンター", "トレーナー",

    "内閣官房長官", "内閣総理大臣", "仲居", "ナニー", "ナレーター",
    "入国警備官", "入国審査官", "ニュースキャスター", "庭師",
    "塗師",
    "ネイリスト", "ネイルアーティスト", "ネットワークエンジニア",
    "農家", "能楽師", "納棺師", "農業土木コンサルタント", "ノンフィクション作家",

    "配管工", "俳人", "バイヤー", "俳優", "パイロット", "バスガイド", "バスケットボール選手", "パタンナー", "発明家", "パティシエ",
    "バーテンダー", "噺家", "花火師", "花屋", "はり師", "バリスタ (コーヒー)", "バルーンアーティスト", "パン屋",
    "ピアノ調律師", "美術 (職業)", "美術家", "美術商", "秘書", "筆跡鑑定人", "ビデオジョッキー", "ビューロクラート", "美容師",
    "評論家", "ビル管理技術者",
    "ファイナンシャル・プランナー", "ファシリテーター", "ファシリティマネジャー", "ファッションデザイナー", "ファッションフォトグラファー",
    "ファッションモデル", "ファンタジー作家", "ファンドマネージャー", "ファンドレイザー", "風俗嬢", "フェロー", "副校長",
    "服飾デザイナー", "副操縦士", "腹話術師", "舞台演出家", "舞台監督", "舞台俳優", "舞台美術家", "舞踏家", "武道家",
    "不動産鑑定士", "不動産屋", "フードコーディネーター", "舞踊家", "フライトアテンダント", "フラワーデザイナー", "プラントハンター",
    "ブリーダー", "振付師", "フリーライター", "プログラマ", "プロゴルファー", "プロジェクトマネージャ", "プロデューサー",
    "プロブロガー", "プロボウラー", "プロボクサー", "プロ野球選手", "プロレスラー", "文芸評論家", "文筆家", "フライス盤工",
    "ヘアメイクアーティスト", "ペスト・コントロール・オペレーター", "ベビーシッター", "編曲家", "弁護士", "編集者", "弁理士",
    "保安官", "保育士", "冒険家", "放射線技師", "宝飾デザイナー", "放送作家", "法務教官", "訪問介護員", "牧師", "保険計理人",
    "保健師", "保護観察官", "補償コンサルタント", "ホステス", "ホスト", "ボディーガード", "ホームヘルパー", "ホラー作家",
    "彫師", "翻訳家",

    "舞妓", "マジシャン (奇術)", "マーシャラー", "マスタリング・エンジニア", "マタギ", "マッサージ師", "マニピュレーター", "マルチタレント", "漫画家", "漫画原作者", "漫才師", "漫談家",
    "ミキサー", "巫女", "水先案内人", "水先人", "宮大工", "ミュージシャン",
    "無線通信士",
    "メイクアップアーティスト", "メイド", "メジャーリーガー",
    "盲導犬訓練士", "モデラー (模型)", "モデル (職業)",

    "薬剤師", "役者", "野菜ソムリエ",
    "郵便配達", "YouTuber",
    "洋菓子職人", "養護教諭", "洋裁師", "養蚕家", "幼稚園教員", "養蜂家",

    "ライトノベル作家", "ライフセービング", "落語家", "酪農家", "ラグビー選手", "ラジオパーソナリティ",
    "ランドスケープアーキテクト", "ランドスケーププランナー", "ランドスケープデザイナー", "ランドスケープコンサルタント",
    "理学療法士", "力士", "陸上自衛官", "リポーター", "猟師", "漁師", "理容師", "料理研究家", "料理人", "旅行作家", "林業従事者", "臨床検査技師", "臨床工学技士", "臨床心理士",
    "ルポライター",
    "レコーディング・エンジニア", "レーサー", "レーシングドライバー", "レスキュー隊員", "レポーター", "レンジャー",
    "労働基準監督官", "録音技師",

    "和菓子職人", "和裁士", "和紙職人",

    "A&R",
    # "AV監督", "AV女優", "AV男優",
    "CMディレクター", "DJ", "ITコーディネータ", "MR", "PAエンジニア", "SF作家", "SP"
]

occupations_other = [
    "幼稚園児",
    "保育園児",
    "小学生",
    "中学生",
    "高校生",
    "高専生",
    "専門学校生",
    "予備校生",
    "大学生",
    "大学院生",
    "ポスドク",
    "留学生",
    "職業訓練生",
    "インターン",
    "ボランティア",
    "主婦",
    "主夫",
    "家事手伝い",
    "無職",
    "ニート",
    "フリーター",
    "パート",
    "アルバイト",
    "自営業者",
    "フリーランス",
]

print(f"length of occupations_mhlw: {len(occupations_mhlw)}", file=sys.stderr)
print(f"length of occupations_wikipedia: {len(occupations_wikipedia)}", file=sys.stderr)
print(f"length of occupations_other: {len(occupations_other)}", file=sys.stderr)

# Find the intersection of the two lists
occupations_intersection = set(occupations_mhlw) & set(occupations_wikipedia)
print(f"length of occupations_intersection: {len(occupations_intersection)}", file=sys.stderr)
print(f"occupations_intersection: {occupations_intersection}", file=sys.stderr)

# Merge the three lists
occupations_merged = list(set(occupations_mhlw) | set(occupations_wikipedia) | set(occupations_other))
print(f"length of occupations_merged: {len(occupations_merged)}", file=sys.stderr)

# Sort the merged list
occupations_sorted = sorted(occupations_merged)

# Save the merged list to a file
for occupation in occupations_sorted:
    print(json.dumps({"persona": occupation}, ensure_ascii=False))

# Run the following command to generate a JSONL file.
# python extract_persona.py > persona_jp.jsonl
