import datetime as dt
import os
import shutil
import tempfile
import traceback
from datetime import datetime
from itertools import combinations

import bambi as bmb
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import joblib
import mogp 


import pymc as pm
import seaborn as sns
from markdown_pdf import MarkdownPdf, Section
from scipy.stats import gaussian_kde

from ._version import __version__ as VERSION

sns.set(style="darkgrid", palette="muted")
DAYS_PER_MONTH = 30.417
imgf = "png"
DPI = None
try:
    MOGP_PTH = os.environ['ALSTRACKER_MOGP']
except KeyError:
    raise Exception("Environment variable 'ALSTRACKER_MOGP' is not set. Stop.")
    


def get_prior(measurement_name, logger):
    priors = None

    if "Hand Grip" in measurement_name:
        # fit by pro-act (-3.485702181069315, 0.004060413119629223, 0.04268958889342467)
        slope_prior = bmb.Prior(
            'SkewNormal', alpha=-3.485, mu=0.00406, sigma=0.042689
        )
        sigma = bmb.Prior(
            'HalfStudentT',nu=4,sigma=1.5
        )

        priors = {
            "x": slope_prior,  # 'x' is the predictor variable (slope in y ~ x)
            "sigma": sigma
        }
        
    if "ALSFRS-R" in measurement_name:
        # Fitted parameters from pro-act (loss per day): (-5.462513259320875, -0.0025174662591182775, 0.0350512159471242)
        slope_prior = bmb.Prior(
            'SkewNormal', alpha=-5.46, mu=-0.00252, sigma=0.035
        )

        priors = {
            "x": slope_prior,  # 'x' is the predictor variable (slope in y ~ x)
        }
    if measurement_name == "Vital capacity":
        # Fitted parameters from pro-act (loss per day): (-3.4796549308580724, 0.005802679016612824, 0.11498742860055096)
        slope_prior = bmb.Prior(
            "SkewNormal", alpha=-3.479654, mu=0.0058026, sigma=0.1149874
        )

        priors = {
            "x": slope_prior,  # 'x' is the predictor variable (slope in y ~ x)
        }
    if measurement_name == "Neurofilament light chain":
        # https://pubmed.ncbi.nlm.nih.gov/37975796/
        # The individual median longitudinal NfL change was close to zero (+1.4 pg/mL),	 with	 80%	 of	 the	 individual	 deviation	 from	 BL	 values	 found	 in	 a	        # range	 between	 −17.6 pg/mL	 (10th	 percentile)	 and +22.1 pg/mL	(90th	percentile),	and	half	of	the	values	even	in	a	 narrow	range
        # between	−5.6 pg/mL	(25th	percentile)	and +14.2 pg/mL	 (75th	percentile).
        #
        # The individual median longitudinal NfL change was close to zero (+1.4 pg/mL). The IQR (from 25th to 75th percentile) is the range between −5.6 pg/mL and +14.2 pg/mL. 
        # With that constrains,  Preliz shows that a Normal distribution with a sigma of 15 is good fit.

        # Over all patients Median is 51.8. IQR is 35.5 to 85.9. With the constrains that 50% of the probability mass should be in the range of 35.5 and 85.9 and with a median of 51.8 Preliz shows that a Gamma distribution is good fit.
        priors = {
            "Intercept": bmb.Prior("Gamma", alpha=3.18, beta=0.0551),
            "sigma": bmb.Prior("HalfNormal", sigma=15),
        }

    if priors:
        logger.append(f"Set prior for {measurement_name}")

    return priors


# This code is adapted from https://www.quantstart.com/articles/Bayesian-Linear-Regression-Models-with-PyMC3/
def glm_mcmc_inference(df, iterations=10000, priors: dict = None, itype="S"):
    trace = None
    if itype == "S":
        # Create the glm using the Bambi model syntax
        model = bmb.Model("y ~ x", df, priors=priors)  # family="t",

    if itype == "L":
        with pm.Model() as model:
            dat = pd.DataFrame({"obs": df["y"]})
            model = bmb.Model("obs ~ 1", data=dat, priors=priors)
            
    print(model)
    # Fit the model
    trace = model.fit(
        draws=iterations,
        tune=1000,
        discard_tuned_samples=True,
        chains=4,
        cores=4,
        progressbar=True,
        target_accept=0.9,
    )

    return trace


