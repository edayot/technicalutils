# @public
execute 
    if entity @s[tag=technicalutils.servo.extract]
    run function ./servo_update_good_extract:
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/extract"
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/extract_connected"


execute
    if entity @s[tag=technicalutils.servo.insert]
    run function ./servo_update_good_insert:
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/insert"
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:item_model" set value "technicalutils:servo/insert_connected"