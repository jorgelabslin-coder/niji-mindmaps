#!/bin/bash
# Descarga imágenes de fondo con estética anime/JP para Niji Mindmaps
# Usa Unsplash como fuente de imágenes de dominio público

ANIME_DIR="data/anime"
mkdir -p "$ANIME_DIR"

echo "Descargando fondos anime-style..."

# Paisajes / naturaleza (estilo anime)
URLS=(
  "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=1920"  # bosque japonés
  "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1920"  # naturaleza
  "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920"  # montaña
  "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=1920"  # bosque
  "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920"  # campo
  "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920"  # playa
  "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920"  # lago
  "https://images.unsplash.com/photo-1518173946687-a36f968f7e1f?w=1920"  # atardecer
  "https://images.unsplash.com/photo-1518495973-8c133f7c3b4f?w=1920"  # montaña
  "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920"  # paisaje
  "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920"  # estrellas
  "https://images.unsplash.com/photo-1465056504211-c5430f3cccec?w=1920"  # amanecer
  "https://images.unsplash.com/photo-1504198453319-5ce911bafcde?w=1920"  # atardecer ciudad
  "https://images.unsplash.com/photo-1504567961542-e24d9439a724?w=1920"  # camino
  "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920"  # bosque
  "https://images.unsplash.com/photo-1503756234508-e32369269deb?w=1920"  # playa atardecer
  "https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?w=1920"  # lago
  "https://images.unsplash.com/photo-1420593248178-d88870618ca0?w=1920"  # secuoyas
  "https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920"  # cascada
  "https://images.unsplash.com/photo-1504392022767-a8fc0771f239?w=1920"  # niebla
  "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1920"  # ciudad
  "https://images.unsplash.com/photo-1559827291-baf8a54ef685?w=1920"  # linternas
  "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=1920"  # templo
  "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=1920"  # cerezos
  "https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?w=1920"  # bambú
  "https://images.unsplash.com/photo-1504198453319-5ce911bafcde?w=1920"  # atardecer
  "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=1920"  # ciudad moderna
  "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920"  # noche ciudad
  "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1920"  # ciudad amanecer
  "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920"  # dubai
)

for i in "${!URLS[@]}"; do
  idx=$((i + 1))
  num=$(printf "%02d" $idx)
  file="$ANIME_DIR/bg-$num.jpg"
  if [ ! -f "$file" ]; then
    echo "  Descargando bg-$num.jpg..."
    curl -sL "${URLS[$i]}" -o "$file" || echo "  [skip] bg-$num.jpg"
    sleep 0.5
  else
    echo "  bg-$num.jpg ya existe"
  fi
done

echo ""
echo "✓ Descarga completada: $(ls $ANIME_DIR/*.jpg 2>/dev/null | wc -l) imágenes en $ANIME_DIR"
