/**
 * Gap Chart slide - shows gap between Regular Tax and AMT by income.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { GapChart } from '@/components/charts/GapChart';
import type { AxisResult } from '@/types';

interface GapSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userIncome: number;
  userGapLaw: number;
  userGapPolicy: number;
}

export function GapSlide({
  currentLawData,
  currentPolicyData,
  userIncome,
  userGapLaw,
  userGapPolicy,
}: GapSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        The gap from AMT to regular tax—absent SALT—influences the effective SALT cap
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <GapChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userIncome={userIncome}
          userGapLaw={userGapLaw}
          userGapPolicy={userGapPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        The gap represents the difference between regular tax and AMT when assuming no SALT deductions.
      </Text>
    </Stack>
  );
}
