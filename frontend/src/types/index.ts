/**
 * Type definitions for the SALT-AMT calculator.
 */

export interface HouseholdInput {
  stateCode: string;
  isMarried: boolean;
  numChildren: number;
  childAges: number[];
  employmentIncome: number;
  realEstateTaxes: number;
  qualifiedDividendIncome: number;
  longTermCapitalGains: number;
  shortTermCapitalGains: number;
  deductibleMortgageInterest: number;
  charitableCashDonations: number;
}

export interface PolicyConfig {
  saltCap: string;
  saltMarriageBonus: boolean;
  saltPhaseout: string;
  saltRepealed: boolean;
  amtExemption: string;
  amtPhaseout: string;
  amtRepealed: boolean;
  amtEliminateMarriagePenalty: boolean;
  otherTcjaProvisionsExtended: string;
}

export interface SinglePointResult {
  householdNetIncome: number;
  federalIncomeTax: number;
  stateIncomeTax: number;
  stateSalesTax: number;
  saltDeduction: number;
  reportedSalt: number;
  regularTax: number;
  amt: number;
  taxableIncome: number;
  amtIncome: number;
  largerOfStateSalesOrIncomeTax: number;
  stateIncomeTaxOverSalesTax: boolean;
}

export interface AxisResult {
  axisValues: number[];
  saltDeduction: number[];
  regularTax: number[];
  amt: number[];
  incomeTax: number[];
  taxableIncome: number[];
  amtIncome: number[];
  reportedSalt?: number[];
  employmentIncome?: number[];
  gap?: number[];
}

export interface TwoAxesResult {
  employmentIncome: number[];
  reportedSalt: number[];
  regularTax: number[];
  amt: number[];
  saltDeduction: number[];
  incomeTax: number[];
  taxableIncome: number[];
  amtIncome: number[];
  amtBinds: boolean[];
}

export interface NationwideImpact {
  reform: string;
  totalIncomeChange: number;
  pctBetterOff: number;
  pctWorseOff: number;
  incomeDistribution: Record<string, number>;
  timeSeries?: { year: number; totalChange: number }[];
}

export type BaselineScenario = 'Current Law' | 'Current Policy';

export const STATE_CODES = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
] as const;

export const SALT_CAP_OPTIONS = [
  'Current Policy ($10k)',
  '$15k',
  '$100k',
  'Current Law (Uncapped)',
] as const;

export const AMT_EXEMPTION_OPTIONS = [
  'Current Law ($70,500 Single, $109,500 Joint)',
  'Current Policy ($89,925 Single, $139,850 Joint)',
] as const;

export const AMT_PHASEOUT_OPTIONS = [
  'Current Law ($156,700 Single, $209,000 Joint)',
  'Current Policy ($639,300 Single, $1,278,575 Joint)',
] as const;

export const SALT_PHASEOUT_OPTIONS = [
  'None',
  '10% for income over 200k (400k joint)',
] as const;

export const DEFAULT_HOUSEHOLD: HouseholdInput = {
  stateCode: 'CA',
  isMarried: true,
  numChildren: 2,
  childAges: [10, 8],
  employmentIncome: 200000,
  realEstateTaxes: 15000,
  qualifiedDividendIncome: 0,
  longTermCapitalGains: 0,
  shortTermCapitalGains: 0,
  deductibleMortgageInterest: 10000,
  charitableCashDonations: 5000,
};

export const DEFAULT_POLICY: PolicyConfig = {
  saltCap: 'Current Law (Uncapped)',
  saltMarriageBonus: false,
  saltPhaseout: 'None',
  saltRepealed: false,
  amtExemption: 'Current Law ($70,500 Single, $109,500 Joint)',
  amtPhaseout: 'Current Law ($156,700 Single, $209,000 Joint)',
  amtRepealed: false,
  amtEliminateMarriagePenalty: false,
  otherTcjaProvisionsExtended: 'Current Law',
};
