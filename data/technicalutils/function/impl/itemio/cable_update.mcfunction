# @public


scoreboard players set #model technicalutils.data 1430000

scoreboard players operation #model technicalutils.data += @s itemio.math
item modify entity @s container.0 {"function": "minecraft:set_custom_model_data","value": {"type": "minecraft:score","target": {"type": "minecraft:fixed","name": "#model"},"score": "technicalutils.data","scale": 1}}