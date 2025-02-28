import os
import sys
import abc
import json
import yaml
import aiohttp
import requests
from enum import Enum
from typing import Union, Dict, List

# 本地召唤
from chariot_scaffold import plugin_spec
from chariot_scaffold.core.base import Base
from chariot_scaffold.core.config import Lang
from chariot_scaffold.exceptions import PackError
from chariot_scaffold.tools import generate_file, generate_online_pack, generate_offline_pack


# 🌌 时空结界调整 | 暂时解除SSL验证警报
# 🔮 魔法效果：
#   ✅ 抑制HTTPS请求的证书警告闪烁
#   ⚠️ 注意：此咒语会降低空间结界安全性
requests.packages.urllib3.disable_warnings()    # noqa


# region -------------------- 魔法枚举 & 混合类 --------------------
class TriggerType(str, Enum):
    """⏰ 时空裂隙的信使类型 | 红莲与星辉的契约"""
    ALARM = "alarm_receivers"   # 🔥 红莲信使：传递灼热告警的火焰凤凰
    ASSET = "asset_receivers"   # 💎 星辉信使：运送珍贵宝物的水晶独角兽


class InputProcessorMixin:
    """🔮 参数调和魔法阵 | 统一参数精灵的着装规范"""

    def __init__(self):
        self.input = None

    def _process_input(self, target: dict):
        """
        🎀 参数精灵换装仪式
        魔法流程：
          1. 为每个参数精灵穿上标准制服（标题+描述+类型）
          2. 佩戴可选配饰（必填徽章/默认值项链/枚举手环）
        """
        for param, info in self.input.items():
            entry = {
                'title': info['title'],
                'description': info['description'],
                'type': info['type']
            }
            # 可选字段魔法注入
            optional_fields = ['required', 'default', 'enum']
            for field in optional_fields:
                if field in info:
                    entry[field] = info[field]
            target[param] = entry

# endregion

# region -------------------- 核心类实现 --------------------
class Connection(Base, InputProcessorMixin):
    """🌈 星界虹桥 | 连接异次元的魔法通道"""

    def __init__(self, model=None):
        super().__init__(model=model)

    def hook(self):
        """✨ 虹桥落成典礼 | 将连接配置刻入世界树年轮"""
        plugin_spec.connection = {}
        self._process_input(plugin_spec.connection)


class Action(Base, InputProcessorMixin):
    """🎭 奥义法典 | 记载终极魔法的禁断卷轴"""

    def __init__(self, title=None, description=None, model=None, example=None):
        super().__init__(title, description, model)
        self.example = example

    def hook(self):
        """✨ 奥义封印解除 | 将技能信息写入虚空图书馆"""
        action_config = {
            'title': self.lang_checking(self.title),
            'description': self.lang_checking(self.description),
            'input': {},
            'output': self.output
        }

        self._process_input(action_config['input'])

        if self.example:
            action_config['example'] = self.example

        plugin_spec.actions[self._func_name] = action_config


class Trigger(Base, InputProcessorMixin):
    """⏰ 时空信标 | 定位维度裂隙的魔法坐标"""
    TRIGGER_MAP = {
        TriggerType.ALARM: plugin_spec.alarm_receivers,
        TriggerType.ASSET: plugin_spec.asset_receivers
    }

    def __init__(self, title=None, description=None, model=None,
                 trigger_type: TriggerType = TriggerType.ALARM):
        super().__init__(title, description, model)
        self.trigger_type = trigger_type

    def hook(self):
        """✨ 信标激活仪式 | 将触发器配置注入星界罗盘"""
        trigger_config = {
            'title': self.lang_checking(self.title),
            'description': self.lang_checking(self.description),
            'input': {}
        }

        self._process_input(trigger_config['input'])
        self.TRIGGER_MAP[self.trigger_type][self._func_name] = trigger_config


# endregion

# region -------------------- 触发器扩展类 --------------------
class SafeSession:
    """🔒 临时信使保管箱 | 管理一次性通信傀儡"""

    def __init__(self):
        self._session = None

    def __enter__(self):
        """🤖 召唤粘土傀儡 | 创建临时通信信使"""
        self._session = requests.Session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """🧹 傀儡净化术 | 将信使化为星尘回归自然"""
        if self._session:
            self._session.close()


