// static/script.js
// const blocker = document.getElementById('click-blocker');
function recordChoice(choice) {
    const hiddenInput = document.getElementById('choice_input');
    if (hiddenInput) {
        hiddenInput.value = choice;
        console.log("Recording choice:", choice);
    } else {
        console.error("Fatal: Could not find hidden input #choice_input");
    }
}

function revealCoin(coinObject) {
    console.log("Revealing coin:", coinObject);
    coinObject.classList.add('prize_reveal_animation');
    if (coinObject.id.includes('left')) {
        choice = 'left';
    } else if (coinObject.id.includes('right')) {
        choice = 'right';
    }

    // Record choice
    recordChoice(choice);

    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit("hi");
    }, 4000);
}

function placeCoinsInBag(prize_place_positions) {
    const staggerDelayMs = 100;
    const prize_elements = document.getElementsByClassName('prize');
    const coins = [];
    for (var prize of prize_elements) {
        if (prize.id.includes('filled_bag_coin_')) {
            coins.push(prize);
        }
    }


    for (let i = 0; i < coins.length; i++) {
        setTimeout(() => {
            coins[i].classList.remove(prize_place_positions[0]);
            coins[i].classList.add(prize_place_positions[1]);
            console.log("Moving coin:", coins[i]);
        }, i * staggerDelayMs);
    }
}


function openChest(object) {
    // blocker.classList.remove('hidden');
    const children = object.children;

    let choice = "unknown";
    let prize_bag_container = null;
    let chest_top = null;

    for (var child of children) {
        console.log("Child found:", child);
        if (child.id.includes('chest_top_image')) {
            chest_top = child;
        } else if (child.classList.contains('bag_container')) {
            prize_bag_container = child;
        }
    }
    console.log('Prize_bag', prize_bag_container);

    // Find choice based on which chest was clicked

    if (object.id.includes('left')) {
        choice = 'left';
    } else if (object.id.includes('right')) {
        choice = 'right';
    }

    // Record choice
    recordChoice(choice);

    chest_top.classList.add('open_chest_rumble_animation');

    // Reveal Prize if there is one
    if (prize_bag_container != null) {
        console.log("Prize has been found !")
        setTimeout(() => {
            revealCoinsAndBag(prize_bag_container);
        }, 2000); // reveal prize after chest opens
    } else {
        console.log("No prize for this chest")
    }

    var audio = new Audio("../audio/open_chest_rumble.mp3");
    console.log("Playing audio");
    audio.play();

    // window.setTimeout(function () {
    //     SUBMITTING = true;
    //     document.querySelector('form').submit("hi");
    // }, 5000);
    // blocker.classList.add('hidden');

}

function revealCoinsAndBag(bagContainerObj) {
    console.log("Revealing coin from bag:", bagContainerObj);
    const staggerDelayMs = 300;
    const bagContainerChildren = bagContainerObj.children
    let prizeBag = null;
    let prizeCoins = [];

    for (var child of bagContainerChildren) {
        if (child.classList.contains('prize_bag')) {
            prizeBag = child;
        } else {
            prizeCoins.push(child);
        }
    }


    console.log("Found prize bag:", prizeBag);
    console.log("Found prize coins:", prizeCoins);



    // TODO: Change this later to match the correct reveal animations

    // 1. Bring bag up

    delta_y = `calc(${prizeBag.style.height} * 2/3)`;
    console.log("Delta Y for bag rise:", delta_y);

    for (var child of bagContainerChildren) {
        child.style.top = `calc(${child.style.top} - ${delta_y})`;
    }

    // 2. Open bag 
    setTimeout(() => {
        prizeBag.src = "/images/open_bag.png";

        setTimeout(() => {
            // 3. Reveal coins one by one, starting with the highest coin (last in list)
            for (let i = prizeCoins.length - 1; i >= 0; i--) {
                setTimeout(() => {
                    prizeCoins[i].classList.add('prize_reveal_animation');
                }, (prizeCoins.length - 1 - i) * staggerDelayMs);
            }
        }, 500);
    }, 1200);


}


function selectChest(object) {
    console.log("Selecting object:", object);
    var audio = new Audio("../audio/pop.mp3");
    audio.play();

    children = object.children;

    for (var child of children) {
        console.log("Child found:", child);
        if (child.id.includes('chest')) {
            chest_top = child;
            chest_top.classList.add('pulse_animation');
        }
    }

    // Find choice based on which chest was clicked

    if (object.id.includes('left')) {
        choice = 'left';
    } else if (object.id.includes('right')) {
        choice = 'right';
    }

    // Record choice
    recordChoice(choice);

    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit();
    }, 2000);
}

