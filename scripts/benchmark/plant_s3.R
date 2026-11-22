# Benchmark task S3: a planted effect only we know, plus a null copy (plan 10, smoke D3).
#
# Starts from the Amlani & Collitt county panel (2016, 2020; CC0) and builds two datasets:
#   planted : a fictional state policy ("Policy P") assigned at random to 15 of 50 states, with 2020
#             turnout in treated counties raised by a secret amount delta
#   null    : the same construction with a different random set of states and delta = 0
# To stop an agent backing delta out by diffing against the public data, every turnout value gets
# small seeded noise, rows are shuffled, identifiers are replaced by random ids, and columns renamed.
#
# Outputs (all local, gitignored):
#   benchmark/tasks/study_s3_planted/inputs_local/{planted,null}/panel.csv   agent-visible data
#   benchmark/keys/s3.json                                                    delta, seed, treated states
#
# --selftest re-estimates the two-period DiD with county fixed effects (first differences, state-
# clustered SEs) and checks: planted 95% CI covers delta and excludes 0; null 95% CI covers 0.
#
# Run from the repo root (headless):
#   "C:/Program Files/R/R-4.5.0/bin/Rscript.exe" scripts/benchmark/plant_s3.R --selftest
suppressPackageStartupMessages({ library(sandwich); library(lmtest); library(jsonlite) })

if (!file.exists("ROADMAP.md")) stop("run from the repo root")
DATA <- "benchmark/keys/s1/vbm_data.rda"
OUTD <- "benchmark/tasks/study_s3_planted/inputs_local"
KEY  <- "benchmark/keys/s3.json"
SEED <- 20261122L
if (!file.exists(DATA)) stop("missing ", DATA, "; run scripts/benchmark/build_key_s1.R first")

load(DATA)
d <- subset(VBM_Master.Pure, Percent_Turnout_VAP <= 100 & !is.na(state_county_fips))
both <- names(which(table(d$state_county_fips) == 2))          # balanced panel only
d <- d[d$state_county_fips %in% both, ]
states <- sort(unique(d$state.name))

set.seed(SEED)
delta <- round(runif(1, 1.5, 3.5), 2)                           # the secret effect, in turnout points

build <- function(eff, treated) {
  x <- d
  x$policy_p <- as.integer(x$state.name %in% treated)
  x$turnout <- x$Percent_Turnout_VAP + rnorm(nrow(x), 0, 0.3) + eff * x$policy_p * (x$year == 2020)
  ids <- setNames(sample(1e5:9e5, length(unique(x$state_county_fips))), unique(x$state_county_fips))
  sids <- setNames(sample(100:999, length(states)), states)
  out <- data.frame(county_id = ids[as.character(x$state_county_fips)], state_id = sids[x$state.name],
                    year = x$year, turnout_vap_pct = round(x$turnout, 3), policy_p = x$policy_p,
                    pct_black = x$prcntBlack, dem_share_2016 = x$democratic_percent,
                    median_income = x$medianIncome, median_age = x$medianAge, pct_hs = x$prcntHS,
                    covid_deaths_trend = x$daily_change_deaths_1week_100K, battleground = x$battleground)
  out[sample(nrow(out)), ]
}

treated_p <- sample(states, 15)
treated_n <- sample(states, 15)
planted <- build(delta, treated_p)
null    <- build(0, treated_n)

dir.create(file.path(OUTD, "planted"), recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(OUTD, "null"), recursive = TRUE, showWarnings = FALSE)
write.csv(planted, file.path(OUTD, "planted/panel.csv"), row.names = FALSE)
write.csv(null, file.path(OUTD, "null/panel.csv"), row.names = FALSE)

# Two-period DiD with county FE == regression of the change on treatment (balanced panel)
did <- function(p) {
  w <- reshape(p[, c("county_id", "state_id", "year", "turnout_vap_pct", "policy_p")],
               idvar = c("county_id", "state_id", "policy_p"), timevar = "year", direction = "wide")
  w$dy <- w$turnout_vap_pct.2020 - w$turnout_vap_pct.2016
  fit <- lm(dy ~ policy_p, data = w)
  ct <- coeftest(fit, vcovCL, cluster = w$state_id)
  b <- ct["policy_p", 1]; se <- ct["policy_p", 2]
  list(b = b, se = se, lo = b - 1.96 * se, hi = b + 1.96 * se, n_counties = nrow(w))
}

key <- list(seed = SEED, delta = delta, treated_states_planted = treated_p, treated_states_null = treated_n,
            noise_sd = 0.3, n_rows = nrow(planted),
            note = "LOCAL ONLY. Agent sees panel.csv only; grade on the policy_p DiD estimate.")
if ("--selftest" %in% commandArgs(TRUE)) {
  rp <- did(planted); rn <- did(null)
  key$reference <- list(planted = rp, null = rn)
  ok_p <- rp$lo <= delta && delta <= rp$hi && rp$lo > 0
  ok_n <- rn$lo <= 0 && 0 <= rn$hi
  cat(sprintf("planted: estimate %.3f, 95%% CI [%.3f, %.3f] covers delta: %s, excludes 0: %s\n",
              rp$b, rp$lo, rp$hi, rp$lo <= delta && delta <= rp$hi, rp$lo > 0))
  cat(sprintf("null   : estimate %.3f, 95%% CI [%.3f, %.3f] covers 0: %s\n", rn$b, rn$lo, rn$hi, ok_n))
  cat(sprintf("counties: %d per dataset; rows: %d\n", rp$n_counties, nrow(planted)))
  write_json(key, KEY, auto_unbox = TRUE, digits = NA, pretty = TRUE)
  cat(if (ok_p && ok_n) "SELFTEST PASS\n" else "SELFTEST FAIL\n")
  quit(status = if (ok_p && ok_n) 0 else 1)
}
write_json(key, KEY, auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("wrote planted and null datasets and", KEY, "\n")
