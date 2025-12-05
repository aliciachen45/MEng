const PLAY_AUDIO = true;
const SCRIPT_PATH = "../audio/script";

// --- Async Helpers ---

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function playAudio(src, basePath = null) {
    if (typeof PLAY_AUDIO !== 'undefined' && !PLAY_AUDIO) return Promise.resolve();

    const fullPath = basePath ? `${basePath}/${src}` : src;

    return new Promise((resolve, reject) => {
        const audio = new Audio(fullPath);
        audio.addEventListener('ended', () => resolve());
        audio.addEventListener('error', (e) => {
            console.error("Audio playback error:", e);
            resolve();
        });
        console.log("Playing audio (awaitable):", fullPath);
        audio.play().catch((e) => {
            console.error("Autoplay failed/blocked:", e);
            resolve();
        });
    });
}

async function add_script(audio_src, delay = 0) {
    if (delay > 0) await wait(delay);
    await playAudio(audio_src, SCRIPT_PATH);
}

// --- Animation Components (Async) ---


function triggerOval() {
    const highlight = document.getElementById('score_highlight');
    highlight.classList.add('oval-highlight-animation');
}
/**
 * Handles the page sliding in from the right.
 * Resolves when the animation is fully complete and cleanup is done.
 */
async function shiftPageInRight() {
    const experiment_doc = document.getElementById("experiment_screen");
    const elements = experiment_doc.children;

    // 1. Add classes to trigger slide-in
    for (var child of elements) {
        if (!child.classList.contains('keep_between_trials')) {
            if (child.children.length > 0) {
                for (var grandchild of child.children) grandchild.classList.add('shift_in_right_animation');
            } else {
                child.classList.add('shift_in_right_animation');
            }
        }
    }

    // 2. Wait for animation duration
    await wait(1100);

    // 3. Cleanup classes
    for (var child of elements) {
        if (!child.classList.contains('keep_between_trials')) {
            if (child.children.length > 0) {
                for (var grandchild of child.children) grandchild.classList.remove('shift_in_right_animation');
            } else {
                child.classList.remove('shift_in_right_animation');
            }
        }
    }
}

/**
 * Handles the page sliding out to the left.
 */
async function shiftPageOutLeft() {

    experiment_doc = document.getElementById("experiment_screen");
    console.log("Shifting experiment screen out left:", experiment_doc);
    for (var child of experiment_doc.children) {
        console.log("Shifting child out left:", child);
        if (child.classList.contains('keep_between_trials')) {
            console.log("Keeping element in place between trials:", child);
            // Do nothing, keep in place
        } else {
            if (child.children.length > 0) {
                for (var grandchild of child.children) {

                    grandchild.classList.add('shift_out_left_animation');
                }
            } else {
                console.log("No grandchildren found for child:", child);
                child.classList.add('shift_out_left_animation');

            }
        }
    }
    await wait(1000);
}

/**
 * Drops coins into the bag one by one.
 */
async function placeCoinsInBag(prize_place_positions) {
    const staggerDelayMs = 100;
    const prize_elements = document.getElementsByClassName('prize');
    const coins = [];

    for (var prize of prize_elements) {
        if (prize.id.includes('filled_bag_coin_')) {
            coins.push(prize);
        }
    }

    for (let i = 0; i < coins.length; i++) {
        if (i > 0) await wait(staggerDelayMs);

        coins[i].classList.remove(prize_place_positions[0]);
        coins[i].classList.add(prize_place_positions[1]);

        // Non-blocking sound
        setTimeout(() => new Audio("../audio/drop_coin.mp3").play(), 750);
    }
    // Wait for the last coin's animation to roughly finish
    await wait(800);
}

/**
 * Handles the visual entry of occluders (flags).
 */
async function animateOccludersEnter(occluders) {
    if (occluders.length === 0) return;

    for (var occluder of occluders) {
        occluder.classList.remove('occluder-place-reset');
    }
    await wait(1200);
}

/**
 * Handles the removal of occluders.
 */
