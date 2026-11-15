"""Direction of a tired baseline. SYNTHETIC, one fresh seed. Does not run the full study."""
import pandas as pd

from csync.rules import DIRECTION
from research.biased_baseline import clean_frame, personal_sd, shift_baseline


def test_shift_moves_days_1_to_5_in_the_unfavourable_direction():
    dv = clean_frame(65000)
    sd = personal_sd(dv)
    tired = shift_baseline(dv, 1.0, sd)
    for ind in sd.index:
        step = sd[ind]
        if pd.isna(step) or step <= 0:
            continue
        delta = tired.loc[1:5, ind].mean() - dv.loc[1:5, ind].mean()
        assert delta * DIRECTION[ind] > 0
        assert tired.loc[6:10, ind].equals(dv.loc[6:10, ind])
