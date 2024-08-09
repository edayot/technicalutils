# @public
execute 
    if entity @s[tag=technicalutils.servo.extract]
    run function ./servo_update_good_extract:
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432002
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432003


execute
    if entity @s[tag=technicalutils.servo.insert]
    run function ./servo_update_good_insert:
        execute 
            if score @s itemio.math matches 0
            run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432004
        execute 
            if score @s itemio.math matches 1
            run data modify entity @s Item.components."minecraft:custom_model_data" set value 1432005