async function animateOccludersExit(occluders) {
    if (occluders.length === 0) return;

    for (var occluder of occluders) {
        occluder.classList.add('occluder-place-reset');
        occluder.style.transition = "all 2s ease-in-out";
    }
    await wait(2000); // Wait for them to leave
}

/*
 Handles coin placement
 */
async function animateCoinMove(prizes, positions) {
    // 1. "Watch this..."
    var trial_type = document.getElementById("trial_type").innerText;
    if (trial_type != "testing") {

        await add_script('watch.wav', 500);
    }

    // 2. Move to Center Mid
    for (var prize of prizes) {
        prize.classList.remove(positions[1]);
        prize.classList.add(positions[2]);
    }
    await wait(800); // Allow move to happen

    // 3. Move to Final (Hidden)
    for (var prize of prizes) {
        prize.classList.remove(positions[2]);
    }

    await wait(700);
    await playAudio("../audio/coin_placement.wav");
}

/**
 * Handles the Hook movement sequence in Stage 2
 */
async function animateHookSequence(hook, prize_elements, original_positions, reset_delta) {
    // 1. Intro Audio
    var play_hook_intro = document.getElementById("play_hook_intro").innerText;
    if (play_hook_intro == "True") {
        await add_script("hook_comes.wav", 500);
    } else {
        await add_script("here_comes_hook.wav", 500);
    }

    // 2. Play specific hook count audio
    await add_script(`hook_${prize_elements.length - 1}.wav`, 0);

    // 3. Move Prize Back to original (In front of chest)
    //    We simulate the hook pulling them by just moving them instantly 
    //    after the delay (as per original logic logic) or animating them.
    //    Original Logic: Waited 3500ms then snapped them back.

    for (let i = 0; i < prize_elements.length; i++) {
        prize_elements[i].style.left = original_prize_positions[i].left;
        prize_elements[i].style.top = original_prize_positions[i].top;
    }

    const [hook_x, hook_y] = [hook.style.left, hook.style.top]; // Current reset pos

    // Move hook to target
    // Note: To animate this properly, we'd need to know the 'target' pos. 
    // Assuming the calling function sets up the DOM state or we snap it.
    // Based on original code, we just snap DOM properties.

    // 4. Retract Hook
    await wait(1200);
    // Reset hook to off-screen
    // (Caller needs to handle specific coord calculations or we pass them in)
}


// --- Main Logic ---

function startExperiment() {
    window.setTimeout(function () {
        SUBMITTING = true;
        document.querySelector('form').submit("hi");
    }, 300);
}

function recordChoice(choice) {
    const hiddenInput = document.getElementById('choice_input');
    if (hiddenInput) hiddenInput.value = choice;
}

function showOverlay() {
    // const overlay = document.createElement('div');
    // overlay.id = 'processing-overlay';
    // Object.assign(overlay.style, {
    //     position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: 9999
    // });
    // document.body.appendChild(overlay);
    const overlay = document.getElementById('processing-overlay');
    overlay.style.zIndex = 9999;
}

function removeObject(object) {
    const allElements = [object, ...object.querySelectorAll('*')];
    allElements.forEach(element => {
        element.style.transition = "all 1s linear";
        requestAnimationFrame(() => {
            element.style.top = `calc(${element.style.top} + -100vh)`;
        });
    });
}

/**
 * Stage 1 Animation (Intro)
 */
