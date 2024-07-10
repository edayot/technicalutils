# @public


execute 
    if entity @s[scores={smithed.data=0}] 
    if score count smithed.data matches 2
    if data storage smithed.crafter:input {recipe: [{components: {"minecraft:custom_data": {smithed: {id: "technicalutils:id_filter"}}}, count: 1}]}
    run function ~/id_filter