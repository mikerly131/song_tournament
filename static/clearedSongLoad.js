function updateSongs() {
    const bracketSize = document.getElementById('bracketSize').value;
    const songsContainer = document.getElementById('songsContainer') || createSongsContainer();
    songsContainer.innerHTML = ''; // Clear existing song inputs

    for (let i = 0; i < bracketSize; i++) {
        const songDiv = document.createElement('div');
        songDiv.className = 'song row mb-3'; // Use 'row' for Bootstrap row formatting

        // Create a label for each song group
        const songLabel = document.createElement('h5');
        songLabel.innerText = `Song ${i + 1}`;
        songDiv.appendChild(songLabel);

        // Creating each input field within a 'col' class for alignment
        const titleInput = createSongInput(`songs[${i}][title]`, 'Title', 'col');
        const artistInput = createSongInput(`songs[${i}][artist]`, 'Artist', 'col');
        const clipUrlInput = createSongInput(`songs[${i}][clip_url]`, 'Clip URL', 'col');

        songDiv.appendChild(titleInput);
        songDiv.appendChild(artistInput);
        songDiv.appendChild(clipUrlInput);

        songsContainer.appendChild(songDiv);
    }
}

function createSongsContainer() {
    const container = document.createElement('div');
    container.id = 'songsContainer';
    document.getElementById('tourneySetup').appendChild(container);
    return container;
}

function createSongInput(name, placeholder, className) {
    const inputGroup = document.createElement('div');
    inputGroup.className = `${className} input-group mb-3`;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control';
    input.name = name;
    input.placeholder = placeholder;

    inputGroup.appendChild(input);
    return inputGroup;
}

document.getElementById('bracketSize').addEventListener('change', updateSongs);
document.addEventListener('DOMContentLoaded', updateSongs);
