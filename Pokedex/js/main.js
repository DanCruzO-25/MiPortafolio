const listaPokemon = document.querySelector("#listaPokemon");
const botonesHeader = document.querySelectorAll(".btn-header");
const modal = document.getElementById("modal");

let URL = "https://pokeapi.co/api/v2/pokemon/";
let pokemonCache = [];

/* ================= CARGAR 151 ================= */

async function cargarPokemon() {
    for (let i = 1; i <= 151; i++) {
        const response = await fetch(URL + i);
        const data = await response.json();
        pokemonCache.push(data);
    }
    mostrarLista(pokemonCache);
}

/* ================= MOSTRAR LISTA ================= */

function mostrarLista(lista) {
    listaPokemon.innerHTML = "";
    lista.forEach(poke => mostrarPokemon(poke));
}

function mostrarPokemon(poke) {
    const tipoPrincipal = poke.types[0].type.name; // fire, water, grass…

    // Stats: HP, ATK, SPD (primeros 3 para la card)
    const hp  = poke.stats[0].base_stat;
    const atk = poke.stats[1].base_stat;
    const spd = poke.stats[5].base_stat;

    // Convertir stat a porcentaje (máximo ~255)
    const pct = val => Math.min(Math.round(val / 255 * 100), 100);

    const div = document.createElement("div");
    div.classList.add("pokemon", tipoPrincipal);
    div.dataset.num = `#${String(poke.id).padStart(3, "0")}`;

    div.innerHTML = `
        <img src="${poke.sprites.front_default}" alt="${poke.name}">
        <h3>${poke.name}</h3>
        <span class="type-tag">${tipoPrincipal}</span>
        <div class="stat-bar-wrap">
            <div class="stat-row">
                <span class="stat-name">HP</span>
                <div class="stat-track">
                    <div class="stat-fill" style="width:${pct(hp)}%"></div>
                </div>
            </div>
            <div class="stat-row">
                <span class="stat-name">ATK</span>
                <div class="stat-track">
                    <div class="stat-fill" style="width:${pct(atk)}%"></div>
                </div>
            </div>
            <div class="stat-row">
                <span class="stat-name">SPD</span>
                <div class="stat-track">
                    <div class="stat-fill" style="width:${pct(spd)}%"></div>
                </div>
            </div>
        </div>
    `;

    div.addEventListener("click", () => abrirModalInfo(poke));
    listaPokemon.append(div);
}

/* ================= FILTROS ================= */

botonesHeader.forEach(boton =>
    boton.addEventListener("click", e => {
        // Quitar activo de todos, poner en el clickeado
        botonesHeader.forEach(b => b.classList.remove("activo"));
        e.target.classList.add("activo");

        const id = e.target.id;

        if (id === "ver-todos") {
            mostrarLista(pokemonCache);
        } else {
            const filtrados = pokemonCache.filter(p =>
                p.types.some(t => t.type.name === id)
            );
            mostrarLista(filtrados);
        }
    })
);

/* ================= ABRIR MODAL ================= */

async function abrirModalInfo(poke) {
    const tipoPrincipal = poke.types[0].type.name;

    // Colores de borde por tipo — para darle color al modal igual que la card
    const tipoBordes = {
        fire: "#ff3300", water: "#3399ff", grass: "#66cc33",
        electric: "#ffcc33", ice: "#66cccc", fighting: "#cc3333",
        poison: "#9933cc", ground: "#ccaa66", flying: "#9999ff",
        psychic: "#ff66aa", bug: "#99cc33", rock: "#ccaa33",
        ghost: "#6666cc", dragon: "#9966ff", dark: "#996644",
        steel: "#aaaacc", fairy: "#ff99cc", normal: "#c6c6a7"
    };

    // Poner borde del tipo en el modal
    document.querySelector(".pokedex-modal").style.borderColor =
        tipoBordes[tipoPrincipal] || "#555";

    // Mostrar modal
    modal.style.display = "flex";

    // Rellenar campos fijos del HTML
    document.getElementById("pokemonNombre").textContent =
        `#${String(poke.id).padStart(3, "0")} ${poke.name.toUpperCase()}`;

    document.getElementById("pokemonImagen").src =
        poke.sprites.other["official-artwork"].front_default || poke.sprites.front_default;

    document.getElementById("pokemonDescripcion").textContent =
        `Tipo: ${poke.types.map(t => t.type.name).join(" / ")}  •  ` +
        `Altura: ${poke.height / 10}m  •  Peso: ${poke.weight / 10}kg`;

    // Stats — lista completa con barra + número
    const statsEl = document.getElementById("pokemonStats");
    statsEl.innerHTML = poke.stats.map(stat => {
        const pct = Math.min(Math.round(stat.base_stat / 255 * 100), 100);
        return `
            <li>
                <span class="stat-label">${stat.stat.name}</span>
                <div class="stat-track">
                    <div class="stat-fill" style="width:${pct}%"></div>
                </div>
                <span class="stat-val">${stat.base_stat}</span>
            </li>
        `;
    }).join("");

    // Descripción en inglés (async)
    try {
        const speciesRes = await fetch(poke.species.url);
        const speciesData = await speciesRes.json();
        const entrada = speciesData.flavor_text_entries.find(
            e => e.language.name === "en"
        );
        if (entrada) {
            document.getElementById("pokemonDescripcion").textContent =
                entrada.flavor_text.replace(/\f/g, " ");
        }
    } catch (e) {
        // Si falla la descripción, dejamos la info básica ya puesta
    }
}

/* ================= CERRAR MODAL ================= */

document.getElementById("cerrarModal").addEventListener("click", () => {
    modal.style.display = "none";
});

modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
});

/* ================= INIT ================= */
cargarPokemon();
