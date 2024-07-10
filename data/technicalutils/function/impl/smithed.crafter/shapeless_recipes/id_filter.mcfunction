

scoreboard players set @s smithed.data 1

data modify storage technicalutils:main temp.recipe set value []
data modify storage technicalutils:main temp.recipe set from storage smithed.crafter:input recipe

data remove storage technicalutils:main temp.result
data modify storage technicalutils:main temp.result set from storage technicalutils:main temp.recipe[{components: {"minecraft:custom_data": {smithed: {id: "technicalutils:id_filter"}}}, count: 1}]
data modify storage technicalutils:main temp.result.Slot set value 16b


data remove storage technicalutils:main temp.recipe[{components: {"minecraft:custom_data": {smithed: {id: "technicalutils:id_filter"}}}}]
data modify storage technicalutils:main temp.filter set from storage technicalutils:main temp.recipe[0]

execute 
    unless data storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters 
    run data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters set value []



execute
    store result score #if_ctc technicalutils.data 
    if data storage technicalutils:main temp.filter.components."minecraft:custom_data".ctc

execute
    store result score #if_smithed_id technicalutils.data 
    if data storage technicalutils:main temp.filter.components."minecraft:custom_data".smithed.id


execute
    if score #if_smithed_id technicalutils.data matches 1 
    run function ~/smithed_id

execute
    if score #if_smithed_id technicalutils.data matches 0
    if score #if_ctc technicalutils.data matches 1
    run function ~/ctc

execute
    if score #if_smithed_id technicalutils.data matches 0
    if score #if_ctc technicalutils.data matches 0
    run function ~/id

function ~/id:
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters prepend value {id: []}
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters[0].id append from storage technicalutils:main temp.filter.id

function ~/smithed_id:
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters prepend value {smithed: {id: []}}
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters[0].smithed.id append from storage technicalutils:main temp.filter.components."minecraft:custom_data".smithed.id

function ~/ctc:
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters prepend value {ctc: [{}]}
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters[0].ctc[0].id set from storage technicalutils:main temp.filter.components."minecraft:custom_data".ctc.id
    data modify storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters[0].ctc[0].from set from storage technicalutils:main temp.filter.components."minecraft:custom_data".ctc.from
    


data modify block ~ ~ ~ Items append from storage technicalutils:main temp.result

data modify storage smithed.crafter:input flags append value "technicalutils:filter_not_consume"


data remove storage technicalutils:main temp.filters
data modify storage technicalutils:main temp.filters set from storage technicalutils:main temp.result.components."minecraft:custom_data".technicalutils.filters

item modify block ~ ~ ~ container.16 technicalutils:impl/set_filter_lore_start

execute 
    if data storage technicalutils:main temp.filters[0] 
    run function ~/loop_filters:
        item modify block ~ ~ ~ container.16 technicalutils:impl/set_filter_lore_middle

        data remove storage technicalutils:main temp.filters[0]
        execute if data storage technicalutils:main temp.filters[0] run function ./id_filter/loop_filters

item modify block ~ ~ ~ container.16 technicalutils:impl/set_filter_lore_end


