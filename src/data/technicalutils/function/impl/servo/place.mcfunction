advancement revoke @s only technicalutils:impl/place_item_frame

execute 
    as @e[type=item_frame,tag=technicalutils.servo.summoned,distance=..10]
    at @s 
    run function technicalutils:impl/servo/place_entity