def make_alldata_regr(all_data, ax1):
    dbentry = all_data
    valuename = dbentry["meta"]["Value"]

    trace, dbdata = dbentry["trace"]["All data"]

    ax1.scatter(dbdata["Date"], dbdata[valuename], color="black")

    # extract slope and intercept draws from PyMC trace
    intercepts = trace.posterior.Intercept.to_numpy()[0]
    slopes = trace.posterior.x.to_numpy()[0]
    dbentry["posterior"] = slopes
    # plot 100 random samples from the slope and intercept draws
    sample_indexes = np.random.randint(len(intercepts), size=100)

    for i in sample_indexes:
        y_line = intercepts[i] + slopes[i] * dbdata["DateNum"]
        ax1.plot(dbdata["Date"], y_line, color="grey", alpha=0.07)


def make_alsfrs_prediction(data, logger, plot_dir):
    logger.append(
                        f"Predict ALSFRS-Score progression"
                    )
    path_to_reference = Path(MOGP_PTH)
    reference_model = joblib.load(path_to_reference)

    df = data['ALSFRS-R Score'][0]['data']
    
    # Filter rows where 'Y_Since_Onset' is greater than 0
    filtered_df = df[df['Y_Since_Onset'] > 0]
    
    # Extract the relevant columns and convert them to numpy arrays
    Xi_new = filtered_df['Y_Since_Onset'].values
    Yi_new = filtered_df['Score'].values

    cluster_list, cluster_ll = mogp.utils.rank_cluster_prediction(reference_model, Xi_new, Yi_new)

    cl=[0,1,2]
    col=['#fc8d62','#66c2a5','#8da0cb']

    fig, ax = plt.subplots(figsize=(8,5))

    # Plot GP model for selected cluster
    alpha=0.2
    alphal=1
    
    for ci, c in enumerate(cl):
        cur_ll = cluster_ll[c]
        if ci > 0:
            alpha=0.1
            alphal=0.5
        _ = reference_model.obsmodel[cluster_list[c]].model.plot_confidence(ax=ax, label=None, color=col[ci],alpha=alpha)
        _ = reference_model.obsmodel[cluster_list[c]].model.plot_mean(ax=ax, label=f'Progression prediction ({cur_ll*100:.0f}%)', color=col[ci], alpha=alphal)
    
    # Plot input new data
    _ = ax.plot(Xi_new, Yi_new, 'o',  markerfacecolor='none' ,color='black', label='Input Data')
    
    # Format plot
    _ = ax.set_xlim(0)
    _ = ax.set_ylim(0,50)
    _ = ax.set_xlabel("Years since onset")
    _ = ax.set_ylabel("ALSFRS-R Score")
    _ = ax.set_title("Progression prediction for the 3 most likely scenarios")
    _ = ax.legend()
    today = datetime.now()

    fpth = os.path.join(
                    plot_dir,
                    today.strftime("%Y%m%d"),
                    f"alsfrs_prediction.{imgf}",
                )
    fpth = fpth.replace(" ", "")
    fig.savefig(fpth, dpi=DPI)
    return fpth
    
def make_alldata_lvl(data, ax1):
    dbentry = data
    valuename = dbentry["meta"]["Value"]

    # Phase bars and scatter plot with regression lines

    trace, dbdata = dbentry["trace"]["All data"]

    ax1.scatter(dbdata["Date"], dbdata[valuename], color="black")

    posterior_samples = trace.posterior.Intercept.to_numpy()[0]

    # Calculate the mean and the 95% credible interval
    mean_mu = np.mean(posterior_samples)
    ci_95 = np.percentile(posterior_samples, [2.5, 97.5])
    ci_low = ci_95[0]
    ci_high = ci_95[1]

    # Prepare data for the plot
    # x = np.linspace(dbdata['DateNum'], lastx+len(pdata), 100)
    mean_line = np.full_like(dbdata[valuename], mean_mu)
    lower_bound = np.full_like(dbdata[valuename], ci_low)
    upper_bound = np.full_like(dbdata[valuename], ci_high)

    ax1.plot(dbdata["Date"], mean_line, label="Mean of μ", color="grey")
    ax1.text(0.8, 0.94, 'The transparent areas show the 95% CI.',
             horizontalalignment='center',
             verticalalignment='center',
             transform=ax1.transAxes)
    ax1.fill_between(
        dbdata["Date"],
        lower_bound,
        upper_bound,
        color="grey",
        alpha=0.2,
        label="95% CI",
    )


