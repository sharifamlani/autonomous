# Build the answer key for benchmark task S1 (and the reference for S2).
#
# Source: Amlani & Collitt (2022), "The Impact of Vote-By-Mail Policy on Turnout and Vote Share in the
# 2020 Election", Election Law Journal, doi:10.1089/elj.2021.0015. Replication package (CC0):
# doi:10.7910/DVN/TKBWOC. The model formulas below are copied verbatim from the package's
# Table2_Figure3_Table3_Figure5.R (only the data path changes; no RStudio needed).
#
# Two versions of the fixed-effects models:
#   published : county fixed effects as in the package, as.factor(county_name)
#   fips      : county fixed effects by state_county_fips (what "county fixed effects" means in the text)
#
# Writes benchmark/keys/s1.json (local only) and compares the published version with the printed
# Tables 2-3 in benchmark/keys/s1_published.json at printed precision.
#
# Run from the repo root (Claude/cron-run, so headless; not the RStudio working-directory standard):
#   "C:/Program Files/R/R-4.5.0/bin/Rscript.exe" scripts/benchmark/build_key_s1.R

suppressPackageStartupMessages({
  library(sandwich)
  library(lmtest)
  library(jsonlite)
})

DATA <- "benchmark/keys/s1/vbm_data.rda"
URL  <- "https://dataverse.harvard.edu/api/access/datafile/5616208"
OUT  <- "benchmark/keys/s1.json"
REF  <- "benchmark/keys/s1_published.json"

if (!file.exists("ROADMAP.md")) stop("run from the repo root")
if (!file.exists(DATA)) {
  dir.create(dirname(DATA), recursive = TRUE, showWarnings = FALSE)
  download.file(URL, DATA, mode = "wb", quiet = TRUE)
}

load(DATA); VBM_Master.1 <- VBM_Master.Pure
VBM_Master.2 <- subset(VBM_Master.1, Percent_Turnout_VAP <= 100)

# ---- Turnout (Table 2), verbatim formulas ----
B_DID.Base <- lm(Percent_Turnout_VAP ~ Conditions_Detail*as.factor(year), data = VBM_Master.2)
B_DID.1 <- lm(Percent_Turnout_VAP ~ Conditions_Detail*as.factor(year) +
                prcntBlack +  democratic_percent  + medianIncome + medianAge + prcntHS + daily_change_deaths_1week_100K + Automatic_Voter_Registration_Change + battleground,
              data = VBM_Master.2)
B_DID.2 <- lm(Percent_Turnout_VAP ~ Conditions_Detail*as.factor(year) +
                prcntBlack +  democratic_percent  + medianIncome + medianAge + prcntHS + daily_change_deaths_1week_100K + Automatic_Voter_Registration_Change + battleground +
                as.factor(county_name), data = VBM_Master.2)
B_DID.3 <- coeftest(B_DID.2, vcovCL, cluster = VBM_Master.2$state.name)

# ---- Vote share (Table 3), verbatim formulas ----
Base.VS <- lm(republican_percent ~ Conditions_Detail*as.factor(year), data = VBM_Master.2)
B_DID.VS.1 <- lm(republican_percent ~ Conditions_Detail*as.factor(year) +
                   prcntHS + prcntBA + prcntBlack + prcntMulti + prcntHisp + prcntForeignBorn + medianIncome + pop_sq_mi + Unemployment_Rate + daily_change_deaths_1week_100K  + Automatic_Voter_Registration_Change + battleground,
                 data = VBM_Master.2)
B_DID.VS.2 <- lm(republican_percent ~ Conditions_Detail*as.factor(year) +
                   prcntHS + prcntBA + prcntBlack + prcntMulti + prcntHisp + prcntForeignBorn + medianIncome + pop_sq_mi +Unemployment_Rate +  daily_change_deaths_1week_100K + Automatic_Voter_Registration_Change  + battleground +
                   as.factor(county_name), data = VBM_Master.2)
B_DID.VS.3 <- coeftest(B_DID.VS.2, vcovCL, cluster = VBM_Master.2$state.name)

# ---- FIPS variant: the same models with county fixed effects by FIPS code ----
fips_fe <- function(m) update(m, . ~ . - as.factor(county_name) + as.factor(state_county_fips))
F_DID.2    <- fips_fe(B_DID.2)
F_DID.3    <- coeftest(F_DID.2, vcovCL, cluster = VBM_Master.2$state.name)
F_DID.VS.2 <- fips_fe(B_DID.VS.2)
F_DID.VS.3 <- coeftest(F_DID.VS.2, vcovCL, cluster = VBM_Master.2$state.name)