function stage_1_animation() {
    /* Getting coin element */
    var prizes = document.getElementsByClassName('prize');
    console.log("Found prize elements:", prizes);
    if (prizes.length === 0) {
        console.log("No prize element found for animation.");
        return;
    }

    const bag_container = document.getElementsByClassName('bag_container');
    if (bag_container.length === 0) {
        console.error("No bag element found for animation.");
        return;
    }
    // const bag = bag_container[0].children[0];
    // var bag = prizes[0];
    let bag = null;
    for (var prize of prizes) {
        if (prize.classList.contains('prize_bag')) {
            bag = prize;
        }
    }

    const chest_top = document.getElementsByClassName('chest_top_image');
    console.log("Found chest tops for animation:", chest_top);

    let prize_side = "left";
    if (bag_container[0].id.includes('right')) {
        prize_side = "right";
    }

    let prize_place_positions = [];

    if (prize_side == "left") {
        prize_place_positions = ['prize-place-left-reset', 'prize-place-left-1', 'prize-place-left-2'];
    }
    else if (prize_side == "right") {
        prize_place_positions = ['prize-place-right-reset', 'prize-place-right-1', 'prize-place-right-2'];
    }


    /* Getting occluder elements */

    const occluders = document.getElementsByClassName('occluder');
    if (occluders.length === 0) {
        console.error("No occluder elements found.");

    } else {
        console.log("Found occluders:", occluders);
    }


    /* Resetting elements to correct positions */
    for (var prize of prizes) {
        prize.classList.add(prize_place_positions[0]);
    }

    for (var occluder of occluders) {
        occluder.classList.add('occluder-place-reset');
    }

    // Stage 0: Initial Delay (The 'oncreation' equivalent)

    const initialDelay = 500; // Wait 0.5 seconds before starting
    for (var occluder of occluders) {
        occluder.classList.remove('hidden');
    }
    for (var prize of prizes) {
        prize.classList.remove('hidden');
    }

    // Introduce coin in center top
    setTimeout(() => {
        bag.classList.remove(prize_place_positions[0]);
        bag.classList.add(prize_place_positions[1]);


        // Coin drop in the bag, bag closes
        setTimeout(() => {
            placeCoinsInBag(prize_place_positions);


            // Close bag
            setTimeout(() => {
                bag.src = "/images/closed_bag.png";

                // Move chest tops up to show it is empty
                setTimeout(() => {

                    for (var top of chest_top) {
                        top.classList.add('open_chest_simple_animation');
                    }

                    // Introduce occluders, doesn't cover the chest yet
                    setTimeout(() => {
                        for (var occluder of occluders) {
                            occluder.classList.remove('occluder-place-reset');
                            occluder.classList.add('occluder-place-1');
                        }

                        var occluder_timeout = (occluders.length > 0) ? 1200 : 0;

                        // Pull occluders down in front of chest. Removing occluder-place-1 will return occluders to their original position
                        setTimeout(() => {
                            for (var occluder of occluders) {
                                occluder.classList.remove('occluder-place-1');
                            }

                            // Move the coin from center top to center mid
                            setTimeout(() => {
                                for (var prize of prizes) {
                                    prize.classList.remove(prize_place_positions[1]);
                                    prize.classList.add(prize_place_positions[2]);

                                }

                                // Move from center mid to left or right
                                setTimeout(() => {
                                    /* Removing coin-place-2 will return coin to its original (aka final) position */
                                    for (var prize of prizes) {
                                        prize.classList.remove(prize_place_positions[2]);
                                    }
                                    // new Audio("../audio/coin_placement.wav").play();


                                    // // /* PPlay the relevant audio */
                                    // var audio = new Audio("../audio/open_chest.mp3");
                                    // const currentDir = __dirname;
                                    // console.log(currentDir);
                                    // console.log(audio);
                                    // audio.play();


                                    // And hide the coin after reaching final position
                                    // setTimeout(() => {
                                    //     coin.classList.add('hidden');
                                    // }, 1200);

                                    setTimeout(() => {
                                        for (var top of chest_top) {
                                            top.classList.remove('open_chest_simple_animation');
                                            top.classList.add('close_chest_simple_animation');
                                        }
                                        // Pull occluders up out of screen
                                        setTimeout(() => {
                                            for (var occluder of occluders) {
                                                occluder.classList.add('occluder-place-reset');
                                                occluder.style.transition = "all 2s ease-in-out";
                                            }


                                            // Submit to kesar
                                            window.setTimeout(function () {
                                                SUBMITTING = true; // Kesar global variable
                                                document.querySelector('form').submit();
                                            }, 2000);
                                        }, occluder_timeout);
                                    }, 500);

                                }, 1200);

                            }, 1200);
                        }, occluder_timeout);
                    }, 1200);
                }, 500);
            }, 2000);

        }, 1200);
    }, initialDelay);
}

