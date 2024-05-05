

execute 
    as @e[tag=technicalutils.block.lodestone] 
    at @s
    unless block ~ ~ ~ lodestone
    run function ./blocks/destroy_lodestone

schedule function technicalutils:impl/tick 1t replace