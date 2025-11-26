// static/script.js
// const blocker = document.getElementById('click-blocker');




// import { gsap } from "gsap";
// import { MotionPathPlugin } from "gsap/MotionPathPlugin";
const PLAY_AUDIO = true;
// function initializeGSAP() {
//     // Check if the global object exists before using it
//     if (typeof gsap !== 'undefined' && typeof MotionPathPlugin !== 'undefined') {
//         gsap.registerPlugin(MotionPathPlugin);
//         console.log("GSAP and MotionPathPlugin registered successfully.");
//         return true;
//     }
//     console.error("GSAP or MotionPathPlugin not yet defined.");
//     return false;
// }
function initializeGSAP() { return true; }

function startExperiment() {
    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit("hi");
    }, 300);
}

function recordChoice(choice) {
    const hiddenInput = document.getElementById('choice_input');
    if (hiddenInput) {
        hiddenInput.value = choice;
        console.log("Recording choice:", choice);
    } else {
        console.error("Fatal: Could not find hidden input #choice_input");
    }
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
            setTimeout(() => {
                new Audio("../audio/drop_coin.mp3").play();
            }, 750);
        }, i * staggerDelayMs);
    }
}


function removeObject(object) {
    console.log("Removing object and descendants:", object);

    // Create an array containing the root object AND all its descendants
    const allElements = [object, ...object.querySelectorAll('*')];
    const dy = "-100vh";

    // Loop through every element in that array
    allElements.forEach(element => {
        // element.classList.add('shift_out_up_animation');
        element.style.transition = "all 1s linear";
        // Get current top or default to 0px to prevent "calc( + -100vh)" errors
        requestAnimationFrame(() => {
            var currentTop = element.style.top;
            console.log('New transition style:', element.style.transition);
            element.style.top = `calc(${currentTop} + ${dy})`;
        });
    });
}

function openChest(object) {
    showOverlay();

    const children = object.children;

    let choice = "unknown";
    let prize_bag_container = null;
    let chest_top = null;

    for (var child of children) {
        if (child.id.includes('chest_top_image')) {
            chest_top = child;
        } else if (child.classList.contains('bag_container')) {
            prize_bag_container = child;
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


    // First remove the non-chosen chest
    non_chosen = choice == 'left' ? 'right' : 'left';
    Array.from(object.parentElement.children).forEach(sibling => {
        if (sibling.id.includes(non_chosen)) {
            removeObject(sibling);
        }
    });
    let base_timeout = 800;


    chest_top.classList.add('open_chest_rumble_animation');
    var audio = new Audio("../audio/open_chest_rumble.mp3");
    console.log("Playing audio");
    audio.play();

    // Reveal Prize if there is one
    if (prize_bag_container != null) {
        console.log("Prize has been found !")

        setTimeout(() => {
            chest_top.style.zIndex = "0";
        }, base_timeout + 1800);

        setTimeout(() => {
            revealCoinsAndBag(prize_bag_container, submit = false);
        }, base_timeout + 2200); // reveal prize after chest opens
        base_timeout += 12500;

    } else {
        console.log("No prize for this chest")
        setTimeout(() => {
            new Audio("../audio/empty_chest1.mp3").play();
            setTimeout(() => {
                new Audio("../audio/empty_chest2.mp3").play();
            }, 1000);

        }, base_timeout + 2200);
        base_timeout = 5500;

    }

    setTimeout(() => {
        chest_top.classList.remove('open_chest_rumble_animation');
        chest_top.classList.add('close_chest_simple_animation');
        setTimeout(() => {
            chest_top.classList.remove('close_chest_simple_animation');
        }, 500);
    }, base_timeout);

    setTimeout(() => {
        shiftPageOutLeft();
    }, base_timeout + 1000);

    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit("hi");
    }, base_timeout + 2500);
}

