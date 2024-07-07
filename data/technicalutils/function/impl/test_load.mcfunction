


function technicalutils:impl/load



execute 
    if data storage smithed.crafter:input recipe{
            0: [
                {components: {"minecraft:custom_data": {smithed: {id: "technicalutils:silver_ingot"}}}, Slot: 0b}, {id: "minecraft:comparator", Slot: 1b}, {components: {"minecraft:custom_data": {smithed: {id: "technicalutils:silver_ingot"}}}, Slot: 2b}], 
            1: [{id: "minecraft:air", Slot: 0b}, {id: "minecraft:redstone_block", Slot: 1b}, {id: "minecraft:air", Slot: 2b}]
        } 
    if data storage smithed.crafter:input {2: []} 
    run loot replace block ~ ~ ~ container.16 loot technicalutils:items/servo_insert
