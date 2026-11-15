package com.pocketmatter.world;

import com.pocketmatter.PocketDimensions;
import com.pocketmatter.PocketMatter;
import com.pocketmatter.registry.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;

public final class PocketTeleporter {
    private static final String ORIGIN_TAG = PocketMatter.MODID + "_origin";

    private PocketTeleporter() {}

    public static boolean isInPocket(Level level) {
        return level.dimension().location().getNamespace().equals(PocketMatter.MODID);
    }

    public static void enter(ServerPlayer player, String dimensionName) {
        MinecraftServer server = player.getServer();
        if (server == null) {
            return;
        }

        ServerLevel target = server.getLevel(PocketDimensions.key(dimensionName));
        if (target == null) {
            player.displayClientMessage(
                    Component.translatable("message.pocketmatter.dimension_missing", dimensionName), false);
            return;
        }

        saveOrigin(player);
        BlockPos arrival = prepareArrival(target);
        player.teleportTo(target, arrival.getX() + 0.5D, arrival.getY(), arrival.getZ() + 0.5D,
                player.getYRot(), player.getXRot());
        player.resetFallDistance();
    }

    public static void leave(ServerPlayer player) {
        MinecraftServer server = player.getServer();
        if (server == null) {
            return;
        }

        ServerLevel destination = null;
        BlockPos pos = null;

        CompoundTag data = player.getPersistentData();
        if (data.contains(ORIGIN_TAG, Tag.TAG_COMPOUND)) {
            CompoundTag origin = data.getCompound(ORIGIN_TAG);
            ResourceKey<Level> key = ResourceKey.create(Registries.DIMENSION,
                    new ResourceLocation(origin.getString("dim")));
            destination = server.getLevel(key);
            pos = new BlockPos(origin.getInt("x"), origin.getInt("y"), origin.getInt("z"));
        }

        // sem origem salva (ou dimensao de origem sumiu): volta pro spawn do Overworld
        if (destination == null || pos == null) {
            destination = server.overworld();
            pos = destination.getSharedSpawnPos();
        }

        player.teleportTo(destination, pos.getX() + 0.5D, pos.getY(), pos.getZ() + 0.5D,
                player.getYRot(), player.getXRot());
        player.resetFallDistance();
    }

    private static void saveOrigin(ServerPlayer player) {
        CompoundTag origin = new CompoundTag();
        origin.putString("dim", player.level().dimension().location().toString());
        BlockPos pos = player.blockPosition();
        origin.putInt("x", pos.getX());
        origin.putInt("y", pos.getY());
        origin.putInt("z", pos.getZ());
        player.getPersistentData().put(ORIGIN_TAG, origin);
    }

    /** Garante um portal de volta perto do ponto de chegada e devolve onde o jogador deve aparecer. */
    private static BlockPos prepareArrival(ServerLevel level) {
        level.getChunk(0, 0); // forca a geracao do chunk
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, 0, 0);

        BlockPos portalPos = new BlockPos(0, y, 2);
        if (!level.getBlockState(portalPos).is(ModBlocks.POCKET_PORTAL.get())) {
            level.setBlockAndUpdate(portalPos, ModBlocks.POCKET_PORTAL.get().defaultBlockState());
        }
        return new BlockPos(0, y, 0);
    }
}
