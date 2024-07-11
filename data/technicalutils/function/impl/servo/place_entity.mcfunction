tag @s remove technicalutils.servo.summoned
execute if entity @s[tag=technicalutils.servo.extract] run tag @s add itemio.servo.extract
execute if entity @s[tag=technicalutils.servo.insert] run tag @s add itemio.servo.insert

tag @s add technicalutils.servo

data merge entity @s {Invulnerable:false,Invisible:true,Fixed:false,Silent:true}

data modify entity @s Item set value {id:"minecraft:light_gray_stained_glass_pane",count:1,components:{"minecraft:custom_data":{technicalutils:{servo:{placed:1}}}}}
execute if entity @s[tag=technicalutils.servo.extract] run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432002
execute if entity @s[tag=technicalutils.servo.insert] run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432004


scoreboard players set @s itemio.servo.stack_limit 1
scoreboard players set @s itemio.servo.retry_limit 1






function #itemio:calls/servos/init