# ---- The other clustered-SE convention (decision 10-K, D29) ----
# vcovCL's default (HC1) counts every county dummy in the small-sample correction (N-1)/(N-K), which with
# 3,113 nested county FE multiplies each SE by about 1.42; p from t(N-K). The usual convention when the FE are
# nested in the clusters counts only the cluster adjustment G/(G-1) (HC0 here), with p from t(G-1). The
# paper says only "clustered by state", so S2 accepts the 5% call under either convention.
G_STATES <- length(unique(VBM_Master.2$state.name))
nested <- function(fit) coeftest(fit, vcov = vcovCL(fit, cluster = VBM_Master.2$state.name, type = "HC0"),
                                 df = G_STATES - 1)
F_DID.3n    <- nested(F_DID.2)
F_DID.VS.3n <- nested(F_DID.VS.2)

# ---- Collect the difference-in-differences terms ----
TERMS <- c(excuse_to_noexcuse_x2020  = "Conditions_DetailWith Excuse To No Excuse:as.factor(year)2020",
           excuse_to_apps_x2020      = "Conditions_DetailWith Excuse To Applications:as.factor(year)2020",
           noexcuse_to_apps_x2020    = "Conditions_DetailNo Excuse to Applications:as.factor(year)2020",
           noexcuse_to_ballots_x2020 = "Conditions_DetailNo Excuse to VBM Election:as.factor(year)2020",
           year2020                  = "as.factor(year)2020")

grab <- function(ct) {
  out <- list()
  for (k in names(TERMS)) {
    r <- TERMS[[k]]
    out[[k]] <- if (r %in% rownames(ct)) list(b = unname(ct[r, 1]), se = unname(ct[r, 2]), p = unname(ct[r, 4])) else NULL
  }
  out
}
model <- function(fit, ct = coef(summary(fit))) {
  s <- summary(fit)
  list(terms = grab(ct), n = length(fit$residuals), adj_r2 = unname(s$adj.r.squared),
       df_resid = fit$df.residual, n_coef = sum(!is.na(coef(fit))))
}

key <- list(
  source = "Amlani & Collitt 2022 replication package doi:10.7910/DVN/TKBWOC; formulas verbatim",
  r_version = R.version.string,
  fe_levels = list(county_name = length(unique(VBM_Master.2$county_name)),
                   state_county_fips = length(unique(VBM_Master.2$state_county_fips))),
  published = list(
    turnout = list(base = model(B_DID.Base), control = model(B_DID.1), county_fe = model(B_DID.2),
                   county_fe_state_cluster = model(B_DID.2, B_DID.3)),
    rep_share = list(base = model(Base.VS), control = model(B_DID.VS.1), county_fe = model(B_DID.VS.2),
                     county_fe_state_cluster = model(B_DID.VS.2, B_DID.VS.3))),
  fips = list(
    turnout = list(county_fe = model(F_DID.2), county_fe_state_cluster = model(F_DID.2, F_DID.3),
                   county_fe_state_cluster_nested = model(F_DID.2, F_DID.3n)),
    rep_share = list(county_fe = model(F_DID.VS.2), county_fe_state_cluster = model(F_DID.VS.2, F_DID.VS.3),
                     county_fe_state_cluster_nested = model(F_DID.VS.2, F_DID.VS.3n)))
)
write_json(key, OUT, auto_unbox = TRUE, digits = NA, pretty = TRUE)
cat("wrote", OUT, "\n")

# ---- Compare the published version with the printed tables ----
ref <- fromJSON(REF)
cols <- c("base", "control", "county_fe", "county_fe_state_cluster")
checked <- 0; bad <- character()
for (tab in c("turnout", "rep_share")) {
  rt <- if (tab == "turnout") ref$table2_turnout_did else ref$table3_rep_share_did
  for (k in setdiff(names(TERMS), if (tab == "rep_share") "year2020" else character())) {
    for (j in seq_along(cols)) {
      got <- key$published[[tab]][[cols[j]]]$terms[[k]]
      for (stat in c("b", "se")) {
        want <- rt[[k]][[stat]][j]
        checked <- checked + 1
        if (is.null(got) || round(got[[stat]], 3) != want)
          bad <- c(bad, sprintf("%s %s %s %s: printed %.3f, code %s", tab, cols[j], k, stat, want,
                                if (is.null(got)) "missing" else sprintf("%.3f", got[[stat]])))
      }
    }
  }
}
cat(sprintf("printed-table check: %d of %d values match at printed precision\n", checked - length(bad), checked))
if (length(bad)) cat(paste0("  MISMATCH ", bad, "\n"), sep = "")

# ---- The headline under both fixed-effects codings ----
h <- function(x) sprintf("%.3f (SE %.3f, p %.4f)", x$b, x$se, x$p)
cat("FE levels: county_name", key$fe_levels$county_name, "| state_county_fips", key$fe_levels$state_county_fips, "\n")
cat("ballots sent x 2020, turnout, state-clustered:\n")
cat("  published (county_name FE):", h(key$published$turnout$county_fe_state_cluster$terms$noexcuse_to_ballots_x2020), "\n")
cat("  FIPS county FE            :", h(key$fips$turnout$county_fe_state_cluster$terms$noexcuse_to_ballots_x2020), "\n")
quit(status = if (length(bad)) 1 else 0)
