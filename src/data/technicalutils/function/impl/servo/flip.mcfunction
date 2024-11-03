

scoreboard players set #temp_flip technicalutils.data 0

execute
    if entity @s[tag=technicalutils.servo.insert]
    run function ~/insert:
        scoreboard players set #temp_flip technicalutils.data 1
        tag @s remove technicalutils.servo.insert
        tag @s remove itemio.servo.insert
        tag @s add technicalutils.servo.extract
        tag @s add itemio.servo.extract
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/extract"
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/extract_connected"

execute
    unless score #temp_flip technicalutils.data matches 1
    if entity @s[tag=technicalutils.servo.extract]
    run function ~/extract:
        scoreboard players set #temp_flip technicalutils.data 1
        tag @s remove technicalutils.servo.extract
        tag @s remove itemio.servo.extract
        tag @s add technicalutils.servo.insert
        tag @s add itemio.servo.insert
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/insert"
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/insert_connected"


data modify entity @s ItemRotation set value 0b

playsound minecraft:block.stone.hit block @a