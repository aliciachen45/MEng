## Setup and load data ----
library(dplyr)
library(tidyverse)
library("lme4")
install.packages(c("Matrix", "lme4"), type = "binary", dependencies = TRUE)
if(!require(pacman)) {install.packages("pacman");require("pacman")}
p_load("rstanarm", "XNomial", "emmeans", "sjPlot", "tidybayes", "gt", "lme4", "bayestestR", "lubridate", "rstudioapi", "diptest", "gridExtra", "officer", "tidyverse")
current_path <- getActiveDocumentContext()$path ## gets path for current R script
setwd(dirname(current_path)) ## sets dir to R script path

df <- read.csv("all_logs.csv") |>
  as_tibble() |>
  mutate(id = as.integer(factor(child_id))) |>
  select(id, group, trial_number, prize_side, coins1, choice1, coins_recieved, test_trial, trial_type, coins2, choice2)


## Some basic data shaping ----
test.df <- df %>%
  filter(test_trial == "True") %>%
  mutate(trial.type = case_when(trial_type == 1 ~ "inferred2cVsKnown1c",
                                trial_type == 2 ~ "unknown4cVsKnown1c",
                                trial_type == 3 ~ "unknown2cVsKnown1c"),
         final.choice = ifelse(choice1 == choice2, "chest", "bag") %>% factor(levels = c("chest", "bag"))) %>%
  select(id, group, trial_number, trial.type, final.choice)

# Make sure I generate the same numbers as Alicia
test.df %>%
  group_by(id, trial.type) %>%
  summarize(prop.bag = mean(final.choice == "bag")) %>%
  print(n = 21)



# Check whether there’s any kids who always choose the bag on the unknown trial types
# With 7 kids, 1 always chose the bag over 6 trials
#test.df %>%
  #group_by(id, trial.type) %>%
  #summarize(prop.bag = mean(final.choice == "bag")) %>%
  #filter(trial.type != "inferred2cVsKnown1c", prop.bag == 1)
#test.df

## Model data ----
test.mod <- glmer(final.choice ~ trial.type + (1|id), family = "binomial", data = test.df)
emmeans(test.mod, specs = "trial.type") %>% pairs()

test.plot <- emmeans(test.mod, specs = "trial.type", type = "response") %>%
  as_tibble()

test.ind.props <- test.df %>%
  group_by(id, trial.type) %>%
  summarize(prop.bag = mean(final.choice == "bag"))

ggplot(test.plot, aes(x = trial.type, y = prob)) +
  geom_errorbar(aes(ymin = asymp.LCL, ymax = asymp.UCL), width = .2) +
  geom_point(size = 4, shape = 23, fill = "white") +
  geom_dotplot(data = test.ind.props, aes(x = trial.type, y = prop.bag), binaxis = "y", stackdir = "center", color = "white") +
  ylim(0,1) +
  theme_bw() +
  labs(y = "Probability of choosing the bag")


# Power analysis
fixed_effects <- fixef(test.mod) 
fixed_effects

# how much individual kids vary from the average (for control)
child_std <- as.data.frame(VarCorr(test.mod))$sdcor[1]

# ev-calculators
ev_kid <- function(trial_type, epsilon = 0.1) {
  if (trial_type == "unknown2cVsKnown1c") {
    ifelse(runif(1) < 0.5, "chest", "bag")
  } else {
    ifelse(runif(1) < 1 - epsilon, "chest", "bag")
  }
}

# uncertainty-calcualtors
uncertain_kid <- function(trial_type, epsilon1 = 0.1, epsilon2 = 0.1) {
  if (trial_type == "inferred2cVsKnown1c") {
    ifelse(runif(1) < 1 - epsilon1, "chest", "bag")
  } else {
    ifelse(runif(1) < 1 - epsilon2, "bag", "chest")
  }
}


########
# Method 1: aggregate everything
########
# data from pilot testin
observed_props <- test.df %>%
  group_by(trial.type) %>%
  summarize(real_prop = mean(final.choice == "bag"))


# find the error for the specific simulation


calculate_sim_error <- function(prop_ev, eps_ev, eps_un1, eps_un2) {
  n_sim <- 100
  types <- c("inferred2cVsKnown1c", "unknown4cVsKnown1c", "unknown2cVsKnown1c")
  
  sim_data <- expand.grid(id = 1:n_sim, trial.type = types, rep = 1:4) %>%
    mutate(strategy = sample(c("EV", "Uncertainty"), n(), replace = TRUE, prob = c(prop_ev, 1-prop_ev))) %>%
    rowwise() %>%
    mutate(choice = case_when(
      strategy == "EV" ~ ev_kid(trial.type, eps_ev),
      strategy == "Uncertainty" ~ uncertain_kid(trial.type, eps_un1, eps_un2)
    )) %>%
    group_by(trial.type) %>%
    summarize(sim_prop = mean(choice == "bag"))
  
  sim_data
  
  # Join with real data and calculate RMSE
  comparison <- left_join(observed_props, sim_data, by = "trial.type")
  rmse <- sqrt(mean((comparison$real_prop - comparison$sim_prop)^2))
  return(rmse)
}

#from sample data, assume prop_ev
param_grid <- expand.grid(
  prop_ev = seq(0.1, 0.9, by = 0.1),
  ev_eps = seq(0.01, 0.3, by = 0.05),
  un_eps1 = seq(0.01, 0.3, by = 0.05),
  un_eps2 = seq(0.01, 0.3, by = 0.05)
)

fit_results <- param_grid %>%
  rowwise() %>%
  mutate(error = calculate_sim_error(prop_ev, ev_eps, un_eps1, un_eps2)) %>%
  ungroup()

# Find the best parameters (lowest error)
best_params <- fit_results %>% filter(error == min(error))
print(best_params)

