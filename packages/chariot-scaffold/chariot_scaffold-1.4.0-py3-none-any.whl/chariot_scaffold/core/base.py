import abc
import typing
import asyncio
import functools
from enum import Enum

from chariot_scaffold.core.config import Lang
from chariot_scaffold import data_mapping, log
from chariot_scaffold.exceptions import PackError


class Base(metaclass=abc.ABCMeta):
    """✨ 元数据解析基类 | 魔法少女的契约之书 📖"""

    def __init__(self, title=None, description=None, model=None):
        # 💎 灵魂绑定数据区
        self.__vars_name = None  # 函数内部变量名宝库
        self.__defaults = None  # 默认值糖果盒
        self.__comments = None  # 注释魔法卷轴
        self.__annotations = None  # 类型注解星图
        self.__params_name = None  # 参数名花名册
        self._func_name = None  # 契约者真名
        self._types = {}  # 类型精灵图鉴

        # 🎀 外观属性
        self.model = model  # 参数守卫模型
        self.title = title  # 契约标题
        self.description = description  # 契约描述

        # 📦 输入输出装备库
        self.input = {}  # 参数装备展示架
        self.output = {}  # 返回值王冠陈列台

    def __call__(self, func):
        """✨ 魔法契约签订仪式 | 将普通函数变成魔法少女！"""
        # 🧬 刻印函数灵魂信息
        self.bind_func_info(func)
        # 🛠️ 打造参数铠甲
        self.generate_func_info()
        # 🔮 启动子类专属魔法阵
        self.hook()

        # 🌈 同步/异步双重形态切换
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 🗺️ 绘制参数藏宝图
            mapping = self.get_params_mapping(*args, **kwargs)
            # 🛡️ 召唤模型守卫
            if self.model:
                self.check_model(mapping)
            # ⚡ 发动原函数魔法
            return func(*args, **kwargs)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            mapping = self.get_params_mapping(*args, **kwargs)
            if self.model:
                self.check_model(mapping)
            # ⏳ 异步魔法蓄力
            return await func(*args, **kwargs)

            # 🔄 形态选择器
        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    def generate_func_info(self):
        """🎠 组装函数信息三件套"""
        self.bind_parameters()  # 🎯 参数铠甲锻造
        self.bind_defaults()  # 🍬 默认值糖果分发
        self.bind_output()  # 👑 返回值王冠打造

    def bind_func_info(self, func):
        """📜 捕捉函数的灵魂信息"""
        self.__vars_name = func.__code__.co_varnames  # 🌀 变量名星河
        self.__params_name = [self.__vars_name[i] for i in range(func.__code__.co_argcount)]  # 🎪 参数小分队名单
        self.__annotations = func.__annotations__  # 🌌 类型标签贴纸
        self.__comments = func.__doc__  # 📖 故事书目录
        self.__defaults = func.__defaults__  # 🍭 默认值糖果袋
        self._func_name = func.__name__  # 🏷️ 契约者真名铭牌

    def bind_parameters(self):
        """🎁 给参数小可爱们穿装备"""   # noqa
        for param in self.__params_name:
            if param != 'self':  # 🤖 跳过机器人管家
                # 🧵 初始化装备包
                self.input[param] = {
                    "name": param,
                    "title": None,  # 🏷️ 待填写的姓名牌
                    "description": None,  # 📝 空白故事板
                    "type": None  # 🔮 待识别的属性水晶
                }

                anno = self.__annotations.get(param)
                if isinstance(anno, typing._AnnotatedAlias):  # noqa
                    # 🎇 发现高级注解装备箱
                    res = self.match_annotated(anno)
                    self.input[param].update(res)
                else:
                    # 🎨 绘制基础信息
                    self.input[param]["title"] = self.lang_checking(param)
                    self.input[param]["description"] = self.lang_checking(param)
                    self.input[param]["type"] = self.match_datatype(anno)

    def bind_defaults(self):
        """🍬 给参数分发默认值糖果"""
        defaults_length = len(self.__defaults) if self.__defaults else 0

        # 🔄 倒序寻宝模式启动
        re_params_name = self.__params_name[::-1]
        re_defaults = self.__defaults[::-1] if defaults_length else []

        for i in range(len(self.__params_name)):
            if re_params_name[i] != 'self':
                if i < defaults_length:  # 🍭 找到糖果！
                    param_info = self.input[re_params_name[i]]
                    param_info["default"] = re_defaults[i]

                    # 🧹 打扫空值房间
                    if param_info["default"] is None:
                        if param_info["type"] == "[]string":
                            param_info["default"] = []  # 🧺 换上干净篮子
                        if param_info["type"] == "[]object":
                            param_info["default"] = {}  # 🗃️ 准备魔法柜子

                    # 🎲 发现枚举骰子
                    if isinstance(param_info["default"], Enum):
                        enum_value = param_info["default"]
                        param_info["enum"] = [i.value for i in enum_value.__class__]  # 🎪 召唤所有骰子面
                        param_info["default"] = enum_value.value  # 🎯 显示当前骰子点数
                else:
                    self.input[re_params_name[i]]["required"] = True  # 🚨 标记必填项

    def bind_output(self):
        """👑 打造输出王冠"""
        output_type = self.__annotations.get("return")
        if output_type:
            if isinstance(output_type, dict):
                # 🧩 组装复杂王冠组件
                self.match_basemodel(output_type)
                self.output = self._types
            else:
                # 🎀 制作默认王冠
                self.output["output"] = {
                    "type": self.match_datatype(output_type),
                    "title": Lang("输出", "output").convert(),  # 🌐 多语言宝石
                    "description": Lang("默认输出", "Default Output").convert()
                }

    def check_model(self, kwargs):
        """🛡️ 召唤模型守卫进行参数检查"""
        self.model(**kwargs)  # ⚔️ 发动参数验证斩击

    def get_params_mapping(self, *args, **kwargs) -> dict:
        """🗺️ 绘制参数藏宝图"""
        mapping = {}
        # 🎯 三阶段藏宝图绘制：
        # 1. 默认值宝藏标记
        if self.__defaults:
            for i in range(len(self.__defaults)):
                mapping[list(self.__params_name)[::-1][i]] = list(self.__defaults)[::-1][i]
        # 2. 按顺序填入arg宝石
        for i in range(len(args)):
            if self.__params_name[i] != "self":
                mapping[self.__params_name[i]] = args[i]
        # 3. 合并kwargs神秘包裹
        mapping.update(kwargs)
        return mapping

    @staticmethod
    def lang_checking(param):
        """🌐 语言小精灵的魔法转换"""
        if isinstance(param, str):
            return {"zh-CN": param, "en": param}  # 🐉 中英双龙护体
        elif isinstance(param, Lang):
            return param.convert()  # 🧚♀️ 调用语言精灵

    @staticmethod
    def match_datatype(anno):
        """🔮 类型翻译官的魔法词典"""
        if isinstance(anno, type):
            return data_mapping[str(anno)].__name__  # 📖 查基本类型字典
        elif isinstance(anno, typing._GenericAlias):  # noqa
            return data_mapping[str(anno)].__name__  # 🧩 处理泛型拼图
        elif isinstance(anno, typing.NewType):  # noqa
            return anno.__name__  # 🎭 揭开新类型面具
        else:
            log.warning(f"🆘 发现未知生物：{anno}, {str(type(anno))}")
            return "any"  # ❓ 贴上未知标签

    def match_annotated(self, annotated: typing._AnnotatedAlias):  # noqa
        """🎭 注解解谜大师的工作台"""
        param_type = annotated.__origin__  # 🧬 提取本体DNA
        others = ()
        enum = None

        # 📏 测量注解元数据长度
        annotated_length = len(annotated.__metadata__)
        if annotated_length < 2:
            raise PackError("❌ 注解能量不足！需要至少title和description两个符文")

        # 🎨 绘制基本信息
        title = annotated.__metadata__[0]
        description = annotated.__metadata__[1]

        if annotated_length >= 3:
            others = annotated.__metadata__[2:]  # 🎁 收集额外宝物

            # 🔍 寻找Literal藏宝图
            literal = next(filter(lambda x: typing.get_origin(x) is typing.Literal, others), None)
            if literal is not None:
                enum = typing.get_args(literal)  # 🎲 提取所有骰子面

        # 🧳 打包战利品
        res = {
            "title": self.lang_checking(title),
            "description": self.lang_checking(description),
            "type": (
                param_type.__name__
                if param_type.__class__.__name__ == "ModelMetaclass"
                else self.match_datatype(param_type)
            )
        }

        # 🎯 附加特殊效果
        if "print" in others:
            res["print"] = True  # 🖨️ 添加打印特效
        if enum is not None:
            res["enum"] = list(enum)  # 🎲 装入骰子集合

        return res

    def match_basemodel(self, annotation):
        """🏰 勇者尚未攻略的模型城堡（待优化）"""
        for k, v in annotation.items():
            if v.__class__.__name__ == "_AnnotatedAlias":
                if self._types.get(k) is None:
                    self._types[k] = self.match_annotated(v)  # ⚒️ 临时锻造工具

    @abc.abstractmethod
    def hook(self):
        """🔮 留给子类的魔法阵 | 在此绘制专属契约纹章"""
        ...
