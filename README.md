# Pocket Matter (addon do ProjectE) — Forge 1.20.1

Dimensoes de bolso + conjuntos de armadura de materia. Depende do ProjectE 1.20.1 (PE 1.0.1).

## Como rodar
1. Instale o **JDK 17** e o **IntelliJ IDEA**.
2. Baixe o **Forge MDK 1.20.1-47.3.0** (files.minecraftforge.net) e copie dele para esta pasta:
   `gradlew`, `gradlew.bat` e a pasta `gradle/`. (Nao incluí o wrapper pq e um binario.)
3. Abra esta pasta no IntelliJ (File > Open > build.gradle) e espere o Gradle sincronizar.
4. Rode `./gradlew genIntellijRuns` e depois a run config **runClient**.
5. Para gerar o jar: `./gradlew build` -> `build/libs/pocketmatter-0.1.0.jar`
   (coloque na pasta mods junto com o ProjectE).

## O que tem
- **Pocket Portal** (bloco): fora dos bolsos, clique com uma Chave na mao para entrar.
  Dentro, clique nele para voltar (ele ja aparece 2 blocos ao lado de onde voce chega).
- **3 dimensoes**: Black Matter Pocket, Red Matter Pocket, Twin Matter Pocket (uma Chave para cada).
- **5 conjuntos de armadura** (Void, Ember, Frost, Gaia, Aether), cada um com Nucleo + 4 pecas
  e bonus de set completo (visao noturna, resistencia ao fogo, respirar na agua, regeneracao, queda lenta).
- Tudo aparece na aba criativa **Pocket Matter**.
- O EMC das armaduras/chaves e calculado sozinho pelo ProjectE a partir das receitas.

## Receitas (todas exigem Dark Matter / Red Matter do ProjectE)
- Portal: `DRD / RER / DRD` (D = Dark Matter, R = Red Matter, E = Eye of Ender)
- Chaves: 2x matter + Ender Pearl + Stick (a "Twin" usa 1 Dark + 1 Red)
- Nucleos: 4 ingredientes sem formato (veja `tools/generate_content.py`), rende 2
- Pecas: formato normal de armadura usando Nucleos

## Como adicionar mais coisas
Tudo que e JSON/textura sai de `tools/generate_content.py`  (`pip install pillow`):
- **Nova dimensao**: adicione um item em `DIMENSIONS` no script **e** o nome em
  `PocketDimensions.java`; rode `python3 tools/generate_content.py`.
- **Novo conjunto de armadura**: item em `ARMOR_SETS` **e** constante em `MatterArmorMaterial.java`; rode o script.

## Sem instalar nada (compilar pelo GitHub)
1. Crie uma conta em github.com e um repositorio novo (pode ser privado).
2. "Add file > Upload files" e arraste o CONTEUDO desta pasta (inclusive a pasta `.github` e a `libs`).
3. Aba **Actions** > "Build mod" > espere ficar verde (uns 3-5 min).
4. Clique na execucao > secao **Artifacts** > baixe `pocketmatter-jar` (vem num zip com o .jar dentro).
5. Coloque o .jar e o jar do ProjectE na pasta `mods` do Forge 1.20.1.
