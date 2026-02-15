/**
 * Regular Tax and AMT by Income chart - shows regular tax and AMT by income level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface RegularTaxAmtByIncomeChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userIncome: number;
  userRegularTaxLaw: number;
  userRegularTaxPolicy: number;
  userAmtLaw: number;
  userAmtPolicy: number;
  showCurrentPolicy?: boolean;
}

export function RegularTaxAmtByIncomeChart({
  currentLawData,
  currentPolicyData,
  userIncome,
  userRegularTaxLaw,
  userRegularTaxPolicy,
  userAmtLaw,
  userAmtPolicy,
  showCurrentPolicy = true,
}: RegularTaxAmtByIncomeChartProps) {
  const lines = [
    {
      x: currentLawData.axisValues,
      y: currentLawData.regularTax,
      name: 'Regular Tax (Current Law)',
      color: colors.primary[500],
    },
    {
      x: currentLawData.axisValues,
      y: currentLawData.amt,
      name: 'AMT (Current Law)',
      color: colors.primary[500],
      dash: 'dot' as const,
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.regularTax,
      name: 'Regular Tax (Current Policy)',
      color: colors.gray[400],
      visible: showCurrentPolicy ? ('legendonly' as const) : (false as const),
    },
    {
      x: currentPolicyData.axisValues,
      y: currentPolicyData.amt,
      name: 'AMT (Current Policy)',
      color: colors.gray[400],
      dash: 'dot' as const,
      visible: showCurrentPolicy ? ('legendonly' as const) : (false as const),
    },
  ];

  const markers = [
    { x: userIncome, y: userRegularTaxLaw, name: 'You Tax (Law)', color: colors.primary[500] },
    { x: userIncome, y: userAmtLaw, name: 'You AMT (Law)', color: colors.primary[500] },
    ...(showCurrentPolicy
      ? [
          { x: userIncome, y: userRegularTaxPolicy, name: 'You Tax (Policy)', color: colors.gray[400] },
          { x: userIncome, y: userAmtPolicy, name: 'You AMT (Policy)', color: colors.gray[400] },
        ]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Wages and salaries"
      yAxisTitle="Tax Amount (assuming no SALT, 2026)"
      xRange={[0, 1000000]}
    />
  );
}