async function stage_1_animation() {
    // 1. Slide In
    await shiftPageInRight();

    // --- Setup Variables ---
    var prizes = document.getElementsByClassName('prize');
    if (prizes.length === 0) return;
    const bag_container = document.getElementsByClassName('bag_container');
    let bag = null;
    for (var prize of prizes) { if (prize.classList.contains('prize_bag')) bag = prize; }
    const chest_top = document.getElementsByClassName('chest_top_image');
    let prize_side = bag_container[0].id.includes('right') ? "right" : "left";
    let prize_place_positions = (prize_side == "left")
        ? ['prize-place-left-reset', 'prize-place-left-1', 'prize-place-left-2']
        : ['prize-place-right-reset', 'prize-place-right-1', 'prize-place-right-2'];
    const occluders = document.getElementsByClassName('occluder');

    // Reset positions
    for (var prize of prizes) prize.classList.add(prize_place_positions[0]);
    for (var occluder of occluders) occluder.classList.add('occluder-place-reset');

    // --- Audio Intro ---
    var first_trial = document.getElementById("first_trial").innerText;
    if (first_trial == "True") {
        await add_script("look_treasure_chest.wav");
    } else {
        await add_script("now_look_treasure_chest.wav");
    }

    // --- Reveal Elements ---
    for (var occluder of occluders) occluder.classList.remove('hidden');
    for (var prize of prizes) prize.classList.remove('hidden');

    // --- Bag & Coin Sequence ---
    await wait(500);

    // Move bag to center
    bag.classList.remove(prize_place_positions[0]);
    bag.classList.add(prize_place_positions[1]);
    await wait(1200);

    // Drop coins (Async)
    await placeCoinsInBag(prize_place_positions);

    // Close Bag
    await wait(500); // Short pause after coins drop
    bag.src = "/images/closed_bag.png";
    if (first_trial == "True") {
        await add_script(`${prizes.length - 1}_coins_in_bag.wav`);
    } else {
        await add_script(`bag_has_${prizes.length - 1}_coins.wav`);
    }

    // --- Open Chest (Empty) ---
    await wait(500);
    for (var top of chest_top) {
        top.classList.add('open_chest_simple_animation');
        top.style.zIndex = "0";
    }
    if (PLAY_AUDIO) new Audio("../audio/open_chest_creak.mp3").play();

    // --- Occluders Enter (Async) ---
    await wait(1000);

    // This function handles the loop and timing of flags dropping
    await animateOccludersEnter(occluders);

    // Flag Audio
    if (occluders.length > 0) {
        var play_flag_intro = document.getElementById("play_flag_intro").innerText;

        if (play_flag_intro == "True") {
            await add_script("intro_flags.wav");
        }
    }
    await wait(500);


    setTimeout(() => {
        for (var top of chest_top) {
            top.style.zIndex = "6";
        }
    }, 3700);
    // --- Coin Magic Trick (Async) ---
    await animateCoinMove(prizes, prize_place_positions);

    // --- Close Chest ---
    // await wait(100);

    for (var top of chest_top) {
        top.classList.remove('open_chest_simple_animation');
        top.classList.add('close_chest_simple_animation');
    }
    if (PLAY_AUDIO) new Audio("../audio/open_chest_creak.mp3").play();

    // --- Occluders Exit (Async) ---
    await wait(1000); // Pause before lifting
    await animateOccludersExit(occluders);

    // --- Final Prompt ---

    var num_stages = document.getElementById("num_stages").innerText;
    if (first_trial == "True" && num_stages == "1") {
        await add_script("prompt_click.wav");
    } else {
        await add_script("which_open.wav");
    }

    // --- Submit ---
    // SUBMITTING = true;
    // document.querySelector('form').submit();

    prize_chest_container = document.getElementById(`chest_container_${prize_side}`);
    prize_chest_container.appendChild(bag_container[0]);

    const overlay = document.getElementById('processing-overlay');
    overlay.style.zIndex = -1;
}

/**
 * Stage 2 Animation (Hook)
 */
