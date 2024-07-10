
advancement revoke @s only technicalutils:impl/click

scoreboard players set #holding_wrench technicalutils.data 0
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{smithed:{id:"technicalutils:wrench"}}] run scoreboard players set #holding_wrench technicalutils.data 1



tag @s add technicalutils.me

execute
    if score #holding_wrench technicalutils.data matches 0
    as @e[tag=technicalutils.servo,distance=..10]
    unless data entity @s {ItemRotation:0b}
    run function technicalutils:impl/servo/flip

execute
    if score #holding_wrench technicalutils.data matches 1
    as @e[tag=technicalutils.servo,distance=..10]
    unless data entity @s {ItemRotation:0b}
    run function technicalutils:impl/servo/print_filters


tag @s remove technicalutils.me

