/**
 * Marginal Rate Chart slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { MarginalRateChart } from '@/components/charts/MarginalRateChart';

interface MarginalRateSlideProps {
  currentLawIncome: number[];
  currentLawMarginalRate: number[];
  currentPolicyIncome: number[];
  currentPolicyMarginalRate: number[];
  userIncome: number;
  userMarginalRateLaw: number;
  userMarginalRatePolicy: number;
}

export function MarginalRateSlide({
  currentLawIncome,
  currentLawMarginalRate,
  currentPolicyIncome,
  currentPolicyMarginalRate,
  userIncome,
  userMarginalRateLaw,
  userMarginalRatePolicy,
}: MarginalRateSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        SALT reduces income tax at roughly the regular marginal tax rate
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <MarginalRateChart
          currentLawIncome={currentLawIncome}
          currentLawMarginalRate={currentLawMarginalRate}
          currentPolicyIncome={currentPolicyIncome}
          currentPolicyMarginalRate={currentPolicyMarginalRate}
          userIncome={userIncome}
          userMarginalRateLaw={userMarginalRateLaw}
          userMarginalRatePolicy={userMarginalRatePolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        Your marginal tax rate is the additional regular federal income tax
        (not including credits) owed per additional dollar of taxable income.
      </Text>
    </Stack>
  );
}
