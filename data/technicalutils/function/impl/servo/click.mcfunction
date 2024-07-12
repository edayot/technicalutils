
advancement revoke @s only technicalutils:impl/click

scoreboard players set #holding_wrench technicalutils.data 0
scoreboard players set #holding_id_filter technicalutils.data 0
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{smithed:{id:"technicalutils:wrench"}}] run scoreboard players set #holding_wrench technicalutils.data 1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{smithed:{id:"technicalutils:id_filter"}}] run scoreboard players set #holding_id_filter technicalutils.data 1



tag @s add technicalutils.me

execute
    if score #holding_wrench technicalutils.data matches 0
    if score #holding_id_filter technicalutils.data matches 0
    as @e[tag=technicalutils.servo,distance=..10]
    unless data entity @s {ItemRotation:0b}
    run function technicalutils:impl/servo/flip

execute
    if score #holding_wrench technicalutils.data matches 1
    as @e[tag=technicalutils.servo,distance=..10]
    unless data entity @s {ItemRotation:0b}
    run function technicalutils:impl/servo/print_filters

execute
    if score #holding_id_filter technicalutils.data matches 1
    as @e[tag=technicalutils.servo,distance=..10]
    unless data entity @s {ItemRotation:0b}
    run function technicalutils:impl/servo/apply_filters


tag @s remove technicalutils.me

playsound minecraft:block.stone.hit block @a