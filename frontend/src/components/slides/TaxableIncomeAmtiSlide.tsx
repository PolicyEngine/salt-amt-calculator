/**
 * Taxable Income and AMTI Comparison slide.
 */

import { Box, Text, Stack } from '@mantine/core';
import { colors, spacing, typography } from '@/designTokens';
import { TaxableIncomeAmtiChart } from '@/components/charts/TaxableIncomeAmtiChart';
import type { AxisResult } from '@/types';

interface TaxableIncomeAmtiSlideProps {
  currentLawData: AxisResult;
  currentPolicyData: AxisResult;
  userSalt: number;
  userTaxableIncomeLaw: number;
  userTaxableIncomePolicy: number;
  userAmtiLaw: number;
  userAmtiPolicy: number;
}

export function TaxableIncomeAmtiSlide({
  currentLawData,
  currentPolicyData,
  userSalt,
  userTaxableIncomeLaw,
  userTaxableIncomePolicy,
  userAmtiLaw,
  userAmtiPolicy,
}: TaxableIncomeAmtiSlideProps) {
  return (
    <Stack gap={spacing.lg}>
      <Text
        style={{
          fontSize: typography.fontSize.xl,
          fontWeight: typography.fontWeight.semibold,
          color: colors.text.primary,
        }}
      >
        But AMT income does not vary with SALT
      </Text>

      <Box style={{ width: '100%', minHeight: '400px' }}>
        <TaxableIncomeAmtiChart
          currentLawData={currentLawData}
          currentPolicyData={currentPolicyData}
          userSalt={userSalt}
          userTaxableIncomeLaw={userTaxableIncomeLaw}
          userTaxableIncomePolicy={userTaxableIncomePolicy}
          userAmtiLaw={userAmtiLaw}
          userAmtiPolicy={userAmtiPolicy}
        />
      </Box>

      <Text
        style={{
          fontSize: typography.fontSize.sm,
          color: colors.text.secondary,
        }}
      >
        AMT income equals taxable income plus exemptions and deductions including SALT.
      </Text>
    </Stack>
  );
}
