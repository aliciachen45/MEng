TODOS:


Animations:
+ Flyaway (coin exiting)
+ Hook enter + grab chest and exit out
+ Hook enter and drop coin and out
+ Bounce
+ Coin out of bag
+ Selection
+ Treasure chest should SEE NOTHING BEHIND
+ Coin initial, entrance to one of the chests
    + Mostly done, fix the exact positioning

Trials types:
(all coins are in a bag)
+ Training:
    + 1 coin -> into one of 2 chests, no occluder -> choice 1 -> END
    + 1 coin -> into one of 2 chests, with occluder -> choice 1 -> END
    + 2 coin -> into one of 2 chests, no occluder -> choice 1 -> replace with 1 coin -> choice 2 -> END
    + 1 coin -> into one of 2 chests, no occluder -> choice 1 -> replace with 2 coin -> choice 2 -> END

+ Testing:
    + 2 coin -> into 1 chest -> add 1 coin -> choice 1 -> END
    + 2 coin -> into one of 2 chests, fully occluded -> choice 1 -> replace with 1 coin -> choice 2 -> END (EV equal)
    + 4 coin -> into one of 2 chests, fully occluded -> choice 1 -> replace with 1 coin -> choice 2 -> END (EV unequal)

(1, 2) -> Replication, (2, 3) -> new, (1, 3) -> new


Counterbalancing:
+ The coin is on the left or the right chest
+ Different colors
+ Different sizes

Saving data:
+ How to save the responses to a json
+ And how to counterbalance between the different trial types

Logic:
+ Repeating the training if they get it wrong the first time, if get it wrong 2 times, they can continue but throw they aren't included
    + For each o the training trials
+ Repeat the testing __ times, with pseudo random order

