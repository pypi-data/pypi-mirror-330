# ALSTracker Technical Background

This page is intendet for a readership with a technical background.

## Priors

### ALSFRS-R Score

The priors for the ALSFRS-R I take from the pro-act [1] database. If you fit a skewed normal distribution to the measured progression rates you get the following fit:

![](img/prior_alsfrs.png)

This distribution is used as prior distribution in ALSTracker.

Here is the definition with [bambi](https://bambinos.github.io/bambi/):

```python
slope_prior = bmb.Prior(
    'SkewNormal', 
    alpha=-5.46, 
    mu=-0.00252, 
    sigma=0.035
)

```


### Vital Capacity

Same analysis as for the ALSFRS-R score I did for the slopes of forced vital capacity:

![](img/prior_vc.png)

I use the same distribution as prior for the slope.

Here is the definition with [bambi](https://bambinos.github.io/bambi/):

```python
slope_prior = bmb.Prior(
    "SkewNormal", 
    alpha=-3.479654, 
    mu=0.0058026, 
    sigma=0.1149874
)
```

### Grip strength

Same analysis as for the ALSFRS-R score I did for the slopes of hand grip:

![](img/prior_grip.png)

I use the same distribution as prior for the slope.

The measurement error `sigma` I modeled weakly-informative with HalfStudenT-distribution:

![](img/prior_grip_sigma.png)

Here is the definition with [bambi](https://bambinos.github.io/bambi/):

```python
slope_prior = bmb.Prior(
    'SkewNormal', 
    alpha=-3.485, 
    mu=0.00406, sigma=0.042689
)
sigma = bmb.Prior(
    'HalfStudentT',
    nu=4,
    sigma=1.5
)

```


### Neurofilament light chain

In Witzel et al [2] there is written:

> The individual median longitudinal NfL change was close to zero (+1.4 pg/mL),	 with	 80%	 of	 the	 individual	 deviation	 from	 BL	 values	 found	 in	 a	        # range	 between	 −17.6 pg/mL	 (10th	 percentile)	 and +22.1 pg/mL	(90th	percentile),	and	half	of	the	values	even	in	a	 narrow	range between	−5.6 pg/mL	(25th	percentile)	and +14.2 pg/mL	 (75th	percentile).

The individual median longitudinal NfL change was close to zero (+1.4 pg/mL). The IQR (from 25th to 75th percentile) is the range between −5.6 pg/mL and +14.2 pg/mL. 
With that constrains,  [Preliz](https://preliz.readthedocs.io/en/latest/index.html) shows that a Normal distribution with a sigma of 15 is good fit.

Over all patients Median is 51.8 pg/mL. IQR is 35.5 pg/mL to 85.9 pg/mL. With the constrains that 50% of the probability mass should be in the range of 35.5 pg/mL and 85.9 pg/mL and with a median of 51.8 pg/mL [Preliz](https://preliz.readthedocs.io/en/latest/index.html) shows that a Gamma distribution is good fit:

![](img/prior_nfl.png)


Here is the definition with [bambi](https://bambinos.github.io/bambi/):
```python
priors = {
    "Intercept": bmb.Prior("Gamma", alpha=3.18, beta=0.0551),
    "sigma": bmb.Prior("HalfNormal", sigma=15),
}
```

## ALSFRS Progression Prediction

To predict possible progression trajectories, the Mixture of Gaussian processes (MoGP) method is used [3]. The predictions of MoGP become more reliable once you have ALSFRS measurements for one year or longer.




## References

[1]  "PRO-ACT Dataset is the world’s largest ALS clinical trial data repository, compiling placebo and treatment-arm data from 30 phase II/III clinical trials and 12,229 fully anonymized longitudinal Subject records funded by The ALS Therapy Alliance, Prize4Life, Inc., Northeast ALS Consortium (NEALS), Neurological Clinical Research Institute of Mass. General Hospital, ALS Finding A Cure, and The ALS Association. Neurological Clinical Research Institute of Mass. General Hospital created and maintained the PRO-ACT Dataset and serves as the coordinating center and data distributor of the PRO-ACT Dataset. Find out more at www.alsdatabase.org" 

[2] Witzel S, Statland JM, Steinacker P, Otto M, Dorst J, Schuster J, Barohn RJ, Ludolph AC. Longitudinal course of neurofilament light chain levels in amyotrophic lateral sclerosis-insights from a completed randomized controlled trial with rasagiline. Eur J Neurol. 2024 Mar;31(3):e16154. doi: 10.1111/ene.16154. Epub 2023 Nov 17. PMID: 37975796; PMCID: PMC11235763.

[3] Ramamoorthy, D., Severson, K., Ghosh, S. et al. Identifying patterns in amyotrophic lateral sclerosis progression from sparse longitudinal data. Nat Comput Sci 2, 605–616 (2022). https://doi.org/10.1038/s43588-022-00299-w
