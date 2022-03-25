import time,sys
import numpy as np

def ProgressBar(total, progress, starttime = np.nan):
    """ 
    ProgressBar - Displays or updates a console progress bar.
    Adapted by Catherine Slaughter from https://stackoverflow.com/a/15860757/1391441
    For HCI Spring 2022
    """
    barLength, status = 50, "Running..."
    elapsed = time.time()-starttime
    mins, secs = divmod(elapsed, 60)
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "Complete \r\n"
    block = int(round(barLength * progress))
    
    if np.isnan(starttime):
        text = "\r[{}] {:.0f}% {}".format("#" * block + "-" * (barLength - block), round(progress * 100, 0), status)
    else:
        text = "\r[{}] {:.0f}% ({:02d}:{:02d})".format("#" * block + "-" * (barLength - block), round(progress * 100, 0), int(mins), int(secs))
    sys.stdout.write(text)
    sys.stdout.flush()