package com.pocketmatter.item;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

public class MatterArmorItem extends ArmorItem {
    private final MatterArmorMaterial matter;

    public MatterArmorItem(MatterArmorMaterial material, Type type, Properties properties) {
        super(material, type, properties);
        this.matter = material;
    }

    /** Bonus de set completo: so o capacete aplica, 1 vez por segundo, para nao repetir 4x. */
    @Override
    public void onArmorTick(ItemStack stack, Level level, Player player) {
        if (level.isClientSide || getType() != Type.HELMET || player.tickCount % 20 != 0) {
            return;
        }

        int pieces = 0;
        for (ItemStack armorStack : player.getArmorSlots()) {
            if (armorStack.getItem() instanceof MatterArmorItem other && other.matter == this.matter) {
                pieces++;
            }
        }
        if (pieces < 4) {
            return;
        }

        MobEffect effect = matter.setEffect();
        // duracao 260 ticks (13s) > 10s, entao o efeito nao fica piscando
        player.addEffect(new MobEffectInstance(effect, 260, 0, true, false, true));
    }
}