function stage_2_animation() {
    /* Getting coin element */


    const hooks = document.getElementsByClassName('hook');
    for (var object of hooks) {
        console.log(object.id)
        if (object.id.includes('prize')) {
            hook_pos1_x = object.style.left;
            hook_pos1_y = object.style.top;
            var position = object.id.split('_')[2];
            var hook = object
        } else if (object.id.includes('chest')) {
            hook_pos2_x = object.style.left;
            hook_pos2_y = object.style.top;
        }
    }

    const all_prize_elements = document.getElementsByClassName('prize');
    const prize_elements = [];
    const original_prize_positions = [];
    for (var object of all_prize_elements) {
        if (object.id.includes(position)) {
            prize_elements.push(object);
            original_prize_positions.push(({ left: object.style.left, top: object.style.top }));
        }
    }

    var chest = document.getElementById(`chest_container_${position}`);
    let reset_deltax = "";
    let reset_deltay = "";
    if (position == "right") {
        reset_deltax = "40vw";
        reset_deltay = "-20vh";
    } else if (position == "left") {
        reset_deltax = "-40vw";
        reset_deltay = "-20vh";
    }



    hook_posreset_x = `calc(${hook_pos1_x} + ${reset_deltax})`;
    hook_posreset_y = `calc(${hook_pos1_y} + ${reset_deltay})`;

    // Resetting positions
    // new_prize.style.left = `calc(${prize_position_x} + ${reset_deltax})`;
    // new_prize.style.top = `calc(${prize_position_y} + ${reset_deltay})`;
    for (let i = 0; i < prize_elements.length; i++) {
        prize_elements[i].style.left = `calc(${original_prize_positions[i].left} + ${reset_deltax})`;
        prize_elements[i].style.top = `calc(${original_prize_positions[i].top} + ${reset_deltay})`;
    }

    hook.style.left = hook_posreset_x;
    hook.style.top = hook_posreset_y;

    hook.classList.remove('hidden');
    for (var obj of prize_elements) {
        obj.classList.remove('hidden');
    }

    setTimeout(() => {
        // Move prize in front of chest
        for (let i = 0; i < prize_elements.length; i++) {
            prize_elements[i].style.left = original_prize_positions[i].left;
            prize_elements[i].style.top = original_prize_positions[i].top;
        }
        // new_prize.style.left = prize_position_x;
        // new_prize.style.top = prize_position_y;

        hook.style.left = hook_pos1_x;
        hook.style.top = hook_pos1_y;

        setTimeout(() => {
            hook.style.left = hook_pos2_x;
            hook.style.top = hook_pos2_y;

            setTimeout(() => {
                hook.style.left = hook_posreset_x;
                hook.style.top = hook_posreset_y;


                for (var child of chest.children) {


                    console.log("Child found:", child);
                    child.style.left = `calc(${hook_posreset_x} - ${hook_pos2_x} + ${child.style.left})`;
                    child.style.top = `calc(${hook_posreset_y} - ${hook_pos2_y} + ${child.style.top})`;
                }
                // Submit to kesar
                window.setTimeout(function () {
                    SUBMITTING = true; // Kesar global variable
                    document.querySelector('form').submit();
                }, 2000);
            }, 1200);
        }, 1200);

    }, 1200);
}



document.addEventListener('DOMContentLoaded', () => {
    // stage_1_animation();
    stage = document.getElementById('stage_indicator').innerText;
    console.log("Current stage:", stage);

    if (stage == '1') {
        stage_1_animation();
    } else if (stage == '2') {
        stage_2_animation();
    }

    // have a tag for each of the stages
    // console.log("Document loaded, starting spiral animation");
    // startSpiralAnimation();
});


// function startSpiralAnimation() {
//     // console.log("Initializing GSAP spiral animation");
//     gsap.registerPlugin(MotionPathPlugin);
//     console.log("Starting spiral animation");

//     gsap.to("#dot", {
//         // Standard tween properties
//         duration: 15,          // The time it takes to complete one loop
//         repeat: -1,            // Loop infinitely
//         ease: "none",          // Linear speed for a smooth spiral motion

//         // MotionPathPlugin Configuration
//         motionPath: {
//             path: "#spiralPath", // Reference the ID of the SVG path
//             align: "#spiralPath",// Align the object's center to the path 
//             alignOrigin: [0.5, 0.5], // Center the object precisely on the path
//             autoRotate: true     // Automatically rotate the dot to face the direction of the path
//         }
//     });
// }