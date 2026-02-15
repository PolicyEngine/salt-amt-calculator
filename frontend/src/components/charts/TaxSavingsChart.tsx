/**
 * Tax Savings chart - shows tax savings by income level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';

interface TaxSavingsChartProps {
  incomeValues: number[];
  taxSavings: number[];
  userIncome: number;
  userTaxSavings: number;
}

export function TaxSavingsChart({
  incomeValues,
  taxSavings,
  userIncome,
  userTaxSavings,
}: TaxSavingsChartProps) {
  const lines = [
    {
      x: incomeValues,
      y: taxSavings,
      name: 'Tax Savings',
      color: colors.primary[500],
    },
  ];

  const markers = [
    { x: userIncome, y: userTaxSavings, name: 'Your household', color: colors.primary[500] },
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Wages and salaries"
      yAxisTitle="Tax Savings"
      xRange={[0, 1000000]}
    />
  );
}
