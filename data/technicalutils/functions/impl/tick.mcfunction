

execute 
    as @e[tag=technicalutils.block.lodestone,predicate=!technicalutils:block/destroy_lodestone] 
    at @s
    run function ./blocks/destroy_lodestone

schedule function technicalutils:impl/tick 2t replace