package com.pocketmatter;

import com.pocketmatter.registry.ModBlocks;
import com.pocketmatter.registry.ModCreativeTabs;
import com.pocketmatter.registry.ModItems;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(PocketMatter.MODID)
public class PocketMatter {
    public static final String MODID = "pocketmatter";

    public PocketMatter() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        ModBlocks.BLOCKS.register(bus);
        ModItems.ITEMS.register(bus);
        ModCreativeTabs.TABS.register(bus);
    }
}
