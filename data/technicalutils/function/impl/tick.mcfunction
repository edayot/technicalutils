

execute 
    as @e[tag=technicalutils.block.lodestone,predicate=!technicalutils:block/destroy_lodestone] 
    at @s
    run function ./blocks/destroy_lodestone

execute 
    as @e[tag=technicalutils.block.conduit,predicate=!technicalutils:block/destroy_conduit] 
    at @s
    run function ./blocks/destroy_conduit

schedule function technicalutils:impl/tick 2t replace