class TriggerExtend:
    """🚀 星界通信塔 | 跨维度信息传递中枢"""
    def __init__(self, dispatcher_url: str, cache_url: str):
        """
        🗼 通信塔坐标锚定
        :param dispatcher_url: 中央调度塔魔网坐标 ✉️
        :param cache_url:      记忆水晶库空间坐标 💾
        """
        self.dispatcher_url = dispatcher_url
        self.cache_url = cache_url

    # region --------- 同步方法 ---------
    def send(self, alarm: dict) -> dict:
        """📤 同步空间折跃 | 即时传递告警信息"""
        with SafeSession() as session:
            response = session.post(self.dispatcher_url, json=alarm, verify=False)
            return response.json()

    def set_cache(self, data: dict) -> dict:
        """💾 同步记忆封印术 | 将数据刻入记忆水晶
        魔法流程：
        1. 召唤临时信使 🤖
        2. 将数据卷轴封印到水晶库 🧿
        3. 带回封印完成回执 📜
        魔法效果：数据将永久保存直至被解封
        """
        with SafeSession() as session:
            response = session.post(self.cache_url, json={'method': 'set', 'data': data}, verify=False)
            return response.json()

    def get_cache(self) -> dict:
        """📥 同步记忆召唤术 | 从水晶库解封记忆
        魔法流程：
          1. 召唤临时信使 🤖
          2. 向水晶库发送解封咒语 🔮
          3. 带回记忆卷轴的全息投影 🎞️
        特殊说明：不会破坏原始记忆封印
        """
        with SafeSession() as session:
            response = session.post(self.cache_url, json={'method': 'get'}, verify=False)
            return response.json()

    # endregion

    # region --------- 异步方法 ---------
    async def async_send(self, session: aiohttp.ClientSession, data: dict) -> dict:
        """⚡ 量子隧穿传递 | 非阻塞式跨维度通信"""
        async with session.post(self.dispatcher_url, json=data) as response:
            return await response.json()

    async def async_set_cache(self, session: aiohttp.ClientSession, data: dict) -> dict:
        """⚡ 异步量子封印 | 通过时空裂隙快速存储
        魔法特性：
          🌀 非阻塞式施法
          🌌 利用量子纠缠原理
          💫 适合高频快速存储
        魔法回执：返回时空裂隙的共鸣信号
        """
        async with session.post(self.cache_url, json={'method': 'set', 'data': data}) as response:
            return await response.json()

    async def async_get_cache(self, session: aiohttp.ClientSession) -> dict:
        """⚡ 异步记忆投影 | 从平行宇宙获取数据副本
        魔法亮点：
          🌠 零延迟跨维度访问
          🔮 自动维持数据一致性
          🧩 适合大规模并发读取
        特别提示：返回的是当前时空的数据快照
        """
        async with session.post(self.cache_url, json={'method': 'get'}) as response:
            return await response.json()

    # endregion


# endregion


