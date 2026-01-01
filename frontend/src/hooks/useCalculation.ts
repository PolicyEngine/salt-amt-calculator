/**
 * Hook for running API calculations.
 */

import { useCallback } from 'react';
import { useStore } from '@/store';
import {
  calculateSinglePoint,
  calculateSaltAxis,
  calculateIncomeAxis,
} from '@/api/client';

export function useCalculation() {
  const {
    household,
    policyConfig,
    setCalculating,
    setHasCalculated,
    setSinglePointResult,
    setSaltAxisResult,
    setIncomeAxisResult,
    setBaselineSinglePoint,
    setBaselineSaltAxis,
    setBaselineIncomeAxis,
    setError,
    setSlideIndex,
  } = useStore();

  const runCalculation = useCallback(async () => {
    setCalculating(true);
    setError(null);

    try {
      // Run all calculations in parallel
      const [
        singlePoint,
        saltAxis,
        incomeAxis,
        baselineSinglePoint,
        baselineSaltAxis,
        baselineIncomeAxis,
      ] = await Promise.all([
        // Current Law calculations
        calculateSinglePoint(household, 'Current Law', policyConfig),
        calculateSaltAxis(household, 'Current Law', policyConfig),
        calculateIncomeAxis(household, 'Current Law', policyConfig),
        // Current Policy calculations (for comparison)
        calculateSinglePoint(household, 'Current Policy', policyConfig),
        calculateSaltAxis(household, 'Current Policy', policyConfig),
        calculateIncomeAxis(household, 'Current Policy', policyConfig),
      ]);

      // Store results
      setSinglePointResult(singlePoint);
      setSaltAxisResult(saltAxis);
      setIncomeAxisResult(incomeAxis);
      setBaselineSinglePoint(baselineSinglePoint);
      setBaselineSaltAxis(baselineSaltAxis);
      setBaselineIncomeAxis(baselineIncomeAxis);

      setHasCalculated(true);
      setSlideIndex(1); // Move to first results slide
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Calculation failed';
      setError(message);
      console.error('Calculation error:', error);
    } finally {
      setCalculating(false);
    }
  }, [
    household,
    policyConfig,
    setCalculating,
    setHasCalculated,
    setSinglePointResult,
    setSaltAxisResult,
    setIncomeAxisResult,
    setBaselineSinglePoint,
    setBaselineSaltAxis,
    setBaselineIncomeAxis,
    setError,
    setSlideIndex,
  ]);

  return { runCalculation };
}