function revealCoinsAndBag(bagContainerObj, submit = true) {

    console.log("Revealing coin from bag:", bagContainerObj);
    showOverlay();

    const staggerDelayMs = 200;
    const bagContainerChildren = bagContainerObj.children

    let prizeBag = null;
    let prizeCoins = [];

    let choice = "";
    for (var child of bagContainerChildren) {
        if (child.classList.contains('prize_bag')) {
            prizeBag = child;
            if (child.id.includes('left')) {
                choice = 'left';
            } else if (child.id.includes('right')) {
                choice = 'right';
            } else {
                console.error("Fatal: Could not determine choice from bag id:", child.id);
            }
        } else {
            prizeCoins.push(child);
        }
    }

    // First remove the non-chosen chest
    var remove_delay = 0;

    if (submit) {
        non_chosen = choice == 'left' ? 'right' : 'left';
        Array.from(bagContainerObj.parentElement.children).forEach(sibling => {
            if (sibling.id.includes(non_chosen)) {
                removeObject(sibling);
            }
        });
        remove_delay = 800;
        recordChoice(choice);

    }


    var num_coins = prizeCoins.length;

    console.log("Found prize bag:", prizeBag);
    console.log("Found prize coins:", prizeCoins);

    // 1. Bring bag up

    delta_y = `calc(${prizeBag.style.height} * 2/3)`;
    console.log("Delta Y for bag rise:", delta_y);

    setTimeout(() => {
        for (var child of bagContainerChildren) {
            child.style.top = `calc(${child.style.top} - ${delta_y})`;
        }
    }, remove_delay);


    // 2. Open bag 
    setTimeout(() => {
        prizeBag.src = "/images/open_bag.png";
        var audio = new Audio("../audio/fanfare.wav");
        console.log("Playing audio");
        if (PLAY_AUDIO) {
            audio.play().catch((error) => {
                console.error("Audio playback failed:", error);
            });
        }

        setTimeout(() => {
            let coinsFinalY = `calc(${prizeBag.style.top} - ${prizeBag.style.height}/3)`;
            let coinsFinalX = []

            console.log("Final Y for coin reveal:", coinsFinalY);
            // TODO: Change this later to match the correct reveal animations
            if (num_coins == 1) {
                coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}/2) - ${prizeCoins[0].style.width}/2)`);
            } else if (num_coins == 2) {
                // i = 0 coin starts left, goes left
                coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}/3) - ${prizeCoins[0].style.width}/2)`);
                coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}*2/3) - ${prizeCoins[1].style.width}/2)`);
                coin_order = [0, 1];
                coin_delay = [0, 1];
            } else if (num_coins == 4) {
                // i = 0 coin starts bottom center, goes right
                // i = 1 coin starts left mid, goes mid left
                // i = 2 coin starts right mid, goes mid right
                // i = 3 coin starts top center, goes left
                let prize_bag_left = prizeBag.style.left;
                let prize_bag_width = prizeBag.style.width;
                let prize_coin_width = prizeCoins[0].style.width;
                coinsFinalX.push(`calc(${prize_bag_left} + ${prize_bag_width} - ${prize_coin_width}/2)`);
                coinsFinalX.push(`calc(${prize_bag_left} + ${prize_bag_width}/3 - ${prize_coin_width}/2)`);
                coinsFinalX.push(`calc(${prize_bag_left} + ${prize_bag_width}*2/3 - ${prize_coin_width}/2)`);
                coinsFinalX.push(`calc(${prize_bag_left} - ${prize_coin_width}/2)`);
                coin_order = [3, 1, 2, 0];
                coin_delay = [0, 1, 2, 3];
            } else {
                error("Fatal: Unsupported number of coins for reveal:", num_coins);
            }
            // 3. Reveal coins one by one, starting with the highest coin (last in list)

            for (let i = 0; i < coin_order.length; i++) {
                setTimeout(() => {
                    coin = coin_order[i];
                    prizeCoins[coin].style.top = coinsFinalY;
                    prizeCoins[coin].style.left = coinsFinalX[coin];

                }, coin_delay[i] * staggerDelayMs);
            }

            // Add bounce animation to bag after coins revealed
            for (let i = 0; i < coin_order.length; i++) {
                setTimeout(() => {
                    prizeCoins[coin_order[i]].classList.add('bounce_animation');
                }, (num_coins - 1) * staggerDelayMs + 1000 + i * staggerDelayMs / 2);
            }

            // Add animation for spiral into score
            for (let i = 0; i < coin_order.length; i++) {
                setTimeout(() => {
                    prizeCoins[coin_order[i]].classList.remove('bounce_animation');
                    prizeCoins[coin_order[i]].classList.add("prize_reveal_animation");
                    new Audio(`../audio/reward${i + 1}.mp3`).play();
                    setTimeout(() => {
                        prizeCoins[coin_order[i]].classList.remove("prize_reveal_animation");
                        startArcAnimation(prizeCoins[coin_order[i]]);
                    }, 900);
                }, (num_coins - 1) * 3 / 2 * staggerDelayMs + 1500 + i * 1000);
            }
            // }
        }, 500);
    }, remove_delay + 1000);

    setTimeout(() => {
        prizeBag.classList.add('shift_out_up_animation');
    }, remove_delay + (num_coins - 1) * 3 / 2 * staggerDelayMs + 4000 + num_coins * 1000);

    if (submit) {
        window.setTimeout(function () {
            SUBMITTING = true;
            document.querySelector('form').submit();
        }, remove_delay + (num_coins - 1) * 3 / 2 * staggerDelayMs + 4000 + num_coins * 1000 + 1000);
    }
}

function selectChest(object) {
    showOverlay();
    var audio = new Audio("../audio/pop.mp3");
    audio.play();

    children = object.children;

    let choice = "";
    if (object.id.includes('left')) {
        choice = 'left';
    } else if (object.id.includes('right')) {
        choice = 'right';
    } else {
        console.error("Fatal: Could not determine choice from object id:", object.id);
    }


    for (var child of children) {
        if (child.id.includes('chest')) {
            chest_top = child;
            chest_top.classList.add('pulse_animation');
        }
    }

    // First remove the non-chosen chest
    non_chosen = choice == 'left' ? 'right' : 'left';
    Array.from(object.parentElement.children).forEach(sibling => {
        if (sibling.id.includes(non_chosen)) {
            console.log("Removing sibling:", sibling);
            setTimeout(() => {
                removeObject(sibling);
            }, 700);
        }
    });


    // Record choice
    recordChoice(choice);




    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit();
    }, 2500);
}

function stage_1_animation() {
    /* Getting coin element */
    shiftPageInRight();
    var prizes = document.getElementsByClassName('prize');

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


    /* Resetting elements to correct positions */
    for (var prize of prizes) {
        prize.classList.add(prize_place_positions[0]);
    }

    for (var occluder of occluders) {
        occluder.classList.add('occluder-place-reset');
    }

    // Stage 0: Initial Delay (The 'oncreation' equivalent)

    const initialDelay = 2000; // Wait 0.5 seconds before starting
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
                        // Set z-index to behind
                        top.style.zIndex = "0";
                    }
                    if (PLAY_AUDIO) {
                        new Audio("../audio/open_chest_creak.mp3").play().catch((error) => {
                            console.error("Audio playback failed:", error);
                        });
                    }

                    // Introduce occluders, doesn't cover the chest yet
                    var occluder_timeout = (occluders.length > 0) ? 1800 : 1;

                    setTimeout(() => {
                        for (var occluder of occluders) {
                            occluder.classList.remove('occluder-place-reset');
                            // occluder.classList.add('occluder-place-1');
                        }


                        // Pull occluders down in front of chest. Removing occluder-place-1 will return occluders to their original position
                        // setTimeout(() => {
                        // for (var occluder of occluders) {
                        //     occluder.classList.remove('occluder-place-1');
                        // }

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
                                setTimeout(() => {
                                    new Audio("../audio/coin_placement.wav").play();

                                }, 700);

                                // Audio will not play unless a user interacts with the screen. Perhaps, add a "Click to Start" screen before starting the experiment.



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
                                        top.style.zIndex = "6";
                                    }
                                }, 600);


                                setTimeout(() => {


                                    for (var top of chest_top) {
                                        top.classList.remove('open_chest_simple_animation');
                                        top.classList.add('close_chest_simple_animation');
                                    }
                                    if (PLAY_AUDIO) {
                                        new Audio("../audio/open_chest_creak.mp3").play().catch((error) => {
                                            console.error("Audio playback failed:", error);
                                        });
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
                                        }, 1800);
                                    }, occluder_timeout);
                                }, 1200);

                            }, 800);

                        }, occluder_timeout);
                        // }, occluder_timeout);
                    }, 1000);
                }, 500);
            }, 2000);

        }, 1200);
    }, initialDelay);
}

function stage_2_animation() {
    /* Getting coin element */


    const hooks = document.getElementsByClassName('hook');
    for (var object of hooks) {
        if (object.id.includes('prize')) {
            hook_pos1_x = object.style.left;
            hook_pos1_y = object.style.top;
            var position = object.id.split('_')[2];
            var hook = object;
        }
        // else if (object.id.includes('chest')) {
        //     hook_pos2_x = object.style.left;
        //     hook_pos2_y = object.style.top;
        // }
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


    // var chest = document.getElementById(`chest_container_${position}`);

    // for (var child of chest.children) {
    //     child.style.transition = "all 1s linear";
    // }
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
            hook.style.left = hook_posreset_x;
            hook.style.top = hook_posreset_y;


            // for (var child of chest.children) {

            //     child.style.left = `calc(${hook_posreset_x} - ${hook_pos2_x} + ${child.style.left})`;
            //     child.style.top = `calc(${hook_posreset_y} - ${hook_pos2_y} + ${child.style.top})`;
            // }
            // Submit to kesar
            window.setTimeout(function () {
                SUBMITTING = true; // Kesar global variable
                document.querySelector('form').submit();
            }, 2000);
        }, 1200);

    }, 1200);
}



document.addEventListener('DOMContentLoaded', () => {
    // stage_1_animation();
    // disableBackButton();

    let stage = document.getElementById('stage_indicator').innerText;
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

function startArcAnimation(object) {

    const score_display = document.getElementById('score_display');
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const rippleEl = document.getElementById('ripple-overlay');

    // --- 1. Get Start and End Points ---
    const startX = object.style.left; // Assume VW/VH unit is intended
    const startY = object.style.top;

    const endX = 50;
    const endY = 5;

    // --- 2. Calculate Total Translation (Delta) in VW/VH Numbers ---
    const deltaX_num = `calc(${endX}vw - ${startX})`;
    const deltaY_num = `calc(${endY}vh - ${startY})`;

    // --- 3. Define Arc Bulge ---
    const totalBulgeVH = `calc(${deltaY_num} * -0.4)`; // increase as travel length increases

    // --- 4. Keyframe Generation Loop ---
    const keyframes = [];

    // Helper function for a parabola: f(t) = 4 * t * (1 - t)
    // This gives a value of 0 at t=0 and t=1, and a max height of 1 at t=0.5.
    const parabolicFactor = (t) => 4 * t * (1 - t);

    for (let i = 0; i <= 100; i += 5) {
        const t = i / 100; // time factor from 0.0 to 1.0

        // Apply the bulge factor weighted by the parabolic function
        const bulgeDisplacement = `calc(${totalBulgeVH} * ${parabolicFactor(t)})`;

        // FINAL TRANSFORM VALUES (Numbers)
        const finalX = `calc(${deltaX_num} * ${t})`;
        const finalY = `calc(${deltaY_num} * ${t} + ${bulgeDisplacement})`;


        const transformX = finalX; // Placeholder to keep the calc structure simple
        const transformY = finalY;

        var size = 1 - Math.max(i - 70, 0) * 1 / 30; // Start scaling down after 70% of the animation
        keyframes.push({
            offset: t,
            transform: `translate(${transformX}, ${transformY}) scale(${size})`, // Scale down to 30% size
        });
    }

    // --- 5. Define Animation Options ---
    const options = {
        duration: 700, // Longer duration for better visual smoothness
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', // Still linear for constant speed
        fill: 'forwards'
    };

    object.animate(keyframes, options);

    // --- 6. Run the Animation ---
    setTimeout(() => {
        object.classList.add('hidden');

        let curr_score = parseInt(score_display.innerText);
        score_display.innerText = (curr_score + 1).toString();
        setMeterValue((curr_score + 1).toString());

        score_display.style.fontSize = "6vw";
        setTimeout(() => {
            score_display.style.fontSize = "4vw";
        }, 300);


        //TESTING
        rippleEl.classList.remove('active');

        // Force a "Reflow" so the browser realizes we removed the class
        // (This is a necessary hack in JS animations)
        void rippleEl.offsetWidth;

        rippleEl.classList.add('active');


        // score_display.style.transform = "scale(1.05)";
        // setTimeout(() => {
        //     score_display.style.transform = "scale(1.0)";
        // }, 1000);

    }, options.duration);
}


function showOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'processing-overlay';
    Object.assign(overlay.style, {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        // backgroundColor: 'rgba(0,0,0,0.1)', // Slightly visible for feedback (TODO: REMOVE)
        zIndex: 9999
    });
    document.body.appendChild(overlay);
}

function setMeterValue(amount) {
    const meter = document.getElementById('score-meter');
    const ripple = document.getElementById('ripple-overlay');

    // 1. Update the green bar fill
    if (meter) {
        meter.style.width = amount + '%';
    }

    // 2. Position the Ripple Beam
    if (ripple) {
        // Reset classes for direction
        ripple.classList.remove('facing-right', 'facing-left');

        if (amount >= 50) {
            // --- SHOOT RIGHT ---
            // Start at 50%, Width is the difference (e.g. 70% - 50% = 20% width)
            ripple.style.left = '50%';
            ripple.style.right = 'auto'; // Clear right property
            ripple.style.width = (amount - 50) + '%';

            ripple.classList.add('facing-right');

        } else {
            // --- SHOOT LEFT ---
            // Start at amount (e.g. 30%), Width is difference (50% - 30% = 20%)
            // Visually, this spans from 30% to 50%
            ripple.style.left = amount + '%';
            ripple.style.right = 'auto';
            ripple.style.width = (50 - amount) + '%';

            ripple.classList.add('facing-left');
        }
    }
}

function shiftPageOutLeft() {


    experiment_doc = document.getElementById("experiment_screen");

    const allElements = [...experiment_doc.querySelectorAll('*')];

    // for (var child of experiment_doc.children) {
    for (var child of allElements) {
        if (child.classList.contains('keep_between_trials')) {
            console.log("Keeping element in place between trials:", child);
            // Do nothing, keep in place
        } else {
            if (child.children.length > 0) {
                for (var grandchild of child.children) {

                    grandchild.classList.add('shift_out_left_animation');
                }
            } else {
                child.classList.add('shift_out_left_animation');

            }
        }
    }
}

function shiftPageInRight() {
    experiment_doc = document.getElementById("experiment_screen");
    for (var child of experiment_doc.children) {
        if (child.classList.contains('keep_between_trials')) {
            console.log("Keeping element in place between trials:", child);
            // Do nothing, keep in place
        } else {
            if (child.children.length > 0) {
                for (var grandchild of child.children) {

                    grandchild.classList.add('shift_in_right_animation');
                }
            } else {
                child.classList.add('shift_in_right_animation');
            }
        }
    }

    setTimeout(() => {
        for (var child of experiment_doc.children) {
            if (child.classList.contains('keep_between_trials')) {
                console.log("Keeping element in place between trials:", child);
                // Do nothing, keep in place
            } else {
                if (child.children.length > 0) {
                    for (var grandchild of child.children) {
                        grandchild.classList.remove('shift_in_right_animation');
                    }
                } else {
                    child.classList.remove('shift_in_right_animation');
                }
            }
        }
    }, 1100);
}

// // This function adds a new, null state to the history
// // so the back button points to this dummy state.
// function disableBackButton() {
//     console.log("Disabling back button");
//     for (var i = 0; i < 10; i++) {
//         window.history.pushState(null, "", window.location.href);
//     }
//     // 2. Listen for the "Back" click (popstate)
//     window.onpopstate = function () {
//         // 3. When they click back, immediately push them forward again
//         window.history.pushState(null, "", window.location.href);
//     };
// }
