// static/script.js
// const chest_listener = document.getElementById('full_chest_container');
// chest_listener.addEventListener('click', openChest);

// Function to start the animation and automatically submit the form
function startRotation() {
    const coin = document.getElementById('coin_image');

    // 1. ADD THE CSS CLASS to the element, which starts the animation
    coin.classList.add('pop_rotate');

    // 2. Disable the button to prevent double-clicks
    document.querySelector('button').disabled = false; //change to true later

    // 3. Auto-submit the Kesar form after the animation is complete (2.5 seconds)
    // window.setTimeout(function () {
    //     SUBMITTING = false; // Kesar global variable
    //     document.querySelector('form').submit();
    // }, 2800); // Wait slightly longer than the 2.5s animation duration
    return
}

function openChest(chest_id, prizeId) {
    const chest_top = document.getElementById(chest_id);
    chest_top.classList.add('open_chest_animation');

    if (prizeId) {
        const prize = document.getElementById(prizeId);
        // print(prize)
        if (prize) {
            console.log("Prize has been found !")

            setTimeout(() => {
                prize.classList.add('prize_reveal_animation');
            }, 2000); // reveal prize after chest opens
        } else {
            console.log("Server error finding prize with ID:", prizeId)
        }
    }
    else {
        console.log("No prize for this chest")
    }

    // if (occluderId) {
    //     const occluder = document.getElementById(occluderId);
    //     if (occluder) {
    //         console.log("Occluder has been found !")

    //         setTimeout(() => {
    //             occluder.classList.add('swipe_up_animation');
    //         }, 2000);
    //     } else {
    //         console.log("Server error finding occluder with ID:", occluderId)
    //     }
    // }
    // else {
    //     console.log("No occluder for this chest")
    // }

    var audio = new Audio("../audio/open_chests.mp3");
    console.log("Playing audio");
    audio.play();
    window.setTimeout(function () {
        SUBMITTING = true; // Kesar global variable
        document.querySelector('form').submit();
    }, 5000); // Wait slightly longer than the 2.5s animation duration



    // window.setTimeout(function () {
    //     SUBMITTING = true; // Kesar global variable
    //     document.querySelector('form').submit();
    // }, 5000); // Wait slightly longer than the 2.5s animation duration
    // Example: Make the prize spin after the chest lid moves
    // You would typically apply an animation class here
    //     setTimeout(() => {
    //         prize.classList.add('prize_reveal_animation');
    //     }, 500); // Wait 500ms after opening the chest
    // } else {
    //     console.error(`Prize element with ID '${prizeId}' not found.`);
}

function swipeRight(object) {
    // console.log("Swiping right for object:", object_id);
    // const object = document.getElementById(object_id);
    // e.preventDefault(); // Prevent default touch behavior
    children = object.children;

    for (let i = 0; i < children.length; i++) {
        console.log("Child found:", children[i]);
        children[i].classList.add('swipe_right_animation');
    }
    // console.log("Object found:", object);
    // object.classList.add('swipe_right_animation'); // slight delay before starting animation

    // console.log("Swipe right animation added to object:", object);
}
// const prize = document.getElementById('prize')



function select(object) {
    console.log("Selecting object:", object);
    // document.documentElement.style.setProperty('--animation-speed', '5s');
    root = document.documentElement;
    root.style.setProperty('--animation-speed', '1s');
    object.classList.add('pulse_animation');
    var audio = new Audio("../audio/pop.mp3");
    audio.play();

}

function addCoinPlacement(coinObject) {
    coinObject.classList.add('coin_placement_animation');
}


function stage_1_animation() {
    /* Getting coin element */
    var coin = document.getElementsByClassName('coin_stage_1');
    console.log("Found coin element:", coin);
    if (coin.length === 0) {
        console.error("No coin element found for animation.");
        return;
    }
    coin = coin[0];


    /* Getting occluder elements */

    occluders = document.getElementsByClassName('occluder');
    if (occluders.length === 0) {
        console.error("No occluder elements found.");

    } else {
        console.log("Found occluders:", occluders);
    }


    /* Resetting elements to correct positions */
    coin.classList.add('coin-place-reset');

    for (var occluder of occluders) {
        occluder.classList.add('occluder-place-reset');
    }


    // Stage 0: Initial Delay (The 'oncreation' equivalent)

    const initialDelay = 500; // Wait 0.5 seconds before starting

    // Introduce coin in center top
    setTimeout(() => {
        coin.classList.remove('coin-place-reset');
        coin.classList.add('coin-place-1');

        // TODO: Move chest tops up as well

        // Introduce occluders, doesn't cover the chest yet
        setTimeout(() => {
            for (var occluder of occluders) {
                occluder.classList.remove('occluder-place-reset');
                occluder.classList.add('occluder-place-1');
            }

            // Pull occluders down in front of chest. Removing occluder-place-1 will return occluders to their original position
            setTimeout(() => {
                for (var occluder of occluders) {
                    occluder.classList.remove('occluder-place-1');
                }

                // Move the coin from center top to center mid
                setTimeout(() => {
                    coin.classList.remove('coin-place-1');
                    coin.classList.add('coin-place-2');

                    // Move from center mid to left or right
                    setTimeout(() => {
                        /* Removing coin-place-2 will return coin to its original (aka final) position */

                        coin.classList.remove('coin-place-2');


                        // /* PPlay the relevant audio */
                        // const audio = new Audio("../audio/open_chest.mp3");
                        // const currentDir = __dirname;
                        // console.log(currentDir);
                        // console.log(audio);
                        // audio.play();


                        // And hide the coin after reaching final position
                        setTimeout(() => {
                            coin.classList.add('hidden');
                        }, 1200);


                        // Pull occluders up out of screen
                        setTimeout(() => {
                            for (var occluder of occluders) {
                                occluder.classList.add('occluder-place-reset');
                                occluder.style.transition = "all 2s ease-in-out";
                            }
                        }, 2000);


                    }, 1200);

                }, 1200);
            }, 1200);
        }, 1200);
    }, initialDelay);

    // window.setTimeout(function () {
    //     SUBMITTING = true; // Kesar global variable
    //     document.querySelector('form').submit();
    // }, 5000); // Wait slightly longer than the 2.5s animation duration
}

document.addEventListener('DOMContentLoaded', () => {
    // Run the animation once the DOM structure is ready
    stage_1_animation();
});