# region -------------------- 核心插件类 --------------------
class Pack(metaclass=abc.ABCMeta):
    """📜 世界树幼苗 | 插件生态的核心生命体"""
    __platform: str = None

    def __init__(self):
        self.trigger_no_need_connection = False
        self.create_trigger_extend()
        self.before_startup()

    # --------- 抽象方法 ---------
    @abc.abstractmethod
    def connection(self, *args, **kwargs):
        """🔌 必须实现的连接方法"""
        pass

    def before_startup(self):
        """🚀 插件启动前准备"""
        pass

    def after_closing(self):
        """🔚 插件关闭后清理"""
        pass

    # --------- 配置管理 ---------
    @classmethod
    def plugin_config_init(
            cls,
            name: str,
            title: Union[str, Lang],
            description: Union[str, Lang],
            version: str = "0.1.0",
            tags: List[str] = None,
            vendor: str = "chariot",
            types: List[type] = None,
            platform: str = "linux/amd64",
            category: str = ""
    ):
        """
        🌱 幼苗培育仪式 | 定义插件的基因序列
        魔法流程：
          1. 真名契约认证（验证名称合法性）🔐
          2. 时空坐标锚定（自动获取入口文件）📍
          3. 基因序列注入（写入基础配置）🧬
          4. 记忆水晶铸造（解析自定义类型）💎

        基因要素：
          🧬 name    : 真名契约（必须符合魔法位面命名法则，字母/下划线开头）
          🎴 title   : 灵魂刻印（展示在魔法图鉴中的多语言名称）
          📜 description: 记忆碑文（刻在时空回廊的插件描述）
          🔢 version : 进化阶段（遵循X.Y.Z格式的神圣数字，如1.0.0）
          🏷️ tags    : 元素标签（用于魔法图鉴检索的标记符文）
          🧙 vendor  : 创造者印记（插件铸造者的魔法签名）
          🔮 types   : 自定义咒文（通过pydantic模型定义的特殊魔法类型）
          🏗️ platform: 架构神殿（镜像部署的位面坐标，默认linux/amd64）
          📦 category: 宝箱分类（在魔法仓库中的展示位置）

        魔法效果：
          ✅ 在时空裂隙中生成插件灵魂坐标
          ✅ 在记忆水晶库中固化配置信息
          ✅ 在魔法图鉴中注册可检索的插件档案
        """
        # 🌸 真名契约认证仪式
        # 🚨 检测名称是否符合魔法位面法则
        if not name.isidentifier():
            raise PackError("真名必须由字母/下划线组成，且不可亵渎魔法语法")
        if not all(v.count('.') == 2 for v in [version]):
            raise PackError("进化阶段需遵循X.Y.Z的神圣三元格式")

        cls.__platform = platform

        # 🌌 时空坐标锚定
        # 🧭 获取当前模块的星界坐标
        current_module = sys.modules[cls.__module__]
        # ✨ 提取入口真名并解除.py封印
        plugin_spec.entrypoint = os.path.basename(current_module.__file__).replace('.py', '')

        # 🧬 基因序列注入流程
        # 🏛️ 架构神殿坐标固化
        cls.__platform = platform
        plugin_spec.module = cls.__name__
        # 🔖 灵魂刻印注入（多语言标题）
        plugin_spec.title = cls.lang_checking(title) if title else cls.lang_checking(cls.__name__)
        # 🔢 进化阶段烙印
        plugin_spec.version = version if version else "0.1.0"
        # 📜 记忆碑文篆刻（多语言描述）
        plugin_spec.description = cls.lang_checking(description)

        plugin_spec.name = name
        # 🏷️ 元素标签附魔
        plugin_spec.tags = tags if tags else []
        # 🧙 创造者印记雕刻
        plugin_spec.vendor = vendor
        plugin_spec.type = category
        # 🔮 自定义咒文解析
        plugin_spec.types = cls._parse_custom_types(types)

    @classmethod
    def _parse_custom_types(cls, types: List[type]) -> Dict:
        """
        🔮 咒文解析仪式 | 破译自定义魔法的奥秘
        魔法流程：
        1. 遍历types魔法卷轴集合 📜
        2. 对每个卷轴进行「__annotations__」封印检查 🧿
        3. 将封印的符文转化为「标题+类型」的标准咒文格式 ✨
        4. 存入type_map记忆水晶库供后续召唤使用 💎

        魔法要素：
        📜 model: 魔法卷轴（包含字段定义的模型类）
        🔖 field: 卷轴符文（模型的字段名称）
        ⚗️ field_type: 元素属性（字段的数据类型）

        特殊效果：
        ✅ 自动将字段名称转化为多语言标题
        ✅ 提取字段类型的真名（__name__属性）
        ✅ 生成可供星界图鉴识别的标准格式

        示例咒文解析：
        原始卷轴 -> class User(BaseModel):
                   name: str
                   age: int
        解析结果 -> {
                 "User": {
                   "name": {"title": "name", "type": "str"},
                   "age": {"title": "age", "type": "int"}
                 }
               }
        """
        type_map = {}
        if types:
            for model in types:
                if hasattr(model, '__annotations__'):   # 🧿 卷轴封印检查
                    type_map[model.__name__] = {
                        field: {
                            'title': cls.lang_checking(field),  # 🌐 多语言转换
                            'type': field_type.__name__         # 🔍 提取类型真名
                        }
                        for field, field_type in model.__annotations__.items()
                    }
        return type_map      # 💎 返回充能完成的记忆水晶
    # endregion

    # region --------- 打包方法 ---------
    @classmethod
    def generate_online_pack(cls, path: str = None):
        """
        🌐 编织咒语卷轴 | 生成轻量级在线安装包
        核心特性：
          🧶 仅包含基础咒语（代码逻辑）
          ☁️ 依赖项需通过「pip」魔法网络实时召唤
          ⚡ 适合熟悉魔法网络的巫师快速部署

        魔法流程：
          1. 定位咒语卷轴本源（自动或指定路径）📍
          2. 验证本源存在性（路径合法性检测）🕵️♀️
          3. 编织轻量卷轴（生成.whl文件）📜

        典型场景：
          ✅ 已有稳定魔法依赖库的环境
          ✅ 需要快速更新咒语版本
          ✅ 网络畅通的云端部署
        """
        file_path = path or os.path.abspath(sys.modules[cls.__module__].__file__)
        if not os.path.exists(file_path):
            raise PackError("目标路径不存在喵～(>ω<)")
        generate_online_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version)

    @classmethod
    def generate_offline_pack(cls, path: str = None):
        """
        🧳 打造魔法宝箱 | 生成完整离线安装包
        核心特性：
          📦 包含全部咒语和依赖的镜像
          🛡️ 无需连接魔法网络（pip）
          🌍 支持多架构部署（x86/arm等）

        魔法流程：
          1. 锚定咒语本源坐标（自动或指定路径）📍
          2. 召唤「docker」镜像精灵 🧞♂️
          3. 铸造全量魔法宝箱（生成docker镜像）📦

        典型场景：
          ✅ 封闭的魔法结界（内网环境）
          ✅ 异构位面部署（不同CPU架构）
          ✅ 需要长期稳定运行的古老遗迹
        """
        file_path = path or os.path.abspath(sys.modules[cls.__module__].__file__)
        if not os.path.exists(file_path):
            raise PackError(f"目标路径不存在喵～(>_<): {file_path}")
        generate_offline_pack(file_path, plugin_spec.name, plugin_spec.vendor, plugin_spec.version, cls.__platform)

    def create_yaml(self, path=None):
        """
        🖋️ 撰写魔导书 | 生成plugin.spec.yaml
        魔法特性：
          1. 自动检测书写路径是否存在 📂
          2. 使用UTF-8魔法符文防止乱码 🔡
          3. 保持人类可读的诗意格式 📜
        """
        output_dir  =  path or "./"

        if not os.path.exists(output_dir):
            raise PackError(f"目标路径不存在喵～(>_<): {output_dir}")

        yaml_path = os.path.join(output_dir, "plugin.spec.yaml")
        with open(yaml_path, 'w', encoding='utf-8') as stream:
            yaml.safe_dump(
                self.json,
                stream,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False
            )

    def generate_project(self, path=None):
        """
        🏗️ 构筑魔法工坊 | 生成标准项目结构
        构筑流程：
          1. 先召唤魔导书（create_yaml）
          2. 再生成基础建筑（generate_file）
          3. 自动组装核心模块 🧩
        """
        self.create_yaml(path=path)
        generate_file(module=plugin_spec.module, entrypoint=plugin_spec.entrypoint, path=path)
    # endregion

    # region --------- 注册方法 ---------
    def create_trigger_extend(self):
        """⚡ 创建触发器扩展"""
        if any([plugin_spec.alarm_receivers, plugin_spec.asset_receivers]):
            self._safe_register(TriggerExtend, self.dispatcher_url, self.cache_url)

    def _safe_register(self, obj: object, *args, **kwargs):
        """🛡️ 安全注册方法"""
        instance = obj(*args, **kwargs)  # noqa
        for name in dir(instance):
            if not name.startswith('_') and callable(getattr(instance, name)):
                if hasattr(self, name):
                    raise PackError(f"方法名 {name} 与已有属性冲突啦～(≧∇≦)ﾉ")
                setattr(self, name, getattr(instance, name))

    # endregion

    # region --------- 属性管理 ---------
    @property
    def dispatcher_url(self) -> str:
        """📍 默认信使集散地 | 127.0.0.1:10001/transpond"""
        return "http://127.0.0.1:10001/transpond"

    @property
    def cache_url(self) -> str:
        """📦 默认缓存地址"""
        return "http://127.0.0.1:10001/cache"

    @dispatcher_url.setter
    def dispatcher_url(self, url):
        self.dispatcher_url = url

    @cache_url.setter
    def cache_url(self, url):
        self.cache_url = url

    @property
    def webhook_url(self):
        return ""

    @webhook_url.setter
    def webhook_url(self, url):
        self.webhook_url = url
    # endregion

    # region --------- 工具方法 ---------
    @staticmethod
    def lang_checking(param: Union[str, Lang]) -> Dict:
        """🌐 多语言通灵术 | 将文字转化为位面通用语"""
        if isinstance(param, str):
            return {'zh-CN': param, 'en': param}
        return param.convert()

    def __repr__(self) -> str:
        """🔍 友好显示配置"""
        return json.dumps(plugin_spec.dict(), indent=2, ensure_ascii=False)

    @property
    def yaml(self):
        return yaml.safe_dump(self.json, allow_unicode=True, sort_keys=False)

    @property
    def json(self):
        return plugin_spec.dict()

    # endregion

# endregion