def get_phase_colormap(database):
    phs = [p[0] for p in database["Phases"]]
    cmap = plt.get_cmap("Dark2")
    color_dict = {
        phase: cmap(i / float(len(phs))) for i, phase in enumerate(phs)
    }
    color_dict["All data"] = "grey"
    return color_dict


def make_phase_plots(database, plot_dir, logger):
    if plot_dir:
        today = datetime.now()
        os.makedirs(os.path.join(plot_dir, today.strftime("%Y%m%d")), exist_ok=True)

    figures = {}
    phases_data = database["Phases"]
    phases = {}

    for phs in phases_data:
        phs_start = phs[1]
        phs_end = phs[2]
        phases[phs[0]] = {"start": phs_start, "end": phs_end}

    color_dict = get_phase_colormap(database)

    for measurement_name in database:
        if measurement_name == "Phases":
            continue
        entries_for_measurement = database[measurement_name]
        for dbentry in entries_for_measurement:
            # dbdata = dbentry['data']
            valuename = dbentry["meta"]["Value"]
            unit = dbentry["meta"]["Unit"]

            itype = dbentry["meta"]["Type"]

            title_suffix = "Trends"
            if itype == "L":
                title_suffix = "Levels"

            value_str = ""
            if len(entries_for_measurement) > 1:
                value_str = f" ({valuename})"

            # Create the figure and subplots
            fig, (ax1, ax2, ax3) = plt.subplots(
                3,
                1,
                sharex=True,
                figsize=(10, 8),
                gridspec_kw={"height_ratios": [4, 4, 1]},
            )

            # Phase bars and scatter plot with regression lines
            # color_dict = {phase: plt.cm.pastel2(i/float(len(phases))) for i, phase in enumerate(phases)}

            # Track occupied y-levels
            used_levels = []
            pmin = None
            pmax = None
            for phase in dbentry["trace"]:

                if phase == "All data":
                    if itype == "S":
                        make_alldata_regr(dbentry, ax1)

                    elif itype == "L":
                        make_alldata_lvl(dbentry, ax1)
                    continue

                trace, dbdata = dbentry["trace"][phase]

                pStartEnd = phases[phase]
                if pmin is None:
                    pmin = pStartEnd["start"]

                if pStartEnd["start"] < pmin:
                    pmin = pStartEnd["start"]

                if pmax is None:
                    pmax = pStartEnd["end"]

                if pStartEnd["end"] > pmax:
                    pmax = pStartEnd["end"]

                if itype == "S":

                    # Scatter plot points for the phase
                    ax2.scatter(dbdata["Date"], dbdata[valuename], color="black")

                    # Regression line for the phase

                    # extract slope and intercept draws from PyMC trace
                    intercepts = trace.posterior.Intercept.to_numpy()[0]
                    slopes = trace.posterior.x.to_numpy()[0]
                    dbentry["posterior"] = slopes
                    # plot 100 random samples from the slope and intercept draws
                    sample_indexes = np.random.randint(len(intercepts), size=100)

                    for i in sample_indexes:
                        y_line = intercepts[i] + slopes[i] * dbdata["DateNum"]
                        ax2.plot(
                            dbdata["Date"], y_line, color=color_dict[phase], alpha=0.07
                        )

                elif itype == "L":
                    make_alldata_lvl(measurement_name, dbentry, ax1)

                    ax2.scatter(dbdata["Date"], dbdata[valuename], color="black")
                    posterior_samples = trace.posterior.Intercept.to_numpy()[0]

                    # Calculate the mean and the 95% credible interval
                    mean_mu = np.mean(posterior_samples)
                    ci_95 = np.percentile(posterior_samples, [2.5, 97.5])
                    ci_low = ci_95[0]
                    ci_high = ci_95[1]

                    # Prepare data for the plot
                    # x = np.linspace(dbdata['DateNum'], lastx+len(pdata), 100)
                    mean_line = np.full_like(dbdata[valuename], mean_mu)
                    lower_bound = np.full_like(dbdata[valuename], ci_low)
                    upper_bound = np.full_like(dbdata[valuename], ci_high)

                    ax2.plot(
                        dbdata["Date"],
                        mean_line,
                        label="Mean of μ",
                        color=color_dict[phase],
                    )
                    ax2.fill_between(
                        dbdata["Date"],
                        lower_bound,
                        upper_bound,
                        color=color_dict[phase],
                        alpha=0.3,
                        label="95% CI",
                    )

                # Find a y-level that isn't used
                level = 0
                while level in used_levels:
                    level += 1
                used_levels.append(level)
                # Bar for the phase
                ax3.barh(
                    level,

                    (pStartEnd["end"] - pStartEnd["start"]).days,
                    left=mdates.date2num(pStartEnd["start"]),
                    color=color_dict[phase],
                    align="center",
                    height=0.8,
                )

                # Add phase names below the bars
                pendtext = min(max(dbdata["Date"]), pStartEnd["end"])
                pstarttext = max(min(dbdata["Date"]), pStartEnd["start"])
                ax3.text(
                    pstarttext + (pendtext - pstarttext) / 2,
                    level,
                    phase,
                    ha="center",
                    va="center",
                    fontsize=10,
                    color="white",
                )

            # Determine padding for the x-axis
            x_padding = int(
                (
                        max(dbentry["trace"]["All data"][1]["Date"])
                        - min(dbentry["trace"]["All data"][1]["Date"])
                ).days
                * 0.05
            )
            x_padding = pd.Timedelta(days=max(1, x_padding))
            x_min = min(dbentry["trace"]["All data"][1]["Date"]) - x_padding
            x_max = max(dbentry["trace"]["All data"][1]["Date"]) + x_padding

            # Set x-axis limits
            ax2.set_xlim(x_min, x_max)

            # Formatting the date labels
            ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            fig.autofmt_xdate()

            # Set y-limits according to number of levels
            ax3.set_ylim(-0.5, len(used_levels) - 0.5)
            ax3.set_yticks([])
            ax3.set_ylabel("Phases")

            ax1.set_title(
                f"{measurement_name}{value_str} Over Time with Predicted {title_suffix}",
                fontsize=14,
            )
            ax3.set_xlabel("Measurement Date")
            ax2.set_ylabel(f"{measurement_name} [{unit}]")
            ax1.set_ylabel(f"{measurement_name} [{unit}]")

            text_position_x = 1.02  # Position just outside the right edge of the axes
            text_position_y = 0.5  # Midway up the y-axis in axis coordinates
            ax1.text(
                text_position_x,
                text_position_y,
                "All data",
                transform=ax1.transAxes,
                fontsize=14,
                verticalalignment="center",
                rotation=90,
            )
            ax2.text(
                text_position_x,
                text_position_y,
                "Phases",
                transform=ax2.transAxes,
                fontsize=14,
                verticalalignment="center",
                rotation=90,
            )

            fig.tight_layout()
            if plot_dir:
                fpth = os.path.join(
                    plot_dir,
                    today.strftime("%Y%m%d"),
                    f"{measurement_name}_trends.{imgf}",
                )
                fpth = fpth.replace(" ", "")
                fig.savefig(fpth, dpi=DPI)
                figures[measurement_name] = fpth
            fig.show()
    return figures


