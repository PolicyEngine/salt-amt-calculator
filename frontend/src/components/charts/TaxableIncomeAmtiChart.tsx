/**
 * Taxable Income and AMTI chart - shows taxable income and AMTI by SALT level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface TaxableIncomeAmtiChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userTaxableIncomeLaw: number;
  userTaxableIncomePolicy: number;
  userAmtiLaw: number;
  userAmtiPolicy: number;
  showCurrentPolicy?: boolean;
}

export function TaxableIncomeAmtiChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userTaxableIncomeLaw,
  userTaxableIncomePolicy,
  userAmtiLaw,
  userAmtiPolicy,
  showCurrentPolicy = true,
}: TaxableIncomeAmtiChartProps) {
  const lines = [
    {
      x: currentLawData.axisValues,
      y: currentLawData.taxableIncome,
      name: 'Taxable Income (Current Law)',
      color: colors.primary[500],
    },
    {
      x: currentLawData.axisValues,
      y: currentLawData.amtIncome,
      name: 'AMTI (Current Law)',
      color: colors.primary[500],
      dash: 'dot' as const,
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.taxableIncome,
      name: 'Taxable Income (Current Policy)',
      color: colors.gray[400],
      visible: showCurrentPolicy ? ('legendonly' as const) : (false as const),
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.amtIncome,
      name: 'AMTI (Current Policy)',
      color: colors.gray[400],
      dash: 'dot' as const,
      visible: showCurrentPolicy ? ('legendonly' as const) : (false as const),
    },
  ];

  const markers = [
    { x: userSalt, y: userTaxableIncomeLaw, name: 'You TI (Law)', color: colors.primary[500] },
    { x: userSalt, y: userAmtiLaw, name: 'You AMTI (Law)', color: colors.primary[500] },
    ...(showCurrentPolicy
      ? [
          { x: userSalt, y: userTaxableIncomePolicy, name: 'You TI (Policy)', color: colors.gray[400] },
          { x: userSalt, y: userAmtiPolicy, name: 'You AMTI (Policy)', color: colors.gray[400] },
        ]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Reported SALT"
      yAxisTitle="Taxable Income (2026)"
      xRange={[0, 100000]}
    />
  );
}
