function toggledivExperiencia(div, button) {

    if (div.style.display !== 'flex') {
        div.style.display = 'flex';
        button.textContent = "Fechar"
    } else {
        div.style.display = 'none';
        button.textContent = "Nova Experiência"
    }
}


