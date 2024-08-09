kill @e[limit=1,type=item,distance=..5,nbt={Age:0s,Item:{id:"minecraft:item_frame"}}]
kill @e[limit=1,type=item,distance=..5,nbt={Age:1s,Item:{id:"minecraft:item_frame"}}]


execute if items entity @s container.0 *[minecraft:custom_model_data=1432002] run loot spawn ~ ~ ~ loot technicalutils:impl/items/servo_extract
execute if items entity @s container.0 *[minecraft:custom_model_data=1432003] run loot spawn ~ ~ ~ loot technicalutils:impl/items/servo_extract
execute if items entity @s container.0 *[minecraft:custom_model_data=1432004] run loot spawn ~ ~ ~ loot technicalutils:impl/items/servo_insert
execute if items entity @s container.0 *[minecraft:custom_model_data=1432005] run loot spawn ~ ~ ~ loot technicalutils:impl/items/servo_insert


kill @s
function #itemio:calls/servos/destroy

playsound minecraft:block.stone.break block @a