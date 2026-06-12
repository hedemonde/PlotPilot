【小说设定】
书名：{{ novel.title }}

故事创意/原始设定：
{{ novel.premise }}

大类：{{ novel.genre_major }}
主题：{{ novel.genre_theme }}
类型：{{ novel.genre_label }}
基调：{{ novel.world_preset }}
剧情结构：{{ novel.story_structure }}
节奏把控：{{ novel.pacing_control }}
写作风格：{{ novel.writing_style }}
特殊要求：{{ novel.special_requirements }}
目标章节数：{{ novel.target_chapters }}
每章目标字数：{{ novel.target_words_per_chapter }}

请一次性构建小说 Bible：世界观、角色阵容、地点地图与文风公约。

硬约束：
1. 先从【故事创意/原始设定】中抽取已经出现的人物、人名、关系、身份、创伤事件、地点、时代背景、季节节点和关键意象；这些内容必须保留，不得改名、换关系、换职业时代或改写成无关类型套路。
2. 类型、基调、世界观和市场化戏剧张力只能用于补全空白，不能覆盖作者原始设定。现实校园、都市、职场等原始场域不得被改写为宗门、秘境、王朝、修仙学院、灵脉、洞府等无来源外壳。
3. 角色必须服务 premise 中已有冲突和情绪链，不得凭空加入与 premise 无关的幕后黑手、改名线、王朝秘辛、血脉宿命等核心悬念。
4. 文风、节奏和特殊要求是生成边界，输出必须与其一致。

直接输出 JSON（不要包在代码块里）：

{
  "style": "文风公约，2-3句，单行",
  "worldbuilding": {
    "core_rules": {
      "power_system": "核心能力/社会运行机制，单行",
      "physics_rules": "底层规则，单行",
      "magic_tech": "技术/特殊机制，单行"
    },
    "geography": {
      "terrain": "空间地理，单行",
      "climate": "环境与季节，单行",
      "resources": "关键资源，单行",
      "ecology": "生态或日常环境，单行"
    },
    "society": {
      "politics": "权力结构，单行",
      "economy": "资源流通，单行",
      "class_system": "阶层/身份差异，单行"
    },
    "culture": {
      "history": "关键过往，单行",
      "religion": "信念/价值秩序，单行",
      "taboos": "禁忌，单行"
    },
    "daily_life": {
      "food_clothing": "日常生活，单行",
      "language_slang": "语言习惯，单行",
      "entertainment": "消遣/公共生活，单行"
    }
  },
  "characters": [
    {
      "name": "角色全名",
      "gender": "性别",
      "age": "年龄",
      "role": "主角/对立角色/盟友/次要角色",
      "description": "一句话功能定位与人物矛盾，单行",
      "appearance": "外貌锚点，单行",
      "personality": "性格底色，单行",
      "background": "关键背景，单行",
      "public_profile": "公开身份，单行",
      "hidden_profile": "隐藏身份/秘密；没有则空字符串",
      "reveal_chapter": null,
      "mental_state": "开局心理状态",
      "mental_state_reason": "心理状态成因，单行",
      "core_belief": "核心信念",
      "moral_taboos": ["绝不做的事"],
      "core_motivation": "表层目标，单行",
      "inner_lack": "深层缺口，单行",
      "ghost": "内心创伤或恐惧",
      "want": "表层目标",
      "need": "深层需要",
      "flaw": "致命弱点",
      "verbal_tic": "口头禅；没有则空字符串",
      "idle_behavior": "压力下的小动作",
      "voice_profile": {
        "style": "话语风格",
        "sentence_pattern": "句式习惯",
        "speech_tempo": "fast/normal/slow",
        "metaphors": ["常用隐喻"],
        "catchphrases": ["口头禅"]
      },
      "active_wounds": [
        {"description": "未愈合创伤", "trigger": "触发条件", "effect": "触发后的反应"}
      ],
      "relationships": [
        {"target": "其他角色名", "relation": "关系", "description": "张力说明"}
      ]
    }
  ],
  "locations": [
    {
      "id": "唯一ID，小写英文+下划线+数字",
      "name": "地点名",
      "type": "城市/建筑/区域/特殊场所",
      "description": "地点功能与叙事价值，单行",
      "parent_id": null,
      "connections": [
        {"target": "目标地点名", "relation": "包含/相邻/通往/封锁/隐藏通道", "description": "连接的叙事意义，单行"}
      ]
    }
  ]
}
