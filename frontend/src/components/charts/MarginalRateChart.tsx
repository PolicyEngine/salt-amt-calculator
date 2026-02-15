/**
 * Marginal Rate chart - shows marginal tax rate by income level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';

interface MarginalRateChartProps {
  currentLawIncome: number[];
  currentLawMarginalRate: number[];
  currentPolicyIncome: number[];
  currentPolicyMarginalRate: number[];
  userIncome: number;
  userMarginalRateLaw: number;
  userMarginalRatePolicy: number;
  showCurrentPolicy?: boolean;
}

export function MarginalRateChart({
  currentLawIncome,
  currentLawMarginalRate,
  currentPolicyIncome,
  currentPolicyMarginalRate,
  userIncome,
  userMarginalRateLaw,
  userMarginalRatePolicy,
  showCurrentPolicy = true,
}: MarginalRateChartProps) {
  const lines = [
    {
      x: currentLawIncome,
      y: currentLawMarginalRate,
      name: 'Current Law',
      color: colors.primary[500],
    },
    {
      x: currentPolicyIncome,
      y: currentPolicyMarginalRate,
      name: 'Current Policy',
      color: colors.gray[400],
      dash: 'dash' as const,
      visible: showCurrentPolicy ? ('legendonly' as const) : (false as const),
    },
  ];

  const markers = [
    { x: userIncome, y: userMarginalRateLaw, name: 'You (Law)', color: colors.primary[500] },
    ...(showCurrentPolicy
      ? [{ x: userIncome, y: userMarginalRatePolicy, name: 'You (Policy)', color: colors.gray[400] }]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Wages and salaries"
      yAxisTitle="Marginal Tax Rate (2026)"
      xRange={[0, 1000000]}
      yRange={[0, 1]}
      yTickFormat=".1%"
    />
  );
}
