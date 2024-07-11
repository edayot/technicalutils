

execute 
    as @e[type=item_display,tag=technicalutils.block.lodestone,predicate=!technicalutils:block/destroy_lodestone] 
    at @s
    run function ./blocks/destroy_lodestone

execute 
    as @e[type=item_display,tag=technicalutils.block.conduit,predicate=!technicalutils:block/destroy_conduit] 
    at @s
    run function ./blocks/destroy_conduit

execute 
    as @e[type=item_display,tag=technicalutils.block.conduit,predicate=!technicalutils:block/underwater_conduit] 
    at @s
    run function ./blocks/underwater_conduit


execute 
    as @e[type=item_frame,tag=technicalutils.servo] 
    unless items entity @s contents *[minecraft:custom_data~{technicalutils:{servo:{placed:1}}}]
    run function technicalutils:impl/servo/destroy



schedule function technicalutils:impl/tick 2t replace