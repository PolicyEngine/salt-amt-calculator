/**
 * Effective SALT Cap chart - shows effective SALT cap by income level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';

interface EffectiveSaltCapChartProps {
  incomeValues: number[];
  effectiveSaltCap: number[];
  userIncome: number;
  userEffectiveSaltCap: number;
}

export function EffectiveSaltCapChart({
  incomeValues,
  effectiveSaltCap,
  userIncome,
  userEffectiveSaltCap,
}: EffectiveSaltCapChartProps) {
  const lines = [
    {
      x: incomeValues,
      y: effectiveSaltCap,
      name: 'Effective SALT Cap',
      color: colors.primary[500],
    },
  ];

  const markers = [
    { x: userIncome, y: userEffectiveSaltCap, name: 'Your household', color: colors.primary[500] },
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Wages and salaries"
      yAxisTitle="Effective SALT cap (2026)"
      xRange={[0, 1000000]}
      yRange={[0, 200000]}
    />
  );
}
