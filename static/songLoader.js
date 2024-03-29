// Script for loading songs based on bracket size selected in create-tourney html template
function updateSongs() {
    const bracketSize = parseInt(document.getElementById('bracket_size').value);
    const songsContainer = document.getElementById('songsContainer') || createSongsContainer();
    let existingSongs = [];

    // Before clearing songs, save current songs entered
    const currentSongInputs = songsContainer.getElementsByClassName('song');
    for (let i = 0; i < currentSongInputs.length; i++) {
            let title = currentSongInputs[i].querySelector(`input[name="songs[${i}][title]"]`).value;
            let artist = currentSongInputs[i].querySelector(`input[name="songs[${i}][artist]"]`).value;
            existingSongs.push({ title, artist });
        }

    // Clear existing song inputs
    songsContainer.innerHTML = '';

    for (let i = 0; i < bracketSize; i++) {
        const songDiv = document.createElement('div');
        songDiv.className = 'song row mb-3';

        // Create a label for each song group
        const songLabel = document.createElement('h5');
        songLabel.innerText = `Song ${i + 1}`;
        songDiv.appendChild(songLabel);

        // Creating each input field within a 'col' class for alignment
        const titleInput = createSongInput(`songs[${i}][title]`, 'Title', 'col-3', existingSongs[i]?.title);
        const artistInput = createSongInput(`songs[${i}][artist]`, 'Artist', 'col-3', existingSongs[i]?.artist);

        songDiv.appendChild(titleInput);
        songDiv.appendChild(artistInput);

        songsContainer.appendChild(songDiv);
    }
}

function createSongsContainer() {
    const container = document.createElement('div');
    container.id = 'songsContainer';
    document.getElementById('tourneySetup').appendChild(container);
    return container;
}

function createSongInput(name, placeholder, className, value = '') {
    const inputGroup = document.createElement('div');
    inputGroup.className = `${className} input-group mb-3`;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'form-control';
    input.name = name;
    input.placeholder = placeholder;
    input.value = value;

    inputGroup.appendChild(input);
    return inputGroup;
}

document.getElementById('bracket_size').addEventListener('change', updateSongs);
document.addEventListener('DOMContentLoaded', updateSongs);
