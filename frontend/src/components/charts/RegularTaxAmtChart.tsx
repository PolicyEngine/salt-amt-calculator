/**
 * Regular Tax and AMT chart - shows regular tax and AMT by SALT level.
 */

import { BaseLineChart } from './BaseLineChart';
import { colors } from '@/designTokens';
import type { AxisResult } from '@/types';

interface RegularTaxAmtChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userRegularTaxLaw: number;
  userRegularTaxPolicy: number;
  userAmtLaw: number;
  userAmtPolicy: number;
  showCurrentPolicy?: boolean;
}

export function RegularTaxAmtChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userRegularTaxLaw,
  userRegularTaxPolicy,
  userAmtLaw,
  userAmtPolicy,
  showCurrentPolicy = true,
}: RegularTaxAmtChartProps) {
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
    { x: userSalt, y: userRegularTaxLaw, name: 'You Tax (Law)', color: colors.primary[500] },
    { x: userSalt, y: userAmtLaw, name: 'You AMT (Law)', color: colors.primary[500] },
    ...(showCurrentPolicy
      ? [
          { x: userSalt, y: userRegularTaxPolicy, name: 'You Tax (Policy)', color: colors.gray[400] },
          { x: userSalt, y: userAmtPolicy, name: 'You AMT (Policy)', color: colors.gray[400] },
        ]
      : []),
  ];

  return (
    <BaseLineChart
      lines={lines}
      markers={markers}
      xAxisTitle="Reported SALT"
      yAxisTitle="Tax Amount (2026)"
      xRange={[0, 100000]}
    />
  );
}
