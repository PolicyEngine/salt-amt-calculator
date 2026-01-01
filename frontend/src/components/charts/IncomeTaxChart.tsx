/**
 * Income Tax chart - shows federal income tax by SALT level.
 */

import { ComparisonChart } from './BaseLineChart';
import type { AxisResult } from '@/types';

interface IncomeTaxChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userTaxLaw: number;
  userTaxPolicy: number;
  showCurrentPolicy?: boolean;
}

export function IncomeTaxChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userTaxLaw,
  userTaxPolicy,
  showCurrentPolicy = true,
}: IncomeTaxChartProps) {
  return (
    <ComparisonChart
      currentLawX={currentLawData.axisValues}
      currentLawY={currentLawData.incomeTax}
      currentPolicyX={currentPolicyData.axisValues}
      currentPolicyY={currentPolicyData.incomeTax}
      userX={userSalt}
      userYLaw={userTaxLaw}
      userYPolicy={userTaxPolicy}
      xAxisTitle="Reported SALT"
      yAxisTitle="Federal Income Tax (2026)"
      showCurrentPolicy={showCurrentPolicy}
      xRange={[0, 100000]}
    />
  );
}
