# astrbot_plugin_calculator.py
# 适配 AstrBot 框架的「倍率 / 协力 PT / 单人 PT / 挑战 PT」计算插件
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Star, register
from astrbot.api import logger

# 建议：如需黑白名单，可在 data/config.yaml 中加同名节点自行扩展
@register("calculator", "YourName", "游戏数据计算器：倍率、协力/单人/挑战 PT", "1.0.0")
class CalculatorPlugin(Star):
    def __init__(self, context):
        super().__init__(context)

    async def initialize(self):
        logger.info("CalculatorPlugin loaded.")

    # --------------------------
    # 1. 倍率计算
    # --------------------------
    @filter.command("倍率")
    async def calc_power(self, event: AstrMessageEvent):
        raw = event.message_str
        # 去掉指令头 "/倍率"
        args_part = raw.lstrip().split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
        if not args_part:
            yield event.plain_result("计算需要卡组里面所有角色的技能倍率哦")
            return

        args = args_part.split()
        if len(args) != 5:
            msg = f"需要5张卡的倍率哦，你目前只输入了{len(args)}张卡" if len(args) < 5 else "队伍倍率超载了！"
            yield event.plain_result(msg)
            return

        try:
            a, b, c, d, e = map(float, args)
        except ValueError:
            yield event.plain_result("倍率里混进了奇怪的东西，麻烦你重新审查一遍之后再输入哦")
            return

        total = a + b + c + d + e
        avg_part = (b + c + d + e) / 5
        multiplier = (a + avg_part) / 100 + 1
        actual_value = a + avg_part

        result = (
            f"🎮📊 模拟卡组分析 📊🎮\n"
            f"• 队长加成: {a}\n"
            f"• 综合加成: {total}\n"
            f"• 最终倍率: {multiplier:.2f}\n"
            f"• 技能效果值: {actual_value}%"
        )
        yield event.plain_result(result)

    # --------------------------
    # 2. 协力 PT
    # --------------------------
    @filter.command("协力pt")
    async def calc_together_pt(self, event: AstrMessageEvent):
        raw = event.message_str
        args_part = raw.lstrip().split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
        if not args_part:
            yield event.plain_result("需要输入参数哦，没有参数无法计算的")
            return

        args = args_part.split()
        if len(args) != 4:
            msg = f"你只输入了{len(args)}个参数哦，一共需要4个参数才行" if len(args) < 4 else "协力 PT 超载了！"
            yield event.plain_result(msg)
            return

        try:
            a, c, d, e = map(float, args)
        except ValueError:
            yield event.plain_result("参数里混进了奇怪的东西，麻烦你重新审查一遍之后再输入哦")
            return

        b = 1_100_000
        pt_score = round(((114 + a / 17500 + b / 100000) * c * (d / 100 + 1)) * e)
        yield event.plain_result(
            f"🎮📊 协力模拟 PT 计算 📊🎮\n"
            f"• 活动协力 PT: {pt_score}"
        )

    # --------------------------
    # 3. 单人 PT
    # --------------------------
    @filter.command("单人pt")
    async def calc_solo_pt(self, event: AstrMessageEvent):
        raw = event.message_str
        args_part = raw.lstrip().split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
        if not args_part:
            yield event.plain_result("需要输入参数哦，没有参数无法计算的")
            return

        args = args_part.split()
        if len(args) != 4:
            msg = f"你只输入了{len(args)}个参数哦，一共需要4个参数才行" if len(args) < 4 else "单人 PT 超载了！"
            yield event.plain_result(msg)
            return

        try:
            a, b, c, d = map(float, args)
        except ValueError:
            yield event.plain_result("参数里混进了奇怪的东西，麻烦你重新审查一遍之后再输入哦")
            return

        pt_score = round(((100 + a / 20000) * b * (c / 100 + 1)) * d)
        yield event.plain_result(
            f"🎮📊 单人模拟 PT 计算 📊🎮\n"
            f"• 活动单人 PT: {pt_score}"
        )

    # --------------------------
    # 4. 挑战 PT
    # --------------------------
    @filter.command("挑战pt")
    async def calc_challenge_pt(self, event: AstrMessageEvent):
        raw = event.message_str
        args_part = raw.lstrip().split(maxsplit=1)[1] if len(raw.split()) > 1 else ""
        if not args_part:
            yield event.plain_result("需要输入参数哦，没有参数无法计算的")
            return

        args = args_part.split()
        if len(args) != 1:
            yield event.plain_result("挑战 PT 超载了！")
            return

        try:
            a = float(args[0])
        except ValueError:
            yield event.plain_result("参数里混进了奇怪的东西，麻烦你重新审查一遍之后再输入哦")
            return

        pt_score = round((100 + a / 20000) * 120)
        yield event.plain_result(
            f"🎮📊 挑战模拟 PT 计算 📊🎮\n"
            f"• 活动挑战 PT: {pt_score}"
        )

    async def terminate(self):
        logger.info("CalculatorPlugin unloaded.")