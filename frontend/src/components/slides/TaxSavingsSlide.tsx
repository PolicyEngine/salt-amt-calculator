/**
 * Tax Savings Chart slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { TaxSavingsChart } from '@/components/charts/TaxSavingsChart';

interface TaxSavingsSlideProps {
  incomeValues: number[];
  taxSavings: number[];
  userIncome: number;
  userTaxSavings: number;
}

export function TaxSavingsSlide({
  incomeValues,
  taxSavings,
  userIncome,
  userTaxSavings,
}: TaxSavingsSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        Lastly, this is how much you could potentially save due to SALT
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <TaxSavingsChart
          incomeValues={incomeValues}
          taxSavings={taxSavings}
          userIncome={userIncome}
          userTaxSavings={userTaxSavings}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        Tax savings represent the difference between income tax at zero SALT and
        income tax at the effective SALT cap.
      </Text>
    </Stack>
  );
}
