
execute at @s run kill @e[limit=1,type=item,distance=..5,nbt={Age:0s,Item:{id:"minecraft:item_frame"}}]



execute if items entity @s container.0 *[minecraft:custom_model_data=1432002] at @s run loot spawn ~ ~ ~ loot technicalutils:items/servo_extract
execute if items entity @s container.0 *[minecraft:custom_model_data=1432003] at @s run loot spawn ~ ~ ~ loot technicalutils:items/servo_extract
execute if items entity @s container.0 *[minecraft:custom_model_data=1432004] at @s run loot spawn ~ ~ ~ loot technicalutils:items/servo_insert
execute if items entity @s container.0 *[minecraft:custom_model_data=1432005] at @s run loot spawn ~ ~ ~ loot technicalutils:items/servo_insert


kill @s
function #itemio:calls/servos/destroy