def make_regressions2(database, plot_dir=None):
    if plot_dir:
        today = datetime.now()
        os.makedirs(os.path.join(plot_dir, today.strftime("%Y%m%d")), exist_ok=True)

    figures = {}
    color_dict = get_phase_colormap(database)

    for measurement_name in database:
        if measurement_name == "Phases":
            continue
        entries_for_measurement = database[measurement_name]
        num_phases = sum(len(dbentry["trace"]) for dbentry in entries_for_measurement)
        num_columns = 2
        num_rows = (
                           num_phases + num_columns - 1
                   ) // num_columns  # Calculate the number of rows needed for 2 columns

        fig, axes = plt.subplots(num_rows, num_columns, figsize=(10, num_rows * 5))
        axes = axes.flatten()  # Flatten to easily index

        plot_index = 0
        minx = np.Inf
        maxx = -np.Inf
        bins = 50
        bw = None
        for dbentry in entries_for_measurement:
            valuename = dbentry["meta"]["Value"]
            if len(entries_for_measurement) > 1:
                f" ({valuename})"

            itype = dbentry["meta"]["Type"]

            if itype == "S":
                fig.suptitle(
                    f"Probability of Rate of Change in {measurement_name} per Month",
                    fontsize=14,
                    y=0.93,
                )
                xlabel = "Rate of Change"
                tunit = " / month"
            elif itype == "L":
                fig.suptitle(
                    f"Probability of {measurement_name} Level", fontsize=14, y=0.93
                )
                xlabel = "Level"
                tunit = ""

            for i, phase in enumerate(dbentry["trace"]):
                trace, dbdata = dbentry["trace"][phase]
                unit = dbentry["meta"]["Unit"]
                ax = axes[plot_index]

                if itype == "S":
                    post_month = trace.posterior.x.to_numpy()[0] * DAYS_PER_MONTH
                elif itype == "L":
                    post_month = trace.posterior.Intercept.to_numpy()[0]

                minx = min(minx, np.percentile(post_month, 1))
                maxx = max(maxx, np.percentile(post_month, 99))

                np.mean(post_month)
                mode_slope = get_mode(post_month)
                ci_95 = np.percentile(post_month, [2.5, 97.5])
                ci_txt = (
                    f"{mode_slope:.2f} {unit}{tunit}\n"
                    f"95% CI [{ci_95[0]:.2f} {unit}, {ci_95[1]:.2f} {unit}]{tunit}"
                ).center(50)

                if bw:
                    bins = np.arange(min(post_month), max(post_month) + bw, bw)

                (n, bins, patches) = ax.hist(
                    post_month,
                    bins=bins,
                    density=True,
                    color=color_dict[phase],
                    linewidth=0.3,
                )

                if phase == "All data":
                    bw = np.abs(bins[-2] - bins[-3])
                ax.set_title(f"{phase}", fontsize=12)
                ax.set_ylabel("Probability")
                ax.set_xlabel(f"""{xlabel} ({unit}{tunit})\n\n{ci_txt}""")

                plot_index += 1
        for ax in axes:
            ax.set_xlim(minx, maxx)

        fig.tight_layout(
            rect=[0, 0.03, 1, 0.95]
        )  # Adjust layout to accommodate the suptitle

        # Hide any remaining unused subplots
        if num_phases < len(axes):
            for j in range(num_phases, len(axes)):
                fig.delaxes(axes[j])

        if plot_dir:
            fpth = os.path.join(
                plot_dir, today.strftime("%Y%m%d"), f"{measurement_name}_probs.{imgf}"
            )
            fpth = fpth.replace(" ", "")
            fig.savefig(fpth, dpi=DPI)
            figures[measurement_name] = fpth

        fig.show()

    return figures


