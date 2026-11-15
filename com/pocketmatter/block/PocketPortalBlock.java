package com.pocketmatter.block;

import com.pocketmatter.item.PocketKeyItem;
import com.pocketmatter.world.PocketTeleporter;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Fora de uma dimensao de bolso: clique com uma Chave de Bolso na mao para entrar.
 * Dentro de uma dimensao de bolso: clique (qualquer mao) para voltar.
 */
public class PocketPortalBlock extends Block {
    public PocketPortalBlock(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player,
                                 InteractionHand hand, BlockHitResult hit) {
        if (level.isClientSide) {
            return InteractionResult.SUCCESS;
        }
        if (!(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResult.PASS;
        }

        if (PocketTeleporter.isInPocket(level)) {
            PocketTeleporter.leave(serverPlayer);
            return InteractionResult.CONSUME;
        }

        // procura a chave nas duas maos
        for (InteractionHand h : InteractionHand.values()) {
            ItemStack held = player.getItemInHand(h);
            if (held.getItem() instanceof PocketKeyItem key) {
                PocketTeleporter.enter(serverPlayer, key.getDimensionName());
                return InteractionResult.CONSUME;
            }
        }

        player.displayClientMessage(Component.translatable("message.pocketmatter.need_key"), true);
        return InteractionResult.CONSUME;
    }
}
