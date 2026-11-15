package com.pocketmatter.registry;

import com.pocketmatter.PocketDimensions;
import com.pocketmatter.PocketMatter;
import com.pocketmatter.item.MatterArmorItem;
import com.pocketmatter.item.MatterArmorMaterial;
import com.pocketmatter.item.PocketKeyItem;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.Map;

public final class ModItems {
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, PocketMatter.MODID);

    // ---- Blocos ----
    public static final RegistryObject<Item> POCKET_PORTAL = ITEMS.register("pocket_portal",
            () -> new BlockItem(ModBlocks.POCKET_PORTAL.get(), new Item.Properties().rarity(Rarity.EPIC)));
    public static final RegistryObject<Item> BLACK_MATTER_STONE = ITEMS.register("black_matter_stone",
            () -> new BlockItem(ModBlocks.BLACK_MATTER_STONE.get(), new Item.Properties()));
    public static final RegistryObject<Item> RED_MATTER_STONE = ITEMS.register("red_matter_stone",
            () -> new BlockItem(ModBlocks.RED_MATTER_STONE.get(), new Item.Properties()));

    // ---- Chaves de dimensao (uma por dimensao de bolso) ----
    public static final Map<String, RegistryObject<Item>> KEYS = new LinkedHashMap<>();

    // ---- Nucleos e armaduras (um conjunto por MatterArmorMaterial) ----
    public static final Map<MatterArmorMaterial, RegistryObject<Item>> CORES = new EnumMap<>(MatterArmorMaterial.class);
    public static final Map<MatterArmorMaterial, Map<ArmorItem.Type, RegistryObject<Item>>> ARMOR =
            new EnumMap<>(MatterArmorMaterial.class);

    static {
        for (String dim : PocketDimensions.NAMES) {
            KEYS.put(dim, ITEMS.register(dim + "_key",
                    () -> new PocketKeyItem(dim, new Item.Properties().stacksTo(1).rarity(Rarity.EPIC))));
        }

        for (MatterArmorMaterial mat : MatterArmorMaterial.values()) {
            CORES.put(mat, ITEMS.register(mat.id() + "_core",
                    () -> new Item(new Item.Properties().rarity(Rarity.RARE))));

            Map<ArmorItem.Type, RegistryObject<Item>> pieces = new EnumMap<>(ArmorItem.Type.class);
            for (ArmorItem.Type type : ArmorItem.Type.values()) {
                pieces.put(type, ITEMS.register(mat.id() + "_" + type.getName(),
                        () -> new MatterArmorItem(mat, type,
                                new Item.Properties().fireResistant().rarity(Rarity.EPIC))));
            }
            ARMOR.put(mat, pieces);
        }
    }

    private ModItems() {}
}