async function stage_2_animation() {
    let hook, hook_pos1_x, hook_pos1_y, position;

    const hooks = document.getElementsByClassName('hook');
    for (var object of hooks) {
        if (object.id.includes('prize')) {
            hook_pos1_x = object.style.left;
            hook_pos1_y = object.style.top;
            position = object.id.split('_')[2];
            hook = object;
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

    // Calculate Reset positions
    let reset_deltax = "", reset_deltay = "";
    if (position == "right") {
        reset_deltax = "40vw"; reset_deltay = "-20vh";
    } else if (position == "left") {
        reset_deltax = "-40vw"; reset_deltay = "-20vh";
    }

    const hook_posreset_x = `calc(${hook_pos1_x} + ${reset_deltax})`;
    const hook_posreset_y = `calc(${hook_pos1_y} + ${reset_deltay})`;

    // Apply Initial Reset (Hidden offscreen)
    for (let i = 0; i < prize_elements.length; i++) {
        prize_elements[i].style.left = `calc(${original_prize_positions[i].left} + ${reset_deltax})`;
        prize_elements[i].style.top = `calc(${original_prize_positions[i].top} + ${reset_deltay})`;
    }

    hook.style.left = hook_posreset_x;
    hook.style.top = hook_posreset_y;

    hook.classList.remove('hidden');
    for (var obj of prize_elements) obj.classList.remove('hidden');

    // --- Hook Audio Sequence (Async) ---
    var play_hook_intro = document.getElementById("play_hook_intro").innerText;
    console.log("Play hook intro", play_hook_intro);



    if (play_hook_intro == "True") {

        setTimeout(async () => {
            await add_script("hook_comes.wav");
            await add_script(`hook_${prize_elements.length - 1}.wav`);
            add_script("now_which_open.wav");

        }, 0);
        for (let i = 0; i < prize_elements.length; i++) {
            prize_elements[i].style.left = original_prize_positions[i].left;
            prize_elements[i].style.top = original_prize_positions[i].top;
        }


        // Visual: Hook is at chest
        hook.style.left = hook_pos1_x;
        hook.style.top = hook_pos1_y;

        // --- Retract Hook ---
        await wait(1200);
        hook.style.left = hook_posreset_x;
        hook.style.top = hook_posreset_y;

        await wait(1200);
    } else {
        for (let i = 0; i < prize_elements.length; i++) {
            prize_elements[i].style.left = original_prize_positions[i].left;
            prize_elements[i].style.top = original_prize_positions[i].top;
        }


        // Visual: Hook is at chest
        hook.style.left = hook_pos1_x;
        hook.style.top = hook_pos1_y;

        // --- Retract Hook ---
        await wait(1200);
        hook.style.left = hook_posreset_x;
        hook.style.top = hook_posreset_y;

        await add_script(`hook_${prize_elements.length - 1}_short.wav`);
        add_script("now_which_open.wav");

    }
    hook.classList.add('hidden');


    var hooked_prize_bag = document.getElementById(`hooked_prize_${position}_bag`);
    var grandparent = hooked_prize_bag.parentElement.parentElement;
    grandparent.appendChild(hooked_prize_bag);

    // --- Submit ---
    const overlay = document.getElementById('processing-overlay');
    overlay.style.zIndex = -1;
}

/**
 * Main Interaction: Select Chest
 */
async function selectChest(object) {
    showOverlay();
    playAudio("../audio/pop.mp3");

    let choice = object.id.includes('left') ? 'left' : 'right';
    let chest_top = null;

    for (var child of object.children) {
        if (child.id.includes('chest')) {
            chest_top = child;
            chest_top.classList.add('pulse_animation');
        }
    }

    // Remove non-chosen chest
    const non_chosen = choice == 'left' ? 'right' : 'left';
    Array.from(object.parentElement.children).forEach(sibling => {
        if (sibling.id.includes(non_chosen)) {
            // Async removal not strictly necessary here as we just want it gone
            // but we can delay slightly to match pulse
            setTimeout(() => removeObject(sibling), 700);
        }
    });

    recordChoice(choice);
    await wait(2500);

    SUBMITTING = true;
    document.querySelector('form').submit();
}

/**
 * Main Interaction: Open Chest
 */
/**
 * Plays the response audio based on game state.
 * Fully Async: Waited for audio to finish before resolving.
 */
async function coin_reveal_response(prize_bag_container) {
    var trial_type = document.getElementById("trial_type").innerText;
    const num_coins_chosen = prize_bag_container ? prize_bag_container.children.length - 1 : 0;

    console.log(`Response: Trial type ${trial_type}, Coins: ${num_coins_chosen}`);

    if (trial_type == "testing") {
        if (num_coins_chosen > 0) {
            // Play "Great Job" and wait for it to finish
            await add_script("great_job", 0);

            // Play number of coins (with a small natural pause of 200ms between sentences)
            await add_script(`${num_coins_chosen}_coins.wav`, 200);
        } else {
            await add_script("oh_no_no_coins.wav", 0);
        }
    } else {
        // Main Game Logic
        var max_possible_coins = document.getElementById("max_coins").innerText;

        if (num_coins_chosen == 0) {
            await add_script("lets_try_again.mp3", 0);
        } else if (num_coins_chosen == max_possible_coins) {
            var num_stages = document.getElementById("num_stages").innerText;

            if (num_stages == "2") {
                await add_script("great_job.wav", 0);
            } else {
                // var first_trial = document.getElementById("first_trial").innerText;
                // if (first_trial == "True") {
                //     await add_script("great_job_watch.mp3", 0);
                // } else {
                await add_script("great_job_found.wav", 0);
                // }
            }
        } else {
            await add_script("nice_try_again.wav", 0);
        }
    }
}

/**
 * Main Interaction: Open Chest
 * Now fully compatible with async audio responses.
 */
async function openChest(object) {
    showOverlay();

    const children = object.children;
    let chest_top = null;
    let prize_bag_container = null;

    for (var child of children) {
        if (child.id.includes('chest_top_image')) chest_top = child;
        else if (child.classList.contains('bag_container')) prize_bag_container = child;
    }

    let choice = object.id.includes('left') ? 'left' : 'right';
    recordChoice(choice);

    // Remove non-chosen chest
    const non_chosen = choice == 'left' ? 'right' : 'left';


    Array.from(object.parentElement.children).forEach(sibling => {
        if (sibling.id.includes(non_chosen)) {
            // Async removal not strictly necessary here as we just want it gone
            // but we can delay slightly to match pulse
            removeObject(sibling)
        }
    });

    // 1. Initial Wait
    await wait(800);

    // 2. Rumble
    chest_top.classList.add('open_chest_rumble_animation');
    playAudio("../audio/open_chest_rumble.mp3");

    // 3. Open
    await wait(1600);
    chest_top.style.zIndex = "0";

    // 4. Reveal Prize Logic
    await wait(600);

    if (prize_bag_container != null) {
        console.log("Prize has been found!");
        // Await the full coin reveal animation sequence
        await revealCoinsAndBag(prize_bag_container, false);
    } else {
        console.log("No prize for this chest");
        await playAudio("../audio/empty_chest1.mp3");
        await playAudio("../audio/empty_chest2.mp3");
    }

    // Execution effectively PAUSES here until the voiceover is completely done
    await coin_reveal_response(prize_bag_container);

    // 6. Close Chest
    // Small buffer after talking stops
    await wait(500);

    chest_top.classList.remove('open_chest_rumble_animation');
    chest_top.classList.add('close_chest_simple_animation');
    setTimeout(() => chest_top.classList.remove('close_chest_simple_animation'), 500);

    // 7. Shift Page Out (Async)
    await wait(1100);
    await shiftPageOutLeft();

    // // 8. Submit
    SUBMITTING = true;
    document.querySelector('form').submit("hi");
}

async function revealCoinsAndBag(bagContainerObj, submit = true) {
    console.log("Revealing coin from bag:", bagContainerObj);
    showOverlay();

    const staggerDelayMs = 200;
    const bagContainerChildren = bagContainerObj.children;
    let prizeBag = null;
    let prizeCoins = [];
    let choice = "";

    for (var child of bagContainerChildren) {
        if (child.classList.contains('prize_bag')) {
            prizeBag = child;
            choice = child.id.includes('left') ? 'left' : 'right';
        } else {
            prizeCoins.push(child);
        }
    }

    if (submit) {
        const non_chosen = choice == 'left' ? 'right' : 'left';
        Array.from(bagContainerObj.parentElement.children).forEach(sibling => {
            if (sibling.id.includes(non_chosen)) removeObject(sibling);
        });
        // Array.from(document.querySelectorAll('*')).forEach(element => {
        //     if (element.id.includes(non_chosen)) removeObject(element);
        // });
        await wait(800);
        recordChoice(choice);
    }

    const num_coins = prizeCoins.length;

    // 1. Bring bag up
    const delta_y = `calc(${prizeBag.style.height} * 2/3)`;
    for (var child of bagContainerChildren) {
        child.style.top = `calc(${child.style.top} - ${delta_y})`;
    }
    await wait(1000);

    // 2. Open bag
    prizeBag.src = "/images/open_bag.png";
    playAudio("../audio/fanfare.wav");
    await wait(500);

    // Calculate Coordinates (Simplified from original for brevity, logic preserved)
    let coinsFinalY = `calc(${prizeBag.style.top} - ${prizeBag.style.height}/3)`;
    let coinsFinalX = [];
    let coin_order = [];

    if (num_coins == 1) {
        coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}/2) - ${prizeCoins[0].style.width}/2)`);
        coin_order = [0];
    } else if (num_coins == 2) {
        coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}/3) - ${prizeCoins[0].style.width}/2)`);
        coinsFinalX.push(`calc(${prizeBag.style.left} + ${prizeBag.style.width}*2/3) - ${prizeCoins[1].style.width}/2)`);
        coin_order = [0, 1];
    } else if (num_coins == 4) {
        let pb_left = prizeBag.style.left;
        let pb_width = prizeBag.style.width;
        let pc_width = prizeCoins[0].style.width;
        coinsFinalX.push(`calc(${pb_left} + ${pb_width} - ${pc_width}/2)`);
        coinsFinalX.push(`calc(${pb_left} + ${pb_width}/3 - ${pc_width}/2)`);
        coinsFinalX.push(`calc(${pb_left} + ${pb_width}*2/3 - ${pc_width}/2)`);
        coinsFinalX.push(`calc(${pb_left} - ${pc_width}/2)`);
        coin_order = [3, 1, 2, 0];
    }

    // 3. Reveal coins loop
    for (let i = 0; i < coin_order.length; i++) {
        if (i > 0) await wait(staggerDelayMs);
        const coinIndex = coin_order[i];
        prizeCoins[coinIndex].style.top = coinsFinalY;
        prizeCoins[coinIndex].style.left = coinsFinalX[coinIndex];
    }
    await wait(1000);

    // 4. Bounce
    for (let i = 0; i < coin_order.length; i++) {
        if (i > 0) await wait(staggerDelayMs / 2);
        prizeCoins[coin_order[i]].classList.add('bounce_animation');
    }
    await wait(800);

    // Add animation for spiral into score
    trigger_highlight = document.getElementById("score_highlight");
    if (trigger_highlight != null) {
        triggerOval();
        await add_script("highlight.wav");
    }


    for (let i = 0; i < coin_order.length; i++) {
        setTimeout(() => {
            prizeCoins[coin_order[i]].classList.remove('bounce_animation');
            prizeCoins[coin_order[i]].classList.add("prize_reveal_animation");
            new Audio(`../audio/reward${i + 1}.mp3`).play();
            setTimeout(() => {
                prizeCoins[coin_order[i]].classList.remove("prize_reveal_animation");
                startArcAnimation(prizeCoins[coin_order[i]]);
            }, 900);
        }, i * 1000);
    }
    await wait(coin_order.length * 1000);

    if (submit) {
        await coin_reveal_response(bagContainerObj);
    }

    prizeBag.classList.add('shift_out_up_animation');
    await wait(1200);

    if (submit) {
        await shiftPageOutLeft();
        SUBMITTING = true;
        document.querySelector('form').submit();
    }
}

