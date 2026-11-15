package com.pocketmatter.item;

import com.pocketmatter.PocketMatter;
import com.pocketmatter.registry.ModItems;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

/**
 * Cada constante vira um conjunto completo de armadura (4 pecas + 1 nucleo).
 * Para criar um conjunto novo: adicione uma constante aqui E no tools/generate_content.py,
 * depois rode o script para gerar texturas, receitas, modelos e traducoes.
 */
public enum MatterArmorMaterial implements ArmorMaterial {
    //   id        durab.  defesa [capacete, peitoral, calca, bota]  encant. tenacidade  knockback  bonus de set completo
    VOID  ("void",   40, new int[]{3, 6, 8, 3}, 18, 3.0F, 0.10F, MobEffects.NIGHT_VISION),
    EMBER ("ember",  42, new int[]{3, 6, 8, 3}, 20, 3.0F, 0.10F, MobEffects.FIRE_RESISTANCE),
    FROST ("frost",  38, new int[]{3, 6, 8, 3}, 20, 3.0F, 0.10F, MobEffects.WATER_BREATHING),
    GAIA  ("gaia",   48, new int[]{4, 7, 9, 4}, 16, 4.0F, 0.15F, MobEffects.REGENERATION),
    AETHER("aether", 36, new int[]{3, 6, 8, 3}, 24, 2.0F, 0.00F, MobEffects.SLOW_FALLING);

    private final String id;
    private final int durabilityMultiplier;
    private final int[] defense;
    private final int enchantmentValue;
    private final float toughness;
    private final float knockbackResistance;
    private final MobEffect setEffect;

    MatterArmorMaterial(String id, int durabilityMultiplier, int[] defense, int enchantmentValue,
                        float toughness, float knockbackResistance, MobEffect setEffect) {
        this.id = id;
        this.durabilityMultiplier = durabilityMultiplier;
        this.defense = defense;
        this.enchantmentValue = enchantmentValue;
        this.toughness = toughness;
        this.knockbackResistance = knockbackResistance;
        this.setEffect = setEffect;
    }

    public String id() {
        return id;
    }

    public MobEffect setEffect() {
        return setEffect;
    }

    @Override
    public int getDurabilityForType(ArmorItem.Type type) {
        int base = switch (type) {
            case HELMET -> 11;
            case CHESTPLATE -> 16;
            case LEGGINGS -> 15;
            case BOOTS -> 13;
        };
        return base * durabilityMultiplier;
    }

    @Override
    public int getDefenseForType(ArmorItem.Type type) {
        return switch (type) {
            case HELMET -> defense[0];
            case CHESTPLATE -> defense[1];
            case LEGGINGS -> defense[2];
            case BOOTS -> defense[3];
        };
    }

    @Override
    public int getEnchantmentValue() {
        return enchantmentValue;
    }

    @Override
    public SoundEvent getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_NETHERITE;
    }

    @Override
    public Ingredient getRepairIngredient() {
        return Ingredient.of(ModItems.CORES.get(this).get());
    }

    /** Vira o caminho da textura: pocketmatter:textures/models/armor/<id>_layer_1.png */
    @Override
    public String getName() {
        return PocketMatter.MODID + ":" + id;
    }

    @Override
    public float getToughness() {
        return toughness;
    }

    @Override
    public float getKnockbackResistance() {
        return knockbackResistance;
    }
}
