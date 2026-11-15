#!/usr/bin/env python3
"""
Gera TODOS os arquivos de dados/recursos do mod Pocket Matter:
texturas, modelos, blockstates, traducoes, receitas, loot tables, tags e dimensoes.

Uso (na raiz do projeto):   python3 tools/generate_content.py
Requer: pip install pillow

Para adicionar conteudo, edite as listas ARMOR_SETS e DIMENSIONS abaixo
e rode de novo. Depois lembre de espelhar no Java:
  - novo conjunto de armadura  -> nova constante em MatterArmorMaterial.java
  - nova dimensao              -> novo nome em PocketDimensions.java
"""
import json
import math
import os
import random
import zlib
from PIL import Image

MODID = "pocketmatter"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources")
ASSETS = os.path.join(ROOT, "assets", MODID)
DATA = os.path.join(ROOT, "data", MODID)
MC_DATA = os.path.join(ROOT, "data", "minecraft")

DM = "projecte:dark_matter"
RM = "projecte:red_matter"

# --------------------------------------------------------------------------------------
# CONFIGURACAO  (edite aqui)
# --------------------------------------------------------------------------------------
# colors = (escuro, medio, claro)
ARMOR_SETS = [
    dict(id="void", en="Void Matter", pt="Matéria do Vazio",
         colors=("#1c1030", "#4a2c6e", "#a47ae0"),
         core=[DM, DM, "minecraft:ender_pearl", "minecraft:obsidian"]),
    dict(id="ember", en="Ember Matter", pt="Matéria Ardente",
         colors=("#5a1408", "#b3361a", "#ffa040"),
         core=[RM, "minecraft:magma_block", "minecraft:blaze_rod", "minecraft:blaze_powder"]),
    dict(id="frost", en="Frost Matter", pt="Matéria Gélida",
         colors=("#16384a", "#3a8fb0", "#c4f6ff"),
         core=[DM, "minecraft:blue_ice", "minecraft:blue_ice", "minecraft:prismarine_crystals"]),
    dict(id="gaia", en="Gaia Matter", pt="Matéria de Gaia",
         colors=("#173a1a", "#3e8b45", "#b6f2a0"),
         core=[DM, RM, "minecraft:emerald", "minecraft:golden_apple"]),
    dict(id="aether", en="Aether Matter", pt="Matéria do Éter",
         colors=("#6e5518", "#d9b53a", "#fff6c0"),
         core=[RM, RM, "minecraft:phantom_membrane", "minecraft:feather"]),
]

# effects = tipo de renderizacao do ceu: minecraft:overworld | the_nether | the_end
# layers  = camadas do chao, de baixo pra cima (o mundo comeca em y=0)
DIMENSIONS = [
    dict(id="black_pocket", en="Black Matter Pocket", pt="Bolso da Matéria Negra",
         effects="minecraft:the_end", ambient=0.1, fixed_time=18000, biome="minecraft:the_void",
         layers=[("minecraft:bedrock", 1), (f"{MODID}:black_matter_stone", 6)],
         key=[DM, DM, "minecraft:ender_pearl", "minecraft:stick"],
         key_colors=("#1c1030", "#4a2c6e", "#a47ae0")),
    dict(id="red_pocket", en="Red Matter Pocket", pt="Bolso da Matéria Vermelha",
         effects="minecraft:the_nether", ambient=0.2, fixed_time=6000, biome="minecraft:the_void",
         layers=[("minecraft:bedrock", 1), (f"{MODID}:red_matter_stone", 6)],
         key=[RM, RM, "minecraft:ender_pearl", "minecraft:stick"],
         key_colors=("#5a0a10", "#c02030", "#ff8090")),
    dict(id="mixed_pocket", en="Twin Matter Pocket", pt="Bolso da Matéria Gêmea",
         effects="minecraft:overworld", ambient=0.1, fixed_time=13000, biome="minecraft:the_void",
         layers=[("minecraft:bedrock", 1), (f"{MODID}:black_matter_stone", 2), (f"{MODID}:red_matter_stone", 2),
                 (f"{MODID}:black_matter_stone", 2), (f"{MODID}:red_matter_stone", 2)],
         key=[DM, RM, "minecraft:ender_pearl", "minecraft:stick"],
         key_colors=("#2a1030", "#8a2050", "#ff90c0")),
]

