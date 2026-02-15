/**
 * Gap chart - shows gap between Regular Tax and AMT by income level.
 */

import { ComparisonChart } from './BaseLineChart';
import type { AxisResult } from '@/types';

interface GapChartProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userIncome: number;
  userGapLaw: number;
  userGapPolicy: number;
  showCurrentPolicy?: boolean;
}

export function GapChart({
  currentLawData,
  currentPolicyData,
  userIncome,
  userGapLaw,
  userGapPolicy,
  showCurrentPolicy = true,
}: GapChartProps) {
  return (
    <ComparisonChart
      currentLawX={currentLawData.axisValues}
      currentLawY={currentLawData.gap || []}
      currentPolicyX={currentPolicyData.axisValues}
      currentPolicyY={currentPolicyData.gap || []}
      userX={userIncome}
      userYLaw={userGapLaw}
      userYPolicy={userGapPolicy}
      xAxisTitle="Wages and salaries"
      yAxisTitle="Gap between Regular Tax and AMT (assuming no SALT)"
      showCurrentPolicy={showCurrentPolicy}
      xRange={[0, 1000000]}
    />
  );
}
