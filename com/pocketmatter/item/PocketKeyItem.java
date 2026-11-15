package com.pocketmatter.item;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class PocketKeyItem extends Item {
    private final String dimensionName;

    public PocketKeyItem(String dimensionName, Properties properties) {
        super(properties);
        this.dimensionName = dimensionName;
    }

    public String getDimensionName() {
        return dimensionName;
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.pocketmatter.key",
                Component.translatable("dimension.pocketmatter." + dimensionName)).withStyle(ChatFormatting.GRAY));
    }
}
