/**
 * SALT Deduction comparison chart component.
 * Shows SALT deduction vs reported SALT for Current Law and Current Policy.
 */

import { ComparisonChart } from './BaseLineChart';

interface ChartData {
  axisValues: number[];
  saltDeduction: number[];
}

interface SaltDeductionChartProps {
  currentLawData: ChartData;
  currentPolicyData: ChartData;
  userSalt: number;
  userDeductionLaw: number;
  userDeductionPolicy: number;
  showCurrentPolicy?: boolean;
}

export function SaltDeductionChart({
  currentLawData,
  currentPolicyData,
  userSalt,
  userDeductionLaw,
  userDeductionPolicy,
  showCurrentPolicy = true,
}: SaltDeductionChartProps) {
  return (
    <ComparisonChart
      currentLawX={currentLawData.axisValues}
      currentLawY={currentLawData.saltDeduction}
      currentPolicyX={currentPolicyData.axisValues}
      currentPolicyY={currentPolicyData.saltDeduction}
      userX={userSalt}
      userYLaw={userDeductionLaw}
      userYPolicy={userDeductionPolicy}
      xAxisTitle="Reported SALT"
      yAxisTitle="SALT Deduction (2026)"
      showCurrentPolicy={showCurrentPolicy}
      xRange={[0, 100000]}
    />
  );
}
