


const SERVER_API_URL = 'http://localhost:5002';

// Get all celebrity cards
const celebrityCards = document.querySelectorAll('.celebrity-card');

// Apply random float animations to each card
celebrityCards.forEach(card => {
    const randomDuration = Math.floor(Math.random() * 8) + 2; // Random duration between 2s and 7s
    const randomDelay = Math.random() * 1.5; // Random delay between 0s and 2s
    const randomAmplitude = Math.floor(Math.random() * 20) + 5; // Random amplitude between 5px and 15px

    card.style.animation = `floatAnimation ${randomDuration}s infinite alternate ease-in-out`;
    card.style.animationDelay = `-${randomDelay}s`;
    card.style.transform = `translateY(${randomAmplitude}px)`;
});

// variables to store selected data 
var hostName;
var guestName;
var episodeTopic;
var episodeDuration;


function selectCard(selectedCard, type){

    clearSelections(type)

    // Highlight the selected container
    selectedCard.classList.add('selected-card');

    // Retrieve the name from the selected container
    var name = selectedCard.querySelector('.name').innerText;
    var nameArr = name.split(" ");
    name = nameArr.join("_");
    name = name.toLowerCase();
    if (type == 'host'){
        hostName = name;
    }
    else {
        guestName = name;
    }
    console.log("Selected: ", name);

}

function clearSelections(type) {

    var allSelections;

    if (type == 'host') {
        allSelections = document.querySelectorAll('.host');
    }
    else {
        allSelections = document.querySelectorAll('.guest');
    }
    // Remove the 'selected-container' class from all containers
    allSelections.forEach(container => {
        container.classList.remove('selected-card');
    });
}

function getTopic() {
    // Retrieve the value from the input field
    episodeTopic = document.getElementById('episodeTopicInput').value;
    console.log("Episode Topic:", episodeTopic);
}

function getDuration() {
    // Retrieve the value from the input field
    episodeDuration = document.getElementById('episodeDurationInput').value;
    console.log("Episode Duration:", episodeDuration);
}

function sendPodcastData() {

    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'flex';

    console.log(hostName);
    console.log(guestName);

    const podcastData = {
        'host': hostName,
        'guest': guestName,
        'topic': episodeTopic,
        'duration': Number(episodeDuration)
    };

    // send data to backend using fetch 
    var api_url = SERVER_API_URL + '/cast';
    fetch(api_url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(podcastData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent to the backend:', data);
        // Add any additional logic here based on the backend response
        const videoUrl = data.video;
        // Set the video source dynamically
        const videoElement = document.getElementById('podcast-video');

        // Show the video element
        videoElement.style.display = 'block';

        // Hide the loading indicator
        const loadingIndicator = document.getElementById('loadingIndicator');
        loadingIndicator.style.display = 'none';

        videoElement.src = videoUrl;
    })
    .catch(error => {
        console.error('Error sending data to the backend:', error);
        // Handle errors if needed
        // Hide the loading indicator in case of an error
        loadingIndicator.style.display = 'none';
    });
    
}

document.getElementById('generateButton').addEventListener('click', function() {

    // Call functions to get selected data
    getTopic();
    getDuration();
    // Call the function to send data to the backend
    sendPodcastData();
});

document.addEventListener('mousemove', (e) => {
    const cursor = document.getElementById('cursor');
    cursor.style.left = e.pageX + 'px';
    cursor.style.top = e.pageY + 'px';
});

document.addEventListener('mouseenter', () => {
    const cursor = document.getElementById('cursor');
    cursor.style.width = '200px';
    cursor.style.height = '200px';
});

document.addEventListener('mouseleave', () => {
    const cursor = document.getElementById('cursor');
    cursor.style.width = '500px';
    cursor.style.height = '500px';
});