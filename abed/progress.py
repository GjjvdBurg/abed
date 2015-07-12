"""
Functions for progress bars

"""

try:
    from progressbar import ProgressBar, Percentage, Bar, Timer
    PROGRESS = True
except ImportError:
    PROGRESS = False

try:
    assert PROGRESS
    from progressbar import AdaptiveETA
except AssertionError:
    pass
except ImportError:
    class AdaptiveETA(Timer):
        """Widget which attempts to estimate the time of arrival.

        Uses a weighted average of two estimates:
        1) ETA based on the total progress and time elapsed so far
        2) ETA based on the progress as per tha last 10 update reports

        The weight depends on the current progress so that to begin with the
        total progress is used and at the end only the most recent progress is
        used.
        """

        TIME_SENSITIVE = True
        NUM_SAMPLES = 10

        def _update_samples(self, currval, elapsed):
            sample = (currval, elapsed)
            if not hasattr(self, 'samples'):
                self.samples = [sample] * (self.NUM_SAMPLES + 1)
            else:
                self.samples.append(sample)
            return self.samples.pop(0)

        def _eta(self, maxval, currval, elapsed):
            return elapsed * maxval / float(currval) - elapsed

        def update(self, pbar):
            """Updates the widget to show the ETA or total time when 
            finished."""
            if pbar.currval == 0:
                return 'ETA:  --:--:--'
            elif pbar.finished:
                return 'Time: %s' % self.format_time(pbar.seconds_elapsed)
            else:
                elapsed = pbar.seconds_elapsed
                currval1, elapsed1 = self._update_samples(pbar.currval, elapsed)
                eta = self._eta(pbar.maxval, pbar.currval, elapsed)
                if pbar.currval > currval1:
                    etasamp = self._eta(pbar.maxval - currval1,
                            pbar.currval - currval1,
                            elapsed - elapsed1)
                    weight = (pbar.currval / float(pbar.maxval)) ** 0.5
                    eta = (1 - weight) * eta + weight * etasamp
                return 'ETA: %s' % self.format_time(eta)

class AbedProgress(object):
    def __init__(self, label):
        self.pm = ProgressBar(widgets=[label, Percentage(), ' ', Bar(), ' ', 
            AdaptiveETA()])

    def set_maximum(self, maxval):
        self.pm.maxval = maxval
        self.pm.start()

    def increment(self):
        self.pm.update(self.pm.currval + 1)
        if self.pm.currval == self.pm.maxval:
            self.pm.finish()

class NullProgress(object):
    def __init__(self):
        self.pm = None
    def set_maximum(self, maxval):
        pass
    def increment(self):
        pass

def iter_with_progress(iterable, pbar=NullProgress()):
    pbar.set_maximum(len(iterable))
    for element in iterable:
        yield element
        pbar.increment()

def iter_progress(iterable, label=''):
    if PROGRESS:
        return iter_with_progress(iterable, pbar=AbedProgress(label))
    else:
        return iter_with_progress(iterable)

def enum_with_progress(iterable, pbar=NullProgress()):
    pbar.set_maximum(len(iterable))
    count = 0
    for element in iterable:
        yield (count, element)
        pbar.increment()
        count += 1

def enum_progress(iterable, label=''):
    if PROGRESS:
        return enum_with_progress(iterable, pbar=AbedProgress(label))
    else:
        return enum_with_progress(iterable)