def add_traces_to_db(database, logger):
    phases = database["Phases"]
    for measurement_name in database:
        if measurement_name == "Phases":
            continue
        entries_for_measurement = database[measurement_name]

        for dbentry in entries_for_measurement:

            dbdata = dbentry["data"]

            if len(dbdata) < 2:
                continue
            valuename = dbentry["meta"]["Value"]
            itype = dbentry["meta"]["Type"]
            dbentry["trace"] = {}
            for phs in phases:
                phs_name = phs[0]
                phs_start = phs[1]
                phs_end = phs[2]
                mask = np.ones(dbdata.shape[0], dtype=bool)
                if phs_start:
                    mask = mask & (dbdata["Date"] >= phs_start)
                if phs_end:
                    mask = mask & (dbdata["Date"] <= phs_end)

                dfmasked = dbdata.loc[mask]
                dfmasked["DateNum"] = dfmasked["DateNum"] - dfmasked["DateNum"].mean()
                if len(dfmasked) < 2:
                    logger.append(
                        f"Not enough data to fit {measurement_name} ({valuename}, n={len(dfmasked['DateNum'])}) for phase '{phs_name}'"
                    )
                    continue
                logger.append(
                    f"Fit {measurement_name} ({valuename}, n={len(dfmasked['DateNum'])}) for phase '{phs_name}'"
                )
                priors = get_prior(measurement_name, logger)

                fitdf = pd.DataFrame(
                    {
                        "x": dfmasked["DateNum"].to_list(),
                        "y": dfmasked[valuename].to_list(),
                    }
                )

                trace = glm_mcmc_inference(fitdf, priors=priors, itype=itype)
                dbentry["trace"][phs_name] = (trace, dfmasked)


