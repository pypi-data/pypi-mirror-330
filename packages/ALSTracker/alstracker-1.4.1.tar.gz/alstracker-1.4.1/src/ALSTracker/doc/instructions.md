# ALSTracker Excel file

There are two mandatory sheets and as many measurement sheets as you like. The order of the sheets does not matter.

## Measurement sheets

Create one sheet for each score you measure. The sheets for the ALSFRS-R score, the vital capacity score, Neurofilament light chain measurements and the grip strength are already given in the template. Please don't change their names they use prior knowledge from the scientific literature for them. All other scores can be named arbitrarily.

The first column must be titled "Date" and contain the date of the measurement in the format DAY.MONTH.YEAR.

It must contain at least one other column with your measurement, you can also give it an abitary title such as "Score".

If you are making a new entry, add the measurement without a unit. The unit will be given in the meta sheet instead.
 
## Mandatory sheets

### Meta

One of your sheets must be called "Meta". It contains meta data about your measurement sheets. It must have the following columns:

- **Sheet**: The exact name of the measurement sheet, e.g. "ALSFRS-R Score".
- **Value**: The name of the column in which the score can be found, e.g. "Score".
- **HigherIsBetter**: Either "Yes" or "No". ALSFRS-R Score would get a "Yes", Neurofilaments would get a "No".
- **Unit**: The unit of your "value". For ALSFRS-R it would be "points". For grip strength it would be "kg".
- **Type**: Defines the type of analysis. "S" is for slope and therefore for measurements that decline over time, e.g "ALSFRS-R Score". "L" is for Level measurements. These tend to fluctuate around a constant level but might change their level during a treatment phase. An example would be "Neurofilament light chain".

### Other
This sheet contains arbitrary information that the ALSTracker needs. It must have the following columns:

- **Name**: The name of the information you provide, e.g. "Onset".
- **Value**: Value for the information, e.g. "01.01.2024".

You have to define your disease onset date with the Name "Onset" and Value the onset date in format DAY.MONTH.YEAR.

### Phases

This is not strictly mandatory. The script always calculates statistics for all data points. But at some point you might want to compare different phases, such as "Reference" vs. "TreatmentA".

- **Phasename**: An arbitrary name for the phase. For example, "Reference" or "Actyl-L-Carnitine".
- **Start**: The start date of the phase in the format DAY.MONTH.YEAR.
- **End**: End date of the phase in the format DAY.MONTH.YEAR.

You can also define open phases by leaving the start or the end date blank.