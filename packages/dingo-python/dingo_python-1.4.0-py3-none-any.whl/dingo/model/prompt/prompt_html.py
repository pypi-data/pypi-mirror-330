from dingo.model.model import Model
from dingo.model.prompt.base import BasePrompt

@Model.prompt_register("Html_Split", [])
class PromptHtmlSplit(BasePrompt):
    content = """
你是一位熟悉HTML代码的前端工程师。现在需要通过阅读HTML代码来将不同的HTML模块取出并加工成字典，要求如下：
- 代码模块：包括type、inline、content字段，其中content字段又包括code_content、language字段。
    type为string类型，固定值为"code"。inline为bool类型，判断是否为行内代码。content为字典类型。content.code_content为string类型，是格式化过的代码内容。content.language为string类型，是代码语言类型。
    例如：
    {
        "type": "code",
        "inline": false,
        "content": {
              "code_content": "def add(a, b):\n    return a + b",
              "language": "python",
        }
    }      
- 标题模块：包括type、content字段。其中content字段又包括title_content、level字段。
    type为string类型，固定值为"title"。content为字典类型。content.title_content为string类型，是格式化后的标题内容。content.level为int类型，是标题级别，取值为1-N且1最大。
    例如：
    {
        "type": "title",
        "content": {
            "title_content": "大模型好，大模型棒",
            "level": 1
        }
    }
- 段落模块：包括type、content字段。其中content字段又包括c、t字段。
    type为string类型，固定值为"paragraph"。content是array类型，其中每个元素是一个字典类型。content.c是string类型，格式化后的段落内容。content.t是string类型，只有3个取值"text"、"equation-inline"、"md"，分别表示纯文本和行内公式和markdown。
    例如：
    {
        "type": "paragraph",
        "content": [
            {"c": "爱因斯坦的质量方差公式是", "t": "text"},
            {"c": "E=mc^2", "t": "equation-inline"},
            {"c": "，其中E是能量，m是质量，c是光速 ","t": "text"}
          ]
    }

以上的模块加工成字典之后，将其按照在HTML中的顺序填充到一个List中，作为回答。
例如：
[
    {
        "type": "code",
        "inline": false,
        "content": {
              "code_content": "def add(a, b):\n    return a + b",
              "language": "python",
        }
    },
    {
        "type": "title",
        "content": {
            "title_content": "大模型好，大模型棒",
            "level": 1
        }
    },
    {
        "type": "paragraph",
        "content": [
            {"c": "爱因斯坦的质量方差公式是", "t": "text"},
            {"c": "E=mc^2", "t": "equation-inline"},
            {"c": "，其中E是能量，m是质量，c是光速 ","t": "text"}
          ]
    }
]

注意不要输出解释性内容，也不要有注释

以下是HTML代码：
"""