const listaPokemon = document.querySelector("#listaPokemon");
const botonesHeader = document.querySelectorAll(".btn-header");
const modal = document.getElementById("modal");
const cerrarModal = document.getElementById("cerrarModal");

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
    const div = document.createElement("div");
    div.classList.add("pokemon");

    div.innerHTML = `
        <img src="${poke.sprites.front_default}" alt="${poke.name}">
        <h3>#${String(poke.id).padStart(3, "0")} ${poke.name.toUpperCase()}</h3>
    `;

    div.addEventListener("click", () => abrirModalInfo(poke));
    listaPokemon.append(div);
}

/* ================= FILTROS ================= */

botonesHeader.forEach(boton =>
    boton.addEventListener("click", e => {
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

    modal.style.display = "flex";

    const speciesResponse = await fetch(poke.species.url);
    const speciesData = await speciesResponse.json();

    const entrada = speciesData.flavor_text_entries.find(
        entry => entry.language.name === "en"
    );

    const descripcion = entrada
        ? entrada.flavor_text.replace(/\f/g, " ")
        : "No description available.";

    // 👇 Ahora llenamos directamente el modal
    document.querySelector(".pokedex-modal").innerHTML = `
        <button id="cerrarModal">X</button>

        <img class="pokemon-img"
            src="${poke.sprites.other['official-artwork'].front_default}"
            alt="${poke.name}">

        <h2>#${String(poke.id).padStart(3, "0")} ${poke.name.toUpperCase()}</h2>

        <p><strong>Type:</strong> ${poke.types.map(t => t.type.name).join(", ")}</p>
        <p><strong>Height:</strong> ${poke.height}</p>
        <p><strong>Weight:</strong> ${poke.weight}</p>

        <h3>Stats</h3>
        <ul class="stats">
            ${poke.stats.map(stat => `
                <li>${stat.stat.name.toUpperCase()}: ${stat.base_stat}</li>
            `).join("")}
        </ul>

        <h3>Description</h3>
        <p>${descripcion}</p>
    `;

    // 👇 Volvemos a activar el botón cerrar
    document.getElementById("cerrarModal").addEventListener("click", () => {
        modal.style.display = "none";
    });
}

/* ================= CERRAR MODAL AL HACER CLICK FUERA ================= */

modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});


cargarPokemon();
