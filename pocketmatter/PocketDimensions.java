package com.pocketmatter;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * Lista das dimensoes de bolso. Cada nome aqui precisa ter um arquivo
 * data/pocketmatter/dimension/<nome>.json (gerado por tools/generate_content.py).
 * Para criar mais dimensoes: adicione o nome aqui E no script gerador.
 */
public final class PocketDimensions {
    public static final List<String> NAMES = List.of("black_pocket", "red_pocket", "mixed_pocket");

    private PocketDimensions() {}

    public static ResourceKey<Level> key(String name) {
        return ResourceKey.create(Registries.DIMENSION, new ResourceLocation(PocketMatter.MODID, name));
    }
}