def read_database(db_pth, logger):
    data = {}
    database = pd.read_excel(db_pth, sheet_name=None)
    min_date = datetime.max
    max_date = datetime.min
    # Check if database is valid
    if "Meta" not in database:
        raise Exception("No 'Meta' Sheet found in database")

    if "Other" not in database:
        raise Exception("No 'Other' Sheet found in database. This is required as it contains the disease onset.")

    onset=None
    for _,r in database['Other'].iterrows():
        if r['Name'] == 'Onset':
            onset = pd.to_datetime(r['Value'], format="%d.%m.%Y")
            
    if onset is None:
        raise Exception("Can't find 'Onset' date in sheet 'Other'")

    for rowindex, row in database["Meta"].iterrows():
        sheetname = row["Sheet"]
        if sheetname not in database:
            raise Exception(f"Measurement sheet {sheetname} can't be found")

        df = database[sheetname]

        if row["Value"] not in df:
            raise Exception(
                f"Value column '{row['Value']}' does not exist in sheet '{sheetname}'"
            )

        if "DateNum" not in df:
            df = df.dropna()

            # Convert the 'Date' column to datetime format
            df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")

            if max(df["Date"]) > max_date:
                max_date = max(df["Date"])
            if min(df["Date"]) < min_date:
                min_date = min(df["Date"])

            # Required to do regression
            df["DateNum"] = df["Date"].map(dt.datetime.toordinal)
            
        if "Y_Since_Onset" not in df:
            df = df.dropna()
            yso = []
            for di, d in enumerate(df['Date']):
                yso.append((d-onset).days/365)
            df["Y_Since_Onset"] = yso
            
        try:
            row["Type"]
        except:
            logger.append(
                f"Cant find 'Type' for '{sheetname}' in Meta. Assume type 'S'"
            )
            row["Type"] = "S"
        if len(df) < 2:
            continue
        dat = data.get(sheetname, [])
        dat.append({"meta": row, "data": df})
        data[sheetname] = dat

    data["Phases"] = [("All data", None, None)]
    if "Phases" in database:
        phases = database["Phases"]
        phases["Start"] = pd.to_datetime(phases["Start"], format="%d.%m.%Y")
        phases["End"] = pd.to_datetime(phases["End"], format="%d.%m.%Y")

        for _, row in database["Phases"].iterrows():
            start = row["Start"]
            if pd.isnull(start):
                start = min_date

            end = row["End"]
            if pd.isnull(end):
                end = max_date

            data["Phases"].append((row["Phasename"], start, end))

    return data


def get_mode(samples):
    # Assuming trace is the trace object returned by model.fit
    # Flatten the trace and convert it to an array for a specific parameter, e.g., trace[some_param]
    param_samples = samples  # trace.posterior['x'].values.flatten()

    # Use KDE to estimate the density
    kde = gaussian_kde(param_samples)
    x = np.linspace(min(param_samples), max(param_samples), 1000)
    kde_values = kde(x)
    mode_estimate = x[np.argmax(kde_values)]
    return mode_estimate