prop_ev = best_params$prop_ev
ev_eps = best_params$ev_eps
un_eps1 = best_params$un_eps1
un_eps2 = best_params$un_eps2

############
# Method 2:By assuming prop_ev from sample
###########
test.observed_uncertain_kids <- test.df %>% 
  filter(id %in% c(1, 2))  
test.observed_ev_kids <- test.df %>%
  filter(!(id %in% c(1, 2)))

observed_ev_props <- test.observed_ev_kids  %>%
  group_by(trial.type) %>%
  summarize(real_prop = mean(final.choice == "bag"))

observed_uncertain_props <- test.observed_uncertain_kids  %>%
  group_by(trial.type) %>%
  summarize(real_prop = mean(final.choice == "bag"))


calc_ev_error <- function(eps, n, reps=50) {
  errors <- replicate(reps, {
    sim <- expand.grid(id = 1:n, trial.type = observed_ev_props$trial.type, rep = 1:4) %>%
      rowwise() %>%
      mutate(choice = ev_kid(trial.type, eps)) %>%
      group_by(trial.type) %>%
      summarize(sim_prop = mean(choice == "bag"), .groups = "drop")
    
    comparison <- left_join(observed_ev_props, sim, by = "trial.type")
    sqrt(mean((comparison$real_prop - comparison$sim_prop)^2))
  })
  return(mean(errors))
}

calc_un_error <- function(eps1, eps2, n, reps=50) {
  errors <- replicate(reps, {
    sim <- expand.grid(id = 1:n, trial.type = observed_uncertain_props$trial.type, rep = 1:4) %>%
      rowwise() %>%
      mutate(choice = uncertain_kid(trial.type, eps1, eps2)) %>% 
      group_by(trial.type) %>%
      summarize(sim_prop = mean(choice == "bag"), .groups = "drop")
    
    comparison <- left_join(observed_uncertain_props, sim, by = "trial.type")
    sqrt(mean((comparison$real_prop - comparison$sim_prop)^2))
  })
  return(mean(errors))
}

# finding best ev epsilon
ev_eps_grid <- data.frame(eps = seq(0.01, 0.4, by = 0.01))
best_ev_eps <- ev_eps_grid %>% 
  rowwise() %>% 
  mutate(err = calc_ev_error(eps, 4)) %>% 
  ungroup() %>% 
  filter(err == min(err)) %>% 
  slice(1)

# finding best uncertain epsilons
un_eps_grid <- data.frame(eps1 = seq(0.01, 0.4, by = 0.01), 
                          eps2 = seq(0.01, 0.4, by = 0.01))

best_un_eps <- un_eps_grid %>% 
  rowwise() %>% 
  mutate(err = calc_un_error(eps1, eps2, 2)) %>% 
  ungroup() %>% 
  filter(err == min(err)) %>% 
  slice(1)


prop_ev = 2/3
ev_eps = best_ev_eps$eps
un_eps1 = best_un_eps$eps1
un_eps2 = best_un_eps$eps2

print(calculate_sim_error(prop_ev, ev_eps, un_eps1, un_eps2))

#########
# finding the ideal. number of n
#########
sim_power <- function(n_kids, prop_ev, eps_ev, eps_un1, eps_un2) {
  # 3 trial types, 4 trials each, for N kids
  trials_per_type <- 4
  types <- c("inferred2cVsKnown1c", "unknown4cVsKnown1c", "unknown2cVsKnown1c")
  
  kid_strategies <- data.frame(
    id = 1:n_kids,
    strategy = sample(c("EV", "Uncertainty"), 
                      size = n_kids, 
                      replace = TRUE, 
                      prob = c(prop_ev, 1 - prop_ev))
  )
  kid_strategies
  
  fake_data <- expand.grid(id = 1:n_kids, 
                           trial.type = types, 
                           rep = 1:trials_per_type) %>%
    left_join(kid_strategies, by = "id") %>%
    rowwise() %>%
    mutate(choice = case_when(
      strategy == "EV" ~ ev_kid(trial.type, eps_ev),
      strategy == "Uncertainty" ~ uncertain_kid(trial.type, eps_un1, eps_un2)
    )) %>%
    ungroup() %>%
    mutate(choice = factor(choice, levels = c("bag", "chest")),
           trial.type = factor(trial.type))
  
  m <- try(glmer(choice ~ trial.type + (1|id), 
                 family = "binomial", 
                 data = fake_data),
           silent = TRUE)
  if(inherits(m, "try-error")) {return(NA)}
  
  # Extract p-value for the effect of trial.type
  # Using [1] assuming trial.type is the first/only fixed effect in the Anova table
  emm <- emmeans(m, specs = "trial.type")
  
  pairwise_tests <- contrast(emm, method = list(
    "inferred_vs_unknown2c" = c(1, -1, 0),
    "unknown2c_vs_unknown4c" = c(0, 1, -1),
    "duplication" = c(1, 0, -1)
  )) %>% as_tibble()
  
  # Check if both specific comparisons are p < .05
  # Or change to any(p.value < .05) depending on your thesis goals
  success <- all(pairwise_tests$p.value < .05)
  
  return(success)
}

grid <- data.frame(n = seq(10, 60, by = 5))
reps <- 100


parameters <- paste(
  "--- Simulation Parameters ---",
  paste0("prop_ev: ", prop_ev),
  paste0("ev_eps:  ", ev_eps),
  paste0("un_eps1: ", un_eps1),
  paste0("un_eps2: ", un_eps2),
  sep = "\n"
)

cat(parameters, "\n")

power_results <- grid %>%
  group_by(n) %>%
  mutate(power = mean(replicate(reps, sim_power(n, prop_ev, ev_eps, un_eps1, un_eps2)), na.rm = TRUE))


print(power_results)