async function coin_reveal_response(prize_bag_container) {
    var trial_type = document.getElementById("trial_type").innerText;
    const num_coins_chosen = prize_bag_container ? prize_bag_container.children.length - 1 : 0;

    console.log(`Response: Trial type ${trial_type}, Coins: ${num_coins_chosen}`);

    if (trial_type == "testing") {
        if (num_coins_chosen > 0) {
            // Play "Great Job" and wait for it to finish
            await add_script("great_job", 0);

            // Play number of coins (with a small natural pause of 200ms between sentences)
            await add_script(`${num_coins_chosen}_coins.wav`, 200);
        } else {
            await add_script("oh_no_no_coins.wav", 0);
        }
    } else {
        // Main Game Logic
        var max_possible_coins = document.getElementById("max_coins").innerText;

        if (num_coins_chosen == 0) {
            await add_script("lets_try_again.mp3", 0);
        } else if (num_coins_chosen == max_possible_coins) {
            var num_stages = document.getElementById("num_stages").innerText;

            if (num_stages == "2") {
                await add_script("great_job.wav", 0);
            } else {
                // var first_trial = document.getElementById("first_trial").innerText;
                // if (first_trial == "True") {
                //     await add_script("great_job_watch.mp3", 0);
                // } else {
                await add_script("great_job_found.wav", 0);
                // }
            }
        } else {
            await add_script("nice_try_again.wav", 0);
        }
    }
}