def is_phase_exist(measurement_data, phase):
    return phase in measurement_data[0]["trace"]

def compare_intervention(database, measurement, reference_phase, intervention_phase):
    itype = database[measurement][0]["meta"]["Type"]

    if itype == "S":
        pre_intervention_posterior = database[measurement][0]["trace"][reference_phase][
            0
        ].posterior.x.to_numpy()[0]
        post_intervention_posterior = database[measurement][0]["trace"][
            intervention_phase
        ][0].posterior.x.to_numpy()[0]
    elif itype == "L":
        pre_intervention_posterior = database[measurement][0]["trace"][reference_phase][
            0
        ].posterior.Intercept.to_numpy()[0]
        post_intervention_posterior = database[measurement][0]["trace"][
            intervention_phase
        ][0].posterior.Intercept.to_numpy()[0]

    diff = (
                   pre_intervention_posterior - post_intervention_posterior
           ) / pre_intervention_posterior
    prob_improvement = np.sum(diff > 0) / len(diff) * 100
    diff = diff * 100
    diff = np.clip(diff, -500, +500)

    mode_estimate = get_mode(diff)
    np.mean(diff)
    ci_95 = np.percentile(diff, [2.5, 97.5])
    ci_txt = f"{mode_estimate:.2f} % (95% CI [{ci_95[0]:.2f} %, {ci_95[1]:.2f} %]) "

    return diff, ci_txt, prob_improvement


def make_intervention_plots(database, plot_dir):
    phases = [p[0] for p in database["Phases"]]
    cpairs = list(combinations(phases, 2))

    num_meas = len(database) - 1  # Excluding 'Phases' from measurements

    figures = {}

    for measurement_name in database:
        if measurement_name == "Phases":
            continue

        itype = database[measurement_name][0]["meta"]["Type"]
        pairs = []
        for p1,p2 in cpairs:
            if is_phase_exist(database[measurement_name],p1) and is_phase_exist(database[measurement_name],p2):
                pairs.append((p1,p2))

        # Calculate the number of rows needed for the subplots
        num_pairs = len(pairs)
        if num_pairs == 0:
            continue
        num_cols = 2
        num_rows = (num_pairs + 1) // num_cols  # Ceiling division for rows required

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, num_rows * 5))
        axes = axes.flatten()  # Flatten in case of single row

        for idx, (p1, p2) in enumerate(pairs):
            diff, ci_txt, prob_improvement = compare_intervention(
                database=database,
                measurement=measurement_name,
                reference_phase=p1,
                intervention_phase=p2,
            )
            ax = axes[idx]
            ax.hist(
                diff,
                bins=range(int(min(diff)), int(max(diff)) + 2, 2),
                density=True,
                linewidth=0.3,
                color='grey'
            )

            ax.set_title(f"'{p1}' vs '{p2}'")
            ax.set_xlim(-100, 100)
            ax.set_ylabel("Probability")
            if itype == "S":
                ax.set_xlabel(
                    f"""Relative Change in {measurement_name} Rate [%]

                {ci_txt}

                Probability that Rate of Change 
                '{p2}' < '{p1}': {prob_improvement:.2f}%
                '{p2}' > '{p1}': {(100 - prob_improvement):.2f}%


                """.center(
                        75
                    )
                )
            elif itype == "L":
                ax.set_xlabel(
                    f"""Relative Change in {measurement_name} Level [%]

                {ci_txt}

                Probability that Level 
                '{p2}' < '{p1}': {prob_improvement:.2f}%
                '{p2}' > '{p1}': {(100 - prob_improvement):.2f}%


                """.center(
                        75
                    )
                )

        # Hide any remaining unused subplots
        if num_pairs < len(axes):
            for j in range(num_pairs, len(axes)):
                fig.delaxes(axes[j])

        fig.suptitle(f"Comparisons for {measurement_name}", fontsize=14)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        if plot_dir:
            today = datetime.now()
            fpth = os.path.join(
                plot_dir,
                today.strftime("%Y%m%d"),
                f"{measurement_name}_comparisions.{imgf}",
            ).replace(" ", "")
            fig.savefig(fpth, dpi=DPI)
            figures[measurement_name] = fpth
        fig.show()
    return figures