PIECES = [("helmet", "Helmet", "Capacete"), ("chestplate", "Chestplate", "Peitoral"),
          ("leggings", "Leggings", "Calças"), ("boots", "Boots", "Botas")]

PORTAL_RECIPE = dict(pattern=["DRD", "RER", "DRD"], key={"D": DM, "R": RM, "E": "minecraft:ender_eye"})

# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------
def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def scale(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def save_png(img, *parts):
    path = os.path.join(ASSETS, "textures", *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def ing(item):
    return {"item": item}


# --------------------------------------------------------------------------------------
# texturas
# --------------------------------------------------------------------------------------
MASKS = {
    "helmet": [
        "................",
        "................",
        "....########....",
        "...##########...",
        "..############..",
        "..############..",
        "..############..",
        "..###......###..",
        "..###......###..",
        "..##........##..",
    ],
    "chestplate": [
        "................",
        "..####....####..",
        ".#####....#####.",
        ".#####.##.#####.",
        ".#####.##.#####.",
        ".#####.##.#####.",
        "..####.##.####..",
        "..############..",
        "..############..",
        "..############..",
        "...##########...",
        "...##########...",
    ],
    "leggings": [
        "................",
        "..############..",
        "..############..",
        "..############..",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        "..###......###..",
    ],
    "boots": [
        "................",
        "................",
        "................",
        "................",
        "..####....####..",
        "..####....####..",
        "..####....####..",
        ".#####....#####.",
        ".#####....#####.",
        ".#####....#####.",
    ],
    "core": [
        "................",
        "................",
        "......####......",
        "....########....",
        "...##########...",
        "..############..",
        "..############..",
        "...##########...",
        "....########....",
        ".....######.....",
        "......####......",
    ],
    "key": [
        "................",
        "......####......",
        ".....######.....",
        ".....##..##.....",
        ".....##..##.....",
        ".....######.....",
        "......####......",
        ".......##.......",
        ".......##.......",
        ".......####.....",
        ".......##.......",
        ".......####.....",
        ".......##.......",
        ".......##.......",
    ],
}


def render_mask(rows, colors, seed):
    dark, mid, light = (hexrgb(c) for c in colors)
    rnd = random.Random(seed)
    h = len(rows)
    off = (16 - h) // 2
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    grid = [[(x < len(r) and r[x] == "#") for x in range(16)] for r in rows]

    def inside(x, y):
        return 0 <= y < h and 0 <= x < 16 and grid[y][x]

    for y in range(h):
        for x in range(16):
            if not grid[y][x]:
                continue
            border = not (inside(x - 1, y) and inside(x + 1, y) and inside(x, y - 1) and inside(x, y + 1))
            if border:
                c = scale(dark, 0.7)
            else:
                t = y / max(1, h - 1)
                c = light if (y < h * 0.35 and (x + y) % 3 == 0) else mid
                if t > 0.7 and rnd.random() < 0.4:
                    c = dark
                if rnd.random() < 0.08:
                    c = light
            img.putpixel((x, min(15, y + off)), c + (255,))
    return img


def armor_layer(colors, seed):
    dark, mid, light = (hexrgb(c) for c in colors)
    rnd = random.Random(seed)
    img = Image.new("RGBA", (64, 32))
    for y in range(32):
        for x in range(64):
            r = rnd.random()
            c = dark if r < 0.12 else (light if r > 0.90 else mid)
            if y % 8 == 7:
                c = scale(c, 0.75)          # "costuras" horizontais
            if x % 16 in (0, 15):
                c = scale(c, 0.85)
            img.putpixel((x, y), c + (255,))
    return img


def block_stone(base, spots, seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = base
            r = rnd.random()
            if r < 0.18:
                c = spots[0]
            elif r > 0.90:
                c = spots[1]
            img.putpixel((x, y), c + (255,))
    return img


def portal_texture():
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            r = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            if r > 9.2:
                c = (190, 25, 35)                 # manchas vermelhas (Red Matter) nos cantos
            else:
                c = (92, 42, 150)                 # fundo roxo
                if ((a + r * 0.9) % (2 * math.pi)) < 1.0:
                    c = (205, 165, 255)           # espiral clara
                if r < 1.6:
                    c = (245, 235, 255)
            if x in (0, 15) or y in (0, 15):
                c = scale(c, 0.55)
            img.putpixel((x, y), c + (255,))
    return img


# --------------------------------------------------------------------------------------
# geracao
# --------------------------------------------------------------------------------------
def gen_textures():
    for s in ARMOR_SETS:
        for i, (piece, _, _) in enumerate(PIECES):
            save_png(render_mask(MASKS[piece], s["colors"], zlib.crc32((s["id"] + piece).encode()) & 0xFFFF), "item", f"{s['id']}_{piece}.png")
        save_png(render_mask(MASKS["core"], s["colors"], 7), "item", f"{s['id']}_core.png")
        save_png(armor_layer(s["colors"], 11), "models", "armor", f"{s['id']}_layer_1.png")
        save_png(armor_layer(s["colors"], 23), "models", "armor", f"{s['id']}_layer_2.png")
    for d in DIMENSIONS:
        save_png(render_mask(MASKS["key"], d["key_colors"], 3), "item", f"{d['id']}_key.png")
    save_png(block_stone((22, 16, 30), [(46, 30, 70), (12, 8, 18)], 1), "block", "black_matter_stone.png")
    save_png(block_stone((118, 16, 22), [(190, 44, 44), (62, 8, 12)], 2), "block", "red_matter_stone.png")
    save_png(portal_texture(), "block", "pocket_portal.png")


def item_model(name):
    write_json(os.path.join(ASSETS, "models", "item", f"{name}.json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{name}"}})


def block_assets(name):
    write_json(os.path.join(ASSETS, "blockstates", f"{name}.json"),
               {"variants": {"": {"model": f"{MODID}:block/{name}"}}})
    write_json(os.path.join(ASSETS, "models", "block", f"{name}.json"),
               {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MODID}:block/{name}"}})
    write_json(os.path.join(ASSETS, "models", "item", f"{name}.json"),
               {"parent": f"{MODID}:block/{name}"})
    write_json(os.path.join(DATA, "loot_tables", "blocks", f"{name}.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0,
                   "entries": [{"type": "minecraft:item", "name": f"{MODID}:{name}"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}],
    })


def gen_models():
    for s in ARMOR_SETS:
        for piece, _, _ in PIECES:
            item_model(f"{s['id']}_{piece}")
        item_model(f"{s['id']}_core")
    for d in DIMENSIONS:
        item_model(f"{d['id']}_key")
    for b in ("black_matter_stone", "red_matter_stone", "pocket_portal"):
        block_assets(b)


def shaped(path, pattern, key, result, count=1, category="equipment"):
    write_json(path, {"type": "minecraft:crafting_shaped", "category": category, "pattern": pattern,
                      "key": {k: ing(v) for k, v in key.items()},
                      "result": {"item": result, "count": count}})


def shapeless(path, items, result, count=1, category="misc"):
    write_json(path, {"type": "minecraft:crafting_shapeless", "category": category,
                      "ingredients": [ing(i) for i in items],
                      "result": {"item": result, "count": count}})


def gen_recipes():
    rec = os.path.join(DATA, "recipes")
    for s in ARMOR_SETS:
        core = f"{MODID}:{s['id']}_core"
        shapeless(os.path.join(rec, f"{s['id']}_core.json"), s["core"], core, count=2)
        shapes = {"helmet": ["CCC", "C C"], "chestplate": ["C C", "CCC", "CCC"],
                  "leggings": ["CCC", "C C", "C C"], "boots": ["C C", "C C"]}
        for piece, _, _ in PIECES:
            shaped(os.path.join(rec, f"{s['id']}_{piece}.json"), shapes[piece], {"C": core},
                   f"{MODID}:{s['id']}_{piece}")
    for d in DIMENSIONS:
        shapeless(os.path.join(rec, f"{d['id']}_key.json"), d["key"], f"{MODID}:{d['id']}_key")
    shaped(os.path.join(rec, "pocket_portal.json"), PORTAL_RECIPE["pattern"], PORTAL_RECIPE["key"],
           f"{MODID}:pocket_portal", category="misc")
    shapeless(os.path.join(rec, "black_matter_stone.json"), [DM] + ["minecraft:cobblestone"] * 4,
              f"{MODID}:black_matter_stone", count=4, category="building")
    shapeless(os.path.join(rec, "red_matter_stone.json"), [RM] + ["minecraft:cobblestone"] * 4,
              f"{MODID}:red_matter_stone", count=4, category="building")


def gen_dimensions():
    for d in DIMENSIONS:
        write_json(os.path.join(DATA, "dimension_type", f"{d['id']}.json"), {
            "ultrawarm": False, "natural": False, "piglin_safe": False,
            "respawn_anchor_works": False, "bed_works": False, "has_raids": False,
            "has_skylight": True, "has_ceiling": False, "coordinate_scale": 1.0,
            "ambient_light": d["ambient"], "fixed_time": d["fixed_time"],
            "logical_height": 128, "min_y": 0, "height": 128,
            "effects": d["effects"], "infiniburn": "#minecraft:infiniburn_overworld",
            "monster_spawn_light_level": 0, "monster_spawn_block_light_limit": 0,
        })
        write_json(os.path.join(DATA, "dimension", f"{d['id']}.json"), {
            "type": f"{MODID}:{d['id']}",
            "generator": {
                "type": "minecraft:flat",
                "settings": {
                    "biome": d["biome"], "features": False, "lakes": False,
                    "layers": [{"block": b, "height": h} for b, h in d["layers"]],
                    "structure_overrides": [],
                },
            },
        })


def gen_tags():
    blocks = [f"{MODID}:black_matter_stone", f"{MODID}:red_matter_stone", f"{MODID}:pocket_portal"]
    for tag in ("mineable/pickaxe", "needs_iron_tool"):
        write_json(os.path.join(MC_DATA, "tags", "blocks", *tag.split("/")) + ".json",
                   {"replace": False, "values": blocks})


def gen_lang():
    en = {f"itemGroup.{MODID}": "Pocket Matter",
          f"block.{MODID}.pocket_portal": "Pocket Portal",
          f"block.{MODID}.black_matter_stone": "Black Matter Stone",
          f"block.{MODID}.red_matter_stone": "Red Matter Stone",
          f"tooltip.{MODID}.key": "Use on a Pocket Portal to enter: %s",
          f"message.{MODID}.need_key": "You need a Pocket Key to use this portal.",
          f"message.{MODID}.dimension_missing": "Dimension '%s' was not found (check the datapack)."}
    pt = {f"itemGroup.{MODID}": "Pocket Matter",
          f"block.{MODID}.pocket_portal": "Portal de Bolso",
          f"block.{MODID}.black_matter_stone": "Pedra de Matéria Negra",
          f"block.{MODID}.red_matter_stone": "Pedra de Matéria Vermelha",
          f"tooltip.{MODID}.key": "Use em um Portal de Bolso para entrar em: %s",
          f"message.{MODID}.need_key": "Você precisa de uma Chave de Bolso para usar este portal.",
          f"message.{MODID}.dimension_missing": "A dimensão '%s' não foi encontrada (verifique o datapack)."}
    for s in ARMOR_SETS:
        en[f"item.{MODID}.{s['id']}_core"] = f"{s['en']} Core"
        pt[f"item.{MODID}.{s['id']}_core"] = f"Núcleo de {s['pt']}"
        for piece, pen, ppt in PIECES:
            en[f"item.{MODID}.{s['id']}_{piece}"] = f"{s['en']} {pen}"
            pt[f"item.{MODID}.{s['id']}_{piece}"] = f"{ppt} de {s['pt']}"
    for d in DIMENSIONS:
        en[f"item.{MODID}.{d['id']}_key"] = f"{d['en']} Key"
        pt[f"item.{MODID}.{d['id']}_key"] = f"Chave: {d['pt']}"
        en[f"dimension.{MODID}.{d['id']}"] = d["en"]
        pt[f"dimension.{MODID}.{d['id']}"] = d["pt"]
    write_json(os.path.join(ASSETS, "lang", "en_us.json"), en)
    write_json(os.path.join(ASSETS, "lang", "pt_br.json"), pt)


if __name__ == "__main__":
    gen_textures()
    gen_models()
    gen_recipes()
    gen_dimensions()
    gen_tags()
    gen_lang()
    print("OK: conteudo gerado em", os.path.abspath(ROOT))