async function startArcAnimation(object) {
    const score_display = document.getElementById('score_display');
    const rippleEl = document.getElementById('ripple-overlay');

    const startX = object.style.left;
    const startY = object.style.top;
    const endX = 50;
    const endY = 5;

    const deltaX_num = `calc(${endX}vw - ${startX})`;
    const deltaY_num = `calc(${endY}vh - ${startY})`;
    const totalBulgeVH = `calc(${deltaY_num} * -0.4)`;

    const keyframes = [];
    const parabolicFactor = (t) => 4 * t * (1 - t);

    for (let i = 0; i <= 100; i += 5) {
        const t = i / 100;
        const bulgeDisplacement = `calc(${totalBulgeVH} * ${parabolicFactor(t)})`;
        const finalX = `calc(${deltaX_num} * ${t})`;
        const finalY = `calc(${deltaY_num} * ${t} + ${bulgeDisplacement})`;
        var size = 1 - Math.max(i - 70, 0) * 1 / 30;
        keyframes.push({
            offset: t,
            transform: `translate(${finalX}, ${finalY}) scale(${size})`,
        });
    }

    const options = { duration: 700, easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', fill: 'forwards' };
    const animation = object.animate(keyframes, options);
    await animation.finished;

    object.classList.add('hidden');
    let curr_score = parseInt(score_display.innerText);
    score_display.innerText = (curr_score + 1).toString();
    setMeterValue((curr_score + 1).toString());

    score_display.style.fontSize = "6vw";
    setTimeout(() => { score_display.style.fontSize = "4vw"; }, 300);

    rippleEl.classList.remove('active');
    void rippleEl.offsetWidth;
    rippleEl.classList.add('active');
}

function setMeterValue(amount) {
    const meter = document.getElementById('score-meter');
    const ripple = document.getElementById('ripple-overlay');
    if (meter) meter.style.width = amount + '%';
    if (ripple) {
        ripple.classList.remove('facing-right', 'facing-left');
        if (amount >= 50) {
            ripple.style.left = '50%'; ripple.style.right = 'auto'; ripple.style.width = (amount - 50) + '%';
            ripple.classList.add('facing-right');
        } else {
            ripple.style.left = amount + '%'; ripple.style.right = 'auto'; ripple.style.width = (50 - amount) + '%';
            ripple.classList.add('facing-left');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let stage = document.getElementById('stage_indicator').innerText;
    let back_button_note = document.getElementById('backbutton_note');
    console.log("Current stage:", stage);
    if (stage == '1') {
        back_button_note.classList.add('hidden');
        stage_1_animation()
    }
    else if (stage == '2') {
        back_button_note.classList.add('hidden');
        stage_2_animation();
    }

});