def make_doc(pth, lines, slopes, comparisions={}, types={}, logger=None, **kwargs):
    pdf = MarkdownPdf(toc_level=2)

    pdf.add_section(
        Section(
            f"""# ALSTracker Report
    https://alstracker.mpi-dortmund.mpg.de\n\n

    Date: {datetime.today().strftime('%d.%m.%Y')}
    ALSTracker Version: {VERSION} \n
    """,
            toc=False,
        )
    )

    for measurement in lines:
        if types[measurement] == "S":
            pdf.add_section(
                Section(
                    f"""## {measurement}\n\n ### Trends \n\n ![]({lines[measurement]})
            """,
                    toc=False,
                )
            )

            pdf.add_section(
                Section(
                    f"### Estimated Rate during Phases \n\n ![]({slopes[measurement]})\n"
                )
            )

            if measurement == "ALSFRS-R Score":
                pdf.add_section(
                Section(
                    f"### Progression prediction \n\n ![]({kwargs['alsfrs_prediction']})\n"
                )
            )

        if types[measurement] == "L":
            pdf.add_section(
                Section(
                    f"""## {measurement}\n\n ### Levels \n\n ![]({lines[measurement]})
            """,
                    toc=False,
                )
            )

            pdf.add_section(
                Section(
                    f"### Estimated Level during Phases \n\n ![]({slopes[measurement]})\n"
                )
            )

        if measurement in comparisions:
            pdf.add_section(
                Section(
                    f"### Relative Change during Phases ![]({comparisions[measurement]})\n"
                )
            )

    if logger is not None:
        pdf.add_section(
            Section(
                f"## Creation Log\n\n ```\n{logger.log_str()}\n```",
                toc=False,
            )
        )

    pdf.save(pth)


class MyLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.cur_log = []

    def append(self, text):
        print("Logger:", repr(text))
        with self.log_file.open(mode="a") as log:
            log.write(text)
            self.cur_log.append(text)
            if (text and text[-1] != "\n") or not text:
                log.write("\n")
                self.cur_log.append("\n")

    def log_str(self):
        return "".join(self.cur_log)


def run(input_file, pdf_file, log_file):
    logger = MyLogger(log_file)
    try:
        with tempfile.TemporaryDirectory(dir=input_file.parent, delete=True) as outdir:
            plot_dir = os.path.relpath(outdir, os.getcwd())
            logger.append("# 1/6 Read input file")
            database = read_database(input_file, logger)

            logger.append("# 2/6 Estimate posterior")
            add_traces_to_db(database, logger)

            logger.append("# 3/6 Make regression figures")
            line_figures = make_phase_plots(database, plot_dir, logger)
            
            alsfrs_prediction = make_alsfrs_prediction(database, logger, plot_dir)

            logger.append("# 4/6 Make slope distribution figures")
            slope_figures = make_regressions2(database, plot_dir)

            logger.append("# 5/6 Make phase comparison figures")
            try:
                compare_figures = make_intervention_plots(database, plot_dir)
            except Exception:
                compare_figures = {}

            logger.append("# 6/6 Make pdf report")
            pdf_report = os.path.join(plot_dir, "report.pdf")

            types = {}
            for measurement_name in database:
                if measurement_name == "Phases":
                    continue
                itype = database[measurement_name][0]["meta"]["Type"]
                types[measurement_name] = itype
            make_doc(
                pdf_report, line_figures, slope_figures, compare_figures, types, logger, alsfrs_prediction=alsfrs_prediction
            )

            logger.append("# Copy pdf to final location")
            shutil.copy2(pdf_report, pdf_file)
    except Exception as exc:
        tb_str = "".join(traceback.format_exception(exc))
        logger.append(tb_str)
        logger.append(
            "\n\nPlease contact the authors if you made sure you provided valid data!"
        )
