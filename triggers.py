from chara.core.hazard import PLUGINS
from chara.lib.commandparse import CommandParser
from chara.onebot.events import GroupMessageEvent,  PrivateMessageEvent
from chara.plugin import command_trigger, regex_trigger
from chara.plugin import Handler, CommandTriggerCapturedData, RegexTriggerCapturedData
from chara.plugin import Bot
from chara.plugin import SU, Frequency
from chara.plugin import get_current_plugin


trigger_1 = regex_trigger(r'插件\s*(?P<index>\d+)', priority=0, block=True)
trigger_2 = regex_trigger(r'插件', priority=1) # 不会被触发

@trigger_1.handle(condition=Frequency(3, 10)) # 条件也可对handler使用
async def _(handler: Handler, bot: Bot, event: GroupMessageEvent, tcd: RegexTriggerCapturedData) -> None: # 不必使用所有参数
    data = tcd.matched.groupdict()
    index = int(data['index'])
    if index > len(PLUGINS):
        await handler.done('插件序号过大') 
    
    plugin = list(PLUGINS.values())[index-1]
    await handler.send(plugin.metadata.description)

# 多个handler会依次执行
@trigger_1.handle(condition=Frequency(3, 10))
async def _(event: PrivateMessageEvent): # handler会检查参数类型，消息事件为GroupMessageEvent时，此handler不会执行
    pass

cp0 = CommandParser('插件')
cp1 = CommandParser('用法')
cp2 = CommandParser('作者')
cp0.add_sub_parser(cp1)
cp0.add_sub_parser(cp2)
cp1.add_postion_argument(1, int)
cp2.add_postion_argument(1, int)


trigger_3 = command_trigger(cp0, priority=0, block=True)
async def _(tcd: CommandTriggerCapturedData):
    result = tcd.result
    result.posargs
    pass

trigger_4 = regex_trigger(r'关闭', condition=SU)

@trigger_4.handle
async def _():
    trigger_4.alive = False # 会在所有handler执行完后删除
    trigger_4.kill() # 立即停止执行并删除
    print('不会发生')
    

plugin = get_current_plugin()

@plugin.on_load()
async def _():
    # 在导入该插件时所做的事
    pass

@plugin.on_load(priority=1) # 使用priority确保执行顺序晚于上一个
async def _():
    pass

# 导入插件时会在全局变量里寻找trigger，确保你的trigger在__init__.py的全局变量中
__all__ = [
    'trigger_1',
    'trigger_2',
    'trigger_3',
]