

execute 
    as @e[tag=technicalutils.block.lodestone,predicate=!technicalutils:block/destroy_lodestone] 
    at @s
    run function ./blocks/destroy_lodestone

execute 
    as @e[tag=technicalutils.block.conduit,predicate=!technicalutils:block/destroy_conduit] 
    at @s
    run function ./blocks/destroy_conduit


execute 
    as @e[type=item_frame,tag=technicalutils.servo.summoned]
    at @s run function technicalutils:impl/servo/place_entity
execute 
    as @e[type=item_frame,tag=technicalutils.servo] 
    unless data entity @s Item.count 
    run function technicalutils:impl/servo/destroy

execute as @e[type=item] if items entity @s container.0 *[minecraft:custom_data~{technicalutils:{servo:{}}}] at @s run function technicalutils:impl/servo/destroy_item

schedule function technicalutils:impl/tick 2t replace