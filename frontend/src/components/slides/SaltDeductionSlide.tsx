/**
 * SALT Deduction Comparison slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { SaltDeductionChart } from '@/components/charts/SaltDeductionChart';
import type { AxisResult } from '@/types';

interface SaltDeductionSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userDeductionLaw: number;
  userDeductionPolicy: number;
}

export function SaltDeductionSlide({
  currentLawData,
  currentPolicyData,
  userSalt,
  userDeductionLaw,
  userDeductionPolicy,
}: SaltDeductionSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        Current policy creates an explicit SALT cap
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <SaltDeductionChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userSalt={userSalt}
          userDeductionLaw={userDeductionLaw}
          userDeductionPolicy={userDeductionPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        TCJA capped SALT at $10,000; prior law allowed deductions for all SALT.
      </Text>
    </Stack>
  );
}
