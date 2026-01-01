/**
 * Effective SALT Cap slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { EffectiveSaltCapChart } from '@/components/charts/EffectiveSaltCapChart';

interface EffectiveSaltCapSlideProps {
  incomeValues: number[];
  effectiveSaltCap: number[];
  userIncome: number;
  userEffectiveSaltCap: number;
  variant: 'intro' | 'formula';
}

export function EffectiveSaltCapSlide({
  incomeValues,
  effectiveSaltCap,
  userIncome,
  userEffectiveSaltCap,
  variant,
}: EffectiveSaltCapSlideProps) {
  const title = variant === 'intro'
    ? 'AMT effectively caps SALT'
    : 'The effective SALT cap ~= Gap / Marginal tax rate';

  const description = variant === 'intro'
    ? 'AMT functions as an implicit cap on SALT by disallowing them under AMTI, limiting the tax benefit when AMT exceeds regular tax.'
    : 'The effective SALT cap can be approximated by dividing the gap between regular tax and AMT (assuming no SALT) by the marginal tax rate.';

  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        {title}
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <EffectiveSaltCapChart
          incomeValues={incomeValues}
          effectiveSaltCap={effectiveSaltCap}
          userIncome={userIncome}
          userEffectiveSaltCap={userEffectiveSaltCap}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        {description}
      </Text>
    </Stack>
  );
}
