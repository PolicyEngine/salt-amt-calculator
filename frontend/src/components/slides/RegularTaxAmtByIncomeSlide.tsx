/**
 * Regular Tax and AMT Comparison by Income slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { RegularTaxAmtByIncomeChart } from '@/components/charts/RegularTaxAmtByIncomeChart';
import type { AxisResult } from '@/types';

interface RegularTaxAmtByIncomeSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userIncome: number;
  userRegularTaxLaw: number;
  userRegularTaxPolicy: number;
  userAmtLaw: number;
  userAmtPolicy: number;
}

export function RegularTaxAmtByIncomeSlide({
  currentLawData,
  currentPolicyData,
  userIncome,
  userRegularTaxLaw,
  userRegularTaxPolicy,
  userAmtLaw,
  userAmtPolicy,
}: RegularTaxAmtByIncomeSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        The gap from AMT to regular tax influences the effective SALT cap
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <RegularTaxAmtByIncomeChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userIncome={userIncome}
          userRegularTaxLaw={userRegularTaxLaw}
          userRegularTaxPolicy={userRegularTaxPolicy}
          userAmtLaw={userAmtLaw}
          userAmtPolicy={userAmtPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        AMT taxes income at a 26% rate for AMTI under $244,000 and 28% above.
        Your AMT phases in at higher income levels than regular tax due to the AMT exemption.
        In these earnings variation charts, all points assume no SALT.
      </Text>
    </Stack>
  );
}
