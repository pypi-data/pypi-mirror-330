from .modification import LocusModification
from ..models import HaplotypeTable
import pandas as pd
import numpy as np
from typing import Callable, Iterable, Optional
import logging
from .annotate import LOCUS_COLUMN_NAME

logger = logging.getLogger()


class Discretize(LocusModification):
    def __init__(self, discritization_type: str, thesholds: Iterable[float]) -> None:
        self._thresholds = thesholds
        self._discritization_type = discritization_type
        super().__init__()
        logger.debug('Initialized %r.', self)

    def __repr__(self):
        return (f'Discretize(discritization_type={self._discritization_type},'
                f'thesholds={self._thresholds})')

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> Optional[HaplotypeTable]:
        self._logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        self._logger.debug('Started discritization for locus %s', locus_name)
        previous_threshold, *other_threshold = self._thresholds
        for threshold in other_threshold:
            if previous_threshold > threshold:
                raise ValueError("Please make sure the frequency bounds "
                                 "define non-overlapping intervals.")
            previous_threshold = threshold
        calling_function = self._discrete_calls_dispatch(self._discritization_type)
        discrete_calls = calling_function(locus, self._thresholds)\
            .apply(pd.to_numeric).apply(np.round).astype(pd.Int64Dtype())
        return HaplotypeTable(discrete_calls)

    def _discrete_calls_dispatch(self, call_type: str) -> Callable:
        cases = {
            "dominant": self._calculate_dominant,
            "dosage": self._calculate_dosage,
        }
        return cases[call_type]

    def _calculate_dosage(self, df: pd.DataFrame, thresholds) -> pd.DataFrame:
        def pairwise(lst):
            """Yield successive 2-sized chunks from lst."""
            for i in range(0, len(lst), 2):
                yield lst[i:i + 2]
        not_detected, *hetero_bounds, homozygous_lower_bound = thresholds
        undetected_mask = df <= not_detected
        heteroz_masks = [(df >= lower_bound) & (df <= upper_bound)
                         for lower_bound, upper_bound in pairwise(hetero_bounds)]
        other_masks = [(df > lower_bound) & (df < upper_bound)
                       for lower_bound, upper_bound in pairwise(thresholds)]
        homoz_mask = df >= homozygous_lower_bound
        dosages = df.mask(undetected_mask, other=0)
        for i, heteroz_mask in enumerate(heteroz_masks, start=1):
            dosages = dosages.mask(heteroz_mask, other=i)
        dosages = dosages.mask(homoz_mask, other=i + 1)
        for other_mask in other_masks:
            dosages = dosages.mask(other_mask, other=pd.NA)

        return dosages

    def _calculate_dominant(self, df: pd.DataFrame, thresholds) -> pd.DataFrame:
        bound, = thresholds
        not_detected = df <= bound
        dom_mask = df > bound
        dosages = df.mask(not_detected, other=0)
        dosages = dosages.mask(dom_mask, other=1)
        return dosages
