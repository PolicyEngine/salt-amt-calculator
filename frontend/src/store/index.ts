/**
 * Zustand store for SALT-AMT calculator state management.
 */

import { create } from 'zustand';
import type {
  HouseholdInput,
  PolicyConfig,
  SinglePointResult,
  AxisResult,
  TwoAxesResult,
  BaselineScenario,
} from '@/types';
import { DEFAULT_HOUSEHOLD, DEFAULT_POLICY } from '@/types';

interface CalculationState {
  // Input state
  household: HouseholdInput;
  policyConfig: PolicyConfig;
  baselineScenario: BaselineScenario;

  // Navigation state
  slideIndex: number;
  isCalculating: boolean;
  hasCalculated: boolean;

  // Calculation results
  singlePointResult: SinglePointResult | null;
  saltAxisResult: AxisResult | null;
  incomeAxisResult: AxisResult | null;
  twoAxesResult: TwoAxesResult | null;
  baselineSinglePoint: SinglePointResult | null;
  baselineSaltAxis: AxisResult | null;
  baselineIncomeAxis: AxisResult | null;

  // Error state
  error: string | null;

  // Actions
  setHousehold: (household: Partial<HouseholdInput>) => void;
  setPolicyConfig: (config: Partial<PolicyConfig>) => void;
  setBaselineScenario: (scenario: BaselineScenario) => void;
  setSlideIndex: (index: number) => void;
  nextSlide: () => void;
  prevSlide: () => void;
  setCalculating: (isCalculating: boolean) => void;
  setSinglePointResult: (result: SinglePointResult | null) => void;
  setSaltAxisResult: (result: AxisResult | null) => void;
  setIncomeAxisResult: (result: AxisResult | null) => void;
  setTwoAxesResult: (result: TwoAxesResult | null) => void;
  setBaselineSinglePoint: (result: SinglePointResult | null) => void;
  setBaselineSaltAxis: (result: AxisResult | null) => void;
  setBaselineIncomeAxis: (result: AxisResult | null) => void;
  setHasCalculated: (hasCalculated: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const TOTAL_SLIDES = 17;

export const useStore = create<CalculationState>((set) => ({
  // Initial state
  household: DEFAULT_HOUSEHOLD,
  policyConfig: DEFAULT_POLICY,
  baselineScenario: 'Current Law',
  slideIndex: 0,
  isCalculating: false,
  hasCalculated: false,
  singlePointResult: null,
  saltAxisResult: null,
  incomeAxisResult: null,
  twoAxesResult: null,
  baselineSinglePoint: null,
  baselineSaltAxis: null,
  baselineIncomeAxis: null,
  error: null,

  // Actions
  setHousehold: (household) =>
    set((state) => ({
      household: { ...state.household, ...household },
      hasCalculated: false, // Reset when inputs change
    })),

  setPolicyConfig: (config) =>
    set((state) => ({
      policyConfig: { ...state.policyConfig, ...config },
      hasCalculated: false,
    })),

  setBaselineScenario: (scenario) =>
    set({
      baselineScenario: scenario,
      hasCalculated: false,
    }),

  setSlideIndex: (index) =>
    set({
      slideIndex: Math.max(0, Math.min(index, TOTAL_SLIDES - 1)),
    }),

  nextSlide: () =>
    set((state) => ({
      slideIndex: Math.min(state.slideIndex + 1, TOTAL_SLIDES - 1),
    })),

  prevSlide: () =>
    set((state) => ({
      slideIndex: Math.max(state.slideIndex - 1, 0),
    })),

  setCalculating: (isCalculating) => set({ isCalculating }),

  setSinglePointResult: (result) => set({ singlePointResult: result }),

  setSaltAxisResult: (result) => set({ saltAxisResult: result }),

  setIncomeAxisResult: (result) => set({ incomeAxisResult: result }),

  setTwoAxesResult: (result) => set({ twoAxesResult: result }),

  setBaselineSinglePoint: (result) => set({ baselineSinglePoint: result }),

  setBaselineSaltAxis: (result) => set({ baselineSaltAxis: result }),

  setBaselineIncomeAxis: (result) => set({ baselineIncomeAxis: result }),

  setHasCalculated: (hasCalculated) => set({ hasCalculated }),

  setError: (error) => set({ error }),

  reset: () =>
    set({
      household: DEFAULT_HOUSEHOLD,
      policyConfig: DEFAULT_POLICY,
      baselineScenario: 'Current Law',
      slideIndex: 0,
      isCalculating: false,
      hasCalculated: false,
      singlePointResult: null,
      saltAxisResult: null,
      incomeAxisResult: null,
      twoAxesResult: null,
      baselineSinglePoint: null,
      baselineSaltAxis: null,
      baselineIncomeAxis: null,
      error: null,
    